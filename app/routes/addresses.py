import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database.connection import get_db
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate, Address as AddressSchema
from app.utils.logger import logger

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.post("/", response_model=AddressSchema)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@router.get("/", response_model=List[AddressSchema])
def get_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = db.query(Address).offset(skip).limit(limit).all()
    return addresses

@router.get("/{address_id}", response_model=AddressSchema)
def get_address(address_id: uuid.UUID, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.address_id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.put("/{address_id}", response_model=AddressSchema)
def update_address(address_id: uuid.UUID, address_update: AddressUpdate, db: Session = Depends(get_db)):
    try:
        address = db.query(Address).filter(Address.address_id == address_id).first()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        for field, value in address_update.dict(exclude_unset=True).items():
            setattr(address, field, value)
        db.commit()
        db.refresh(address)
        logger.info(f"Address {address_id} updated successfully")
        return address
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating address {address_id}: {traceback.format_exc(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{address_id}")
def delete_address(address_id: uuid.UUID, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.address_id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return {"message": "Address deleted successfully"}

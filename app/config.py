class UnittestConfig:
    """
    Configuration class for unit tests.
    """
    # Define any configuration variables needed for unit tests here
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'sqlite:///:memory:'  # Use an in-memory database for testing
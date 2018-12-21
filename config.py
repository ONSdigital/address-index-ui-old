import os


class DevConfig:
    ENVIRONMENT = 'DEV'
    USE_FAKE_DATA = bool(os.getenv('USE_FAKE_DATA', False))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 2))
    AUTH_TIMEOUT = int(os.getenv('AUTH_TIMEOUT', 2))
    AUTH_URL = os.getenv('AUTH_URL', 'http://localhost:3002/auth')
    API_URL = 'http://addressindex-api-dev.apps.devtest.onsclofo.uk'
    # API_URL = os.getenv('API_URL', 'http://addressindex-api-dev.apps.devtest.onsclofo.uk')
    SECRET_KEY = os.getenv('SECRET_KEY', 'you will never guess')


class TestConfig(DevConfig):
    ENVIRONMENT = 'TEST'
    LOG_LEVEL = 'DEBUG'


class ProdConfig(DevConfig):
    """
    For the 'important' environment variables (URLs, secret key), we want to be able to 'fail-fast' if no environment
    variable has been set, so we will leave those config values as None. For non-vital config such as
    timeouts, we provide a default value. When the config is being loaded in PROD,the REQUIRED_VARS list will be
    used to fail the startup if any values are missing.
    """
    REQUIRED_VARS = ['AUTH_URL', 'API_URL', 'SECRET_KEY', 'ENVIRONMENT']
    USE_FAKE_DATA = False
    ENVIRONMENT = 'PROD'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING')
    AUTH_URL = os.getenv('AUTH_URL')
    API_URL = os.getenv('API_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')


host = os.getenv('HOST')
port = os.getenv('PORT')
api_url = "http://addressindex-api-dev.apps.devtest.onsclofo.uk"



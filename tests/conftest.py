import os
import secrets

TEST_API_KEY = secrets.token_hex(16)
TEST_BASE_URL = 'https://demo.unittest.fake.data.com'
TEST_BASE_URL_PREFIX = '/test'

# Mocking environment variables required for the tests before importing other modules
os.environ['API_KEY'] = TEST_API_KEY
os.environ['BASE_URL'] = TEST_BASE_URL
os.environ['BASE_URL_PREFIX'] = TEST_BASE_URL_PREFIX


# Load fixtures
pytest_plugins = ['tests.fixtures']

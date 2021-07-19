import os
# NOTE: database user given must be a superuser to successfully execute all tests.
default_connection = 'postgresql://tethys_super:pass@localhost:5436/temp_precip_trends_tests'
TEST_DB_URL = os.environ.get('TPT_TEST_DATABASE', default_connection)

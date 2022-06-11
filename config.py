##########################################
SECRET_KEY = "mysupersecretkey"

PSQL_HOST = "139.28.223.150"
PSQL_PORT = 5432
PSQL_DBNAME = "test"
PSQL_USER = "admin"
PSQL_PASSWD = "nel"

ADMIN_LOGIN = "Admin"
ADMIN_PASSWORD = "youshallnotpass"

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 5000
SERVER_ENV = "development"

SERVER_DOMAIN = "127.0.0.1"
SSL_ENABLED = False

SESSION_COOKIE_SAMESITE = "Lax"
##########################################

base_url = ("https://" if SSL_ENABLED else "http://") + SERVER_DOMAIN

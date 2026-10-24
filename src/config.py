class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'api_utl'  
    MYSQL_CURSORCLASS='Cursor'

config = {
    'development': DevelopmentConfig
}
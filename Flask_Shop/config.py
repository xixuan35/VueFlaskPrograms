import os


class Config:
    # 设置参数
    MYSQL_DIALECT = "mysql"
    MYSQL_DRIVER = "pymysql"
    MYSQL_USERNAME = "root"
    MYSQL_PASSWORD = "root"
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_DB = "flask_shop"
    MYSQL_CHARSET = "utf8mb4"
    # 数据库链接字符串url
    SQLALCHEMY_DATABASE_URI = f"{MYSQL_DIALECT}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset={MYSQL_CHARSET}"
    # 设置数据盐
    SECRET_KEY = os.urandom(16)
    # 设置JSON数据部使用ASCI编码
    JSON_AS_ASCII = False
    RESTFUL_JSON = {"ensure_ascii": False}
    # 设置token过期时间,以秒为单位
    JWT_EXPIRATION_DELTA = 60 * 60 * 24 * 7  # 7天
    # 设置可以上传的图片类型
    ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]
    # 获取当前项目的根路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 设置图片上传的路径
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "FLASK_SHOP", "static/upload")


class DevelopConfig(Config):
    DEBUG = True


class ProductConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    pass


config_map = {"develop": DevelopConfig, "product": ProductConfig, "test": TestingConfig}

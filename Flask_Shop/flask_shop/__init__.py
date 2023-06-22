from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_map

# 创建SQLALCHEMY实例
db = SQLAlchemy()


def create_app(config_name):
    # 创建一个flask实例
    app = Flask(__name__)
    # 根据config_name获取配置类
    Config = config_map.get(config_name)
    # 根据配置类加载配置信息
    app.config.from_object(Config)
    # 初始化db
    db.init_app(app)
    # 获取user蓝图对象
    from flask_shop.user import user_bp

    # 注册蓝图
    app.register_blueprint(user_bp)
    # 获取蓝图对象
    from flask_shop.menu import menu_bp

    # 注册蓝图对象
    app.register_blueprint(menu_bp)
    # 获取role蓝图对象
    from flask_shop.roles import roles_bp

    # 注册蓝图对象
    app.register_blueprint(roles_bp)
    # 获取categroy蓝图对象
    from flask_shop.category import cate_bp

    # 注册蓝图对象
    app.register_blueprint(cate_bp)
    # 获取attribute蓝图对象
    from flask_shop.category import attr_bp

    # 注册蓝图对象
    app.register_blueprint(attr_bp)

    # 获取product蓝图对象
    from flask_shop.product import product_bp

    # 注册蓝图
    app.register_blueprint(product_bp)

    # 获取order蓝图对象
    from flask_shop.order import order_bp

    # 注册蓝图
    app.register_blueprint(order_bp)
    # 返回flask实例
    return app

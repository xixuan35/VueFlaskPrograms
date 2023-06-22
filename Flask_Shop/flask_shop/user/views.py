from flask_shop.user import user_bp, user_api
from flask_shop import db, modles
from flask import request
import re
from flask_restful import Resource, reqparse
from flask_shop.utils.token import generate_token, verify_token, login_required

"""
get() 这是个比较特殊的方法。它用于根据主键来返回查询结果，因此它有个参数就是要查询的对象的主键。如果没有该主键的结果返回 None ，否则返回这个结果。
flask_restful.reqparse详解
default:请求参数没有传入时，默认赋值
location:参数位置，要从（location:args,form,json,headers,cokkies等）获取数据，默认时json,value
"""


# 创建视图
@user_bp.route("/")
def index():
    return "what your name"


# 登录功能
@user_bp.route("/login/", methods=["POST"])
def login():
    # 获取用户名
    # name = request.form.get('name')  # content-type: application/x-www-form-urlencoded
    name = request.get_json().get("name")
    print(name)  # content-type: application/json
    # 获取密码
    pwd = request.get_json().get("pwd")
    # 判断是否传递数据完整
    if not all([name, pwd]):
        return {"status": 400, "msg": "参数不完整"}
    else:
        # 通过用户名获取用户对象
        user = modles.User.query.filter(modles.User.name == name).first()
        # 判断用户是否存在
        if user:
            if user.check_passwd(pwd):
                # 生成一个token
                token = generate_token({"id": user.id})
                return {"status": 200, "msg": "登录成功", "data": {"token": token}}
        return {"status": 400, "msg": "用户名或密码错误"}


class Users(Resource):
    def get(self):
        msg = request.args.get("name")
        print(request.args.get("pnum"), "================================")
        # 创建RequestParse对象
        parser = reqparse.RequestParser()
        # 添加参数
        # 获取页数
        parser.add_argument("pnum", type=int, default=1, location="args")
        # 获取数据数量
        parser.add_argument("psize", type=int, default=5, location="args")
        # 模糊查询参数
        parser.add_argument("name", type=str, location="args")

        # 解析参数
        args = parser.parse_args()
        # 获取解析结果的数据
        name = args.get("name")
        pnum = args.get("pnum")
        psize = args.get("psize")
        # 判断是否传递了name
        if name:
            # 获取用户列表
            user_list = modles.User.query.filter(
                modles.User.name.like(f"%{name}%")
            ).paginate(page=pnum, per_page=psize)
        else:
            # 获取用户列表
            user_list = modles.User.query.paginate(page=pnum, per_page=psize)
        data = {
            "total": user_list.total,
            "pnum": pnum,
            "data": [u.to_dict() for u in user_list.items],
        }
        return {"status": 200, "msg": "获取用户列表成功", "data": data}

    def post(self):
        # 注册用户
        # 接收用户信息
        name = request.get_json().get("name")
        print(name)
        pwd = request.get_json().get("pwd")
        real_pwd = request.get_json().get("real_pwd")
        # 验证数据的合法性
        if not all([name, pwd, real_pwd]):
            return {"status": 400, "msg": "参数不完整"}
        # 判断两次密码是否一致
        if pwd != real_pwd:
            return {"status": 400, "msg": "两次密码不一致"}
        # 判断用户名是否合法
        if len(name) < 2:
            return {"status": 400, "msg": "用户名不合法"}
        # 接收手机号和邮箱
        phone = request.get_json().get("phone")
        email = request.get_json().get("email")
        # 接收用户角色id
        role_id = request.get_json().get("role_id")
        # 昵称
        nick_name = request.get_json().get("nick_name")
        if phone:
            if not re.match(r"^1[3456789]\d{9}$", phone):
                return {"status": 400, "msg": "手机号不合法"}
        if email:
            if not re.match(
                r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", email
            ):
                return {"status": 400, "message": "邮箱不合法"}
        try:
            # 判断用户名是否存在
            print(modles.User.name)
            user = modles.User.query.filter(modles.User.name == name).first()
            if user:
                return {"status": 400, "message": "用户名已存在"}
        except Exception as e:
            print(e)
        print(2)
        # 创建用户对象
        if role_id:
            user = modles.User(
                name=name,
                password=pwd,
                phone=phone,
                email=email,
                nick_name=nick_name,
                role_id=role_id,
            )
        else:
            user = modles.User(
                name=name, password=pwd, phone=phone, email=email, nick_name=nick_name
            )
        # 保存到数据库
        db.session.add(user)
        db.session.commit()
        return {"status": 200, "message": "注册成功"}


class User(Resource):
    def get(self, id):
        info = modles.User.query.get(id)
        if info:
            return {"status": 200, "message": "查询成功", "data": info.to_dict()}
        else:
            return {"status": 404, "message": "用户不存在"}

    def put(self, id):
        try:
            # 根据参数查询修改用户
            user = modles.User.query.get(id)
            # 创建RequestParse对象
            parse = reqparse.RequestParser()
            # 添加修改参数
            parse.add_argument("nick_name", type=str)
            parse.add_argument("phone", type=str)
            parse.add_argument("email", type=str)
            parse.add_argument("role_id", type=int)
            # 解析参数
            args = parse.parse_args()
            if args.get("nick_name"):
                user.nick_name = args.get("nick_name")
            if args.get("phone"):
                user.phone = args.get("phone")
            if args.get("email"):
                user.email = args.get("email")
            if args.get("role_id"):
                user.role_id = args.get("role_id")
            db.session.commit()
            return {"status": 200, "message": "修改成功", "data": user.to_dict()}
        except BaseException as e:
            print(e)
            return {"status": 400, "message": "修改失败"}

    def delete(self, id):
        try:
            # 根据参数查询修改用户
            user = modles.User.query.get(id)
            if user:
                db.session.delete(user)
                db.session.commit()
            return {"status": 200, "message": "删除成功"}
        except BaseException as e:
            print(e)
            return {"status": 400, "message": "删除失败"}


user_api.add_resource(User, "/user/<int:id>/")
user_api.add_resource(Users, "/users/")


# 由于该方法不需要向前端返回什么，所以不采用restful
@user_bp.route("/resetpwd/<int:id>/")
def resetpwd(id):
    try:
        # 根据用户id查找用户
        user = modles.User.query.get(id)
        # 修改用户密码
        user.password = "123456789"
        db.session.commit()
        return {"status": 200, "message": "修改密码成功"}
    except BaseException as e:
        print(e)
        return {"status": 404, "message": "修改失败"}


@user_bp.route("/test/")
@login_required
def test_login_required():
    return {"status": 200, "message": "验证成功"}

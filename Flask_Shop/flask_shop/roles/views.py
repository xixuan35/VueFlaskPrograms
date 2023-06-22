from flask_shop.roles import roles_bp, role_api
from flask_restful import Resource, reqparse
from flask_shop import modles, db
from flask import request


class Roles(Resource):
    def get(self):
        """
        获取角色列表
        """
        try:
            roles = modles.Role.query.all()
            role_list = [role.to_dict() for role in roles]
            return {"status": 200, "msg": "获取角色列表成功", "data": role_list}
        except BaseException as e:
            return {"status": 500, "msg": "获取角色列表失败"}

    def post(self):
        """
        创建角色
        """
        try:
            # 请求服务时是通过applictain/json传递,获取传递数据
            name = request.get_json().get("name")
            desc = request.get_json().get("desc")
            role = modles.Role(name=name, desc=desc)
            # 添加角色实例到数据会话
            db.session.add(role)
            # 提交事务
            db.session.commit()
            return {"status": 200, "msg": "创建角色成功"}
        except BaseException as e:
            return {"status": 500, "msg": "创建角色失败"}


role_api.add_resource(Roles, "/roles/")


class Role(Resource):
    """
    删除角色
    """

    def delete(self, id):
        try:
            role = modles.Role.query.get(id)
            db.session.delete(role)
            db.session.commit()
            return {"status": 200, "msg": "删除角色成功"}
        except BaseException as e:
            return {"status": 404, "msg": "删除角色失败"}

    def put(self, id):
        """
        修改角色
        """
        try:
            role = modles.Role.query.get(id)
            # 创建Request对象，用来接收数据
            parser = reqparse.RequestParser()
            # 添加参数
            parser.add_argument("name", type=str, required=True, help="请输入角色名称")
            parser.add_argument("desc", type=str)
            # 解析参数
            args = parser.parse_args()
            if args.get("name"):
                role.name = args.name
            if args.get("desc"):
                role.desc = args.desc
            db.session.commit()
            return {"status": 200, "msg": "修改角色成功"}
        except BaseException as e:
            print(e)
            return {"status": 500, "msg": "修改角色失败"}


role_api.add_resource(Role, "/role/<int:id>/")


# 删除角色指定权限接口
@roles_bp.route("/role/<int:rid>/<int:mid>/")
def del_menu(rid: int, mid: int):
    # 查找当前的角色信息
    role = modles.Role.query.get(rid)
    # 查找当前的菜单信息
    menu = modles.Menu.query.get(mid)
    # 判断当前角色与菜单是否存在
    if all([role, menu]):
        # 判断当前角色是否有当前菜单
        if menu in role.menus:
            # 删除当前角色的当前菜单
            role.menus.remove(menu)
            if menu.level == 1:
                # 删除当前角色，父菜单的所有子菜单
                '''
                为什么还要另外写删除子菜单的功能，不应该是删除父菜单，子菜单也删除吗？
                因为查询出来的父菜单包括子菜单只是我们定义好的输出，而不是模型里面的删除

                '''
                for temp in menu.children:
                    # 判断当前角色是否有当前子菜单
                    if temp in role.menus:
                        # 删除当前角色的当前子菜单
                        role.menus.remove(temp)
            # 提交到数据库
            db.session.commit()
            return {"status": 200, "msg": "删除角色菜单成功"}
    else:
        return {"status": 500, "msg": "菜单或角色不存在"}
    
@roles_bp.route('/role/<int:rid>/',methods=['POST'])
def set_menu(rid:int):
    try:
        # 获取当前角色信息
        role = modles.Role.query.get(rid)
        # 获取要分配的权限
        mids =request.get_json().get('mids')
        # 清空当前角色的所有权限
        role.menus = []
        # 遍历要分配的权限
        mids = mids.split(',')
        for m in mids:
            if m: #判断m是否为空
                # 获取权限
                menu =modles.Menu.query.get(int(m))
                # 给角色分配权限
                role.menus.append(menu)
            # 保存到数据库
        db.session.commit()
        # 返回结果
        return {'status': 200, 'msg': '分配权限成功'}
    except Exception as e:
        return {'status': 500, 'msg': '分配权限失败'}
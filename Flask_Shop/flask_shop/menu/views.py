from flask_restful import Resource
from flask import request
from flask_shop import modles
from flask_shop.menu import menu_api


class Menus(Resource):
    def get(self):
        # 获取响应格式
        type_ = request.values.get("type_")
        if not type_:
            type_='tree'
        if type_ != "tree":
            # 通过模型获取数据
            menu_list = modles.Menu.query.filter(modles.Menu.level != 0).all()
            menu_data = []
            # 遍历模型数据，转化成json数据
            for i in menu_list:
                menu_data.append(i.to_dict_list())

            return {"status": 200, "msg": "菜单获取成功", "data": menu_data}
        else:
            # 通过模型获取数据
            menu_list = modles.Menu.query.filter(modles.Menu.level == 1).all()
            menu_data = []
            # 遍历模型数据，转化成json数据
            for i in menu_list:
                menu_data.append(i.to_dict_tree())

            return {"status": 200, "msg": "菜单获取成功", "data": menu_data}


menu_api.add_resource(Menus, "/menus/")

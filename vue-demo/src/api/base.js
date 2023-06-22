/**
 * 存放所有网络请求地址
 */
const base = {
    baseUrl: "http://localhost:5000",                //公共地址
    login: '/user/login/',                          //登录地址,
    test_response: '/user/test/',                   //测试response是否好用
    menu_data: '/menu/menus/',                      //获取tree菜单数据
    menulist_data: '/menu/menus/?type_=list',       //获取列表菜单数据
    get_user: '/user/users/',                       //获取用户数据
    get_userby_id: '/user/user/',                   //查询修改用户信息
    update_user_data: '/user/user/',                //更新用户信息
    resetpwd_user: '/user/resetpwd/',
    get_role: '/roles/',                           //获取角色列表数据
    del_role_menu: '/role/',                       //获取角色列表
    set_menudata: '/role/',                        //设置表单
    get_category: '/categorys/',                   //获取分类列表
    add_category: '/categorys/',                  //添加分类
    get_attr_by_category: '/attributes/',      //根据分类获取属性
    add_attr: '/attributes/',                 //添加属性
    update_attr_value: '/attribute/',            //更新属性值
    get_product_list: '/products/',            //获取商品列表
    delete_product: '/product/',               //删除商品
    upload_img: '/upload_img/',                //上传图片
    add_product: '/products/',                 //添加商品
    get_orders: '/orders/',                    //获取订单列表
    get_express: '/expresses/',                //获取物流信息
    get_cate_group: '/cate_grup/',             //获取分类组
}

export default base 
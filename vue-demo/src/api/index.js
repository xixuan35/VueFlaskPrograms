import axios from "../utils/request";
import base from './base'
const api = {
    getLogin(params) {
        return axios.post(base.baseUrl + base.login, params)
    },
    test_response(params) {
        return axios.get(base.baseUrl + base.test_response, params)
    },
    get_menu_data(params) {
        return axios.get(base.baseUrl + base.menu_data, params)
    },
    get_menulist_data(params) {
        return axios.get(base.baseUrl + base.menulist_data, params)
    },
    get_userlist(params) {
        return axios.get(base.baseUrl + base.get_user, params)
    },
    add_userdata(params) {
        return axios.post(base.baseUrl + base.get_user, params)
    },
    get_userby_id(id) {
        return axios.get(base.baseUrl + base.get_userby_id + id + '/')
    },
    upgrade_userinfo(id, params) {
        return axios.put(base.baseUrl + base.update_user_data + id + '/', params)
    },
    delet_userinfo(id) {
        return axios.delete(base.baseUrl + base.update_user_data + id + '/')
    },
    reset_userpwd(id) {
        return axios.get(base.baseUrl + base.resetpwd_user + id + '/')
    },
    get_role_data(params) {
        return axios.get(base.baseUrl + base.get_role, params)
    },
    del_role_menu(rid, mid) {
        return axios.get(base.baseUrl + base.del_role_menu + rid + '/' + mid + '/')
    },
    set_menu(rid, params) {
        return axios.post(base.baseUrl + base.set_menudata + rid + '/', params)
    },
    get_category(level) {
        return axios.get(base.baseUrl + base.get_category + '?level=' + level)
    },
    add_category(params) {
        return axios.post(base.baseUrl + base.add_category, params)
    },
    get_attr_by_category(cid, _type) {
        return axios.get(base.baseUrl + base.get_attr_by_category + '?cid=' + cid + '&_type=' + _type)
    },
    add_attribute(params) {
        return axios.post(base.baseUrl + base.add_attr, params)
    },
    update_attr_value(id, params) {
        return axios.put(base.baseUrl + base.update_attr_value + id + '/', params)
    }, get_product_list(name) {
        if (name) {
            return axios.get(base.baseUrl + base.get_product_list + '?name=' + name)
        } else {
            return axios.get(base.baseUrl + base.get_product_list)
        }
    },
    delete_product(id) {
        return axios.delete(base.baseUrl + base.delete_product + id + '/')
    },
    add_product(params) {
        return axios.post(base.baseUrl + base.add_product, params)
    },
    get_orders(params) {
        return axios.get(base.baseUrl + base.get_orders, params)
    },
    get_express(id) {
        return axios.get(base.baseUrl + base.get_express + id + '/')
    },
    get_category_group() {
        return axios.get(base.baseUrl + base.get_cate_group)
    }
}


export default api
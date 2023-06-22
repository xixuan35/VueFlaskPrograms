<template>
    <div class="common-layout container">
        <el-container class="container">
            <el-header class="header">
                <div class="logo">
                    <img src="../assets/logo1.png" alt="">
                    <span>电商后台管理系统</span>
                </div>
                <div class="user">
                    <el-button @click="logout" type="danger">退出</el-button>
                    <!-- <el-button @click="test">test</el-button> -->
                </div>
            </el-header>
            <el-container>
                <el-aside class="aside">
                    <el-menu active-text-color="#ffd04b" background-color="#001529" class="el-menu-vertical-demo"
                        default-active="2" text-color="#fff" @open="handleOpen" @close="handleClose" unique-opened="true" router="true">
                        <el-sub-menu :index=index v-for="(item, index) in menuslist.menus">
                            <template #title>
                                <el-icon>
                                    <component :is="menuslist.icons[item.id]"></component>
                                </el-icon>
                                <span>{{ item.name }}</span>
                            </template>
                            <el-menu-item :index=childitem.path v-for="childitem in item.children ">{{ childitem.name
                            }}</el-menu-item>
                        </el-sub-menu>
                    </el-menu>
                </el-aside>
                <el-main>
                    <router-view/>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>
<script setup>
import { useRouter } from 'vue-router'
import api from '@/api/index'
import { onMounted, reactive } from 'vue'
const router = useRouter()
const menuslist = reactive({
    menus: [],
    icons: {
        '1':'User',
        '2': 'Setting',
        '3': 'Goods',
        '4': 'ShoppingTrolley',
        '5': 'PieChart'
    }
})
onMounted(() => {
    get_menu()
})
const logout = () => {
    //删除客服端数据，跳转登入页面
    sessionStorage.removeItem('token')
    router.push('/login')
}
const test = () => {
    api.test_response().then(res => {
        console.log(res)
    })
}

const get_menu = () => {
    api.get_menu_data().then(res => {
        console.log(res)
        menuslist.menus = res.data.data
        console.log(menuslist.menus,999999999)
    })
}
</script>

<style scoped>
.container {
    height: 100%;
}

.header {
    background-color: #fff;
    box-shadow: 0 0 5px rgba(0, 0, 0, 3);
    font-size: 20px;
    color: #999;
    height: 50px;
    width: 100%;
}

.logo {
    float: left;
    height: 50px;
    align-items: center;
    display: flex;
    justify-content: center;
}

.logo img {
    width: 50px;
    height: 30px;
    margin-right: 10px;
}

.user {
    float: right;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
}

.aside {
    width: 200px;
    background-color: #001529;
}
</style>
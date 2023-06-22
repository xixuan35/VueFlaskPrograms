<template>
    <!-- 要显示的内容 -->
    <div class="main">
        <div class="login">
            <div class="logo">
                <img src="../assets/logo1.png" alt="">
            </div>
            <el-form :model="user" class="user_form" :rules="userrule" ref="userFormRef">
                <el-form-item prop="name">
                    <el-input v-model="user.name" placeholder="用户名" :prefix-icon="User" />
                </el-form-item>
                <el-form-item prop="pwd">
                    <el-input v-model="user.pwd" placeholder="密码" :prefix-icon="Lock" show-password />
                </el-form-item>
                <el-form-item class="btns">
                    <el-button type="primary" @click="submitform(userFormRef)">登录</el-button>
                    <el-button type="success" @click="restform(userFormRef)">重置密码</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>
<script setup>
import { reactive, ref } from 'vue'
import { Lock, User } from '@element-plus/icons-vue'
import api from '@/api/index'
import { useRouter } from 'vue-router' // 导入路由对象
//
const userFormRef = ref(null)
// 定义表单数据
const user = reactive({
    name: 'baizhan',
    pwd: '123456'
})
// 创建路由对象
const router = useRouter()

// 定义表单规则
const userrule = reactive({
    name: [{ required: true, message: '用户名不能为空', trigger: 'blur' }, {
        min: 3, max: 10, message: '长度在3-10个字符', trigger: 'blur'
    }],
    pwd: [{ required: true, message: '用户名不能为空', trigger: 'blur' }]
})
//定义重置表单方法
const restform = (userFormRef) => {
    userFormRef.resetFields()
}
//定义定义登录
const submitform = (userFormRef) => {
    userFormRef.validate((valid) => {
        if (valid) {
            console.log('验证通过，可以提交')
            api.getLogin(user).then(res => {
                if (res.data.status == 200) {
                    ElMessage({
                        message: res.data.message,
                        type: 'success'
                    })
                    //记录token值，可以通过sessionstorage或者是localhoststoraage
                    sessionStorage.setItem('token',res.data.data.token)
                    console.log('hello')
                    router.push('/')
                    
                } else {
                    ElMessage.error({
                        message: res.data.message,
                        type: 'success'
                    })
                }
            })
        } else {
            console.log('验证失败')
            return false
        }
    })
}
</script>

<style scoped>
.main {
    width: 100%;
    height: 100%;
    background-color: rgb(232, 180, 51);
    display: flex;
    justify-content: center;
    align-items: center;
}

.login {
    width: 450px;
    height: 300px;
    background-color: aliceblue;
    border-radius: 5px;
}

.logo {
    width: 200px;
    border: 1px solid #eee;
    margin: 0 auto;
    margin-top: -65px;
    padding: 5px;
    border-radius: 5px;
    box-shadow: 0 0 10px #ddd;
}

img {
    width: 100%;
    height: 100%;
}

.user_form {
    padding: 50px;
}

.btns {
    display: flex;
    justify-content: space-between;
}

.btns button {
    flex: 1;
}
</style>

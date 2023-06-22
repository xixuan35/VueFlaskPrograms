<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">home</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row :gutter="12">
            <el-col :span="8">
                <el-input v-model="userlisttable.query_data" placeholder="输入要搜索的账号" class="input-with-select">
                    <template #append>
                        <el-button :icon="Search" @click="usersearch" />
                    </template>
                </el-input>
            </el-col>
            <el-col :span="1">
                <el-button type="primary" :icon="CirclePlus" @click="dialogFormVisible = true">增加用户</el-button>
            </el-col>
        </el-row>
        <el-row>
            <el-table :data="userlisttable.tableData" stripe class="table">
                <el-table-column prop="id" label="id" width="50" />
                <el-table-column prop="name" label="账号" width="100" />
                <el-table-column prop="nick_name" label="昵称" width="100" />
                <el-table-column prop="phone" label="手机号" width="150" />
                <el-table-column prop="email" label="邮箱" width="150" />
                <el-table-column prop="role" label="角色" width="150" />
                <el-table-column label="操作" width="240">
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
                        <el-button size="small" type="danger"
                            @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
                        <el-button size="small" type="success"
                            @click="handleReset(scope.$index, scope.row)">Reset</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
        <el-pagination v-model:current-page="userlisttable.pNum" v-model:page-size="userlisttable.pageSize"
            :page-sizes="pageSize" :small="small" :disabled="disabled" :background="background"
            layout="total, sizes, prev, pager, next, jumper" :total="userlisttable.total" @size-change="handleSizeChange"
            @current-change="handleCurrentChange" class="table" />
    </el-card>
    <!-- 增加用户对话框 -->
    <el-dialog v-model="dialogFormVisible" title="添加用户" :before-close="userFormreset">
        <el-form :model="user_form" :rules="userform_rule" ref="dialog_userform">
            <el-form-item label="用户名" :label-width="formLabelWidth" prop="name">
                <el-input v-model="user_form.name" autocomplete="off" />
            </el-form-item>
            <el-form-item label="密码" :label-width="formLabelWidth" prop="pwd">
                <el-input v-model="user_form.pwd" autocomplete="off" />
            </el-form-item>
            <el-form-item label="确认密码" :label-width="formLabelWidth" prop="real_pwd">
                <el-input v-model="user_form.real_pwd" autocomplete="off" />
            </el-form-item>
            <el-form-item label="昵称" :label-width="formLabelWidth" prop="nick_name">
                <el-input v-model="user_form.nick_name" autocomplete="off" />
            </el-form-item>
            <el-form-item label="手机号" :label-width="formLabelWidth" prop="phone">
                <el-input v-model="user_form.phone" autocomplete="off" />
            </el-form-item>
            <el-form-item label="邮箱" :label-width="formLabelWidth" prop="email">
                <el-input v-model="user_form.email" autocomplete="off" />
            </el-form-item>
            <el-form-item label="角色">
                <el-select v-model="user_form.role_id" placeholder="">
                    <el-option :label="item.name" :value="item.id" v-for="item in rolemenulist" :key="item.id" />
                </el-select>
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="userFormreset">Cancel</el-button>
                <el-button type="primary" @click="add_user(dialog_userform)">
                    Confirm
                </el-button>
            </span>
        </template>
    </el-dialog>
    <!-- 修改用户对话框 -->
    <el-dialog v-model="editdialogFormVisible" title="修改数据">
        <el-form :model="edituser_form" ref="editdialog_userform">
            <el-form-item label="用户名" :label-width="formLabelWidth" prop="name">
                <el-input v-model="edituser_form.name" autocomplete="off" disabled />
            </el-form-item>
            <el-form-item label="昵称" :label-width="formLabelWidth" prop="nick_name">
                <el-input v-model="edituser_form.nick_name" autocomplete="off" />
            </el-form-item>
            <el-form-item label="手机号" :label-width="formLabelWidth" prop="phone">
                <el-input v-model="edituser_form.phone" autocomplete="off" />
            </el-form-item>
            <el-form-item label="邮箱" :label-width="formLabelWidth" prop="email">
                <el-input v-model="edituser_form.email" autocomplete="off" />
            </el-form-item>
            <el-form-item label="角色">
                <el-select v-model="edituser_form.role_id" placeholder="please select your zone">
                    <el-option :label="item.name" :value="item.id" v-for="item in rolemenulist" :key="item.id" />
                </el-select>
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="editdialogFormVisible = false">Cancel</el-button>
                <el-button type="primary" @click="editadd_user(edituser_form)">
                    Confirm
                </el-button>
            </span>
        </template>
    </el-dialog>
    <!-- 删除用户对话框 -->
    <el-dialog v-model="deletdialogFormVisible" title="修改数据">
        <span>确认删除用户{{ userid }}:{{ deletuser }}:{{ deletuser_nickname }}</span>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="deletdialogFormVisible = false">Cancel</el-button>
                <el-button type="primary" @click="delet_user">
                    Confirm
                </el-button>
            </span>
        </template>
    </el-dialog>
    <!-- 重置密码对话框 -->
    <el-dialog v-model="resetdialogFormVisible" title="修改数据">
        <span>确认删除用户{{ userid }}:{{ resetuser }}:{{ resetuser_nickname }}</span>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="resetdialogFormVisible = false">Cancel</el-button>
                <el-button type="primary" @click="reset_user">
                    Confirm
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import { reactive, onMounted, ref } from 'vue'
import { ArrowRight, Search, CirclePlus } from '@element-plus/icons-vue'
import api from '../api/index'
import axios from 'axios';
//用ref定义的变量，修改，要用变量名.valuexiug,否者可能会报错-----Assignment to constant variable.
const formLabelWidth = '80px'
const dialogFormVisible = ref(false)
const small = ref(false)
const background = ref(false)
const disabled = ref(false)
const dialog_userform = ref(null)
const editdialogFormVisible = ref(false)
const editdialog_userform = ref(null)
const deletdialogFormVisible = ref(false)
const resetdialogFormVisible = ref(false)
let pageSize = [1, 2, 5, 10]
let userid = ref(1)
let deletuser = ref('')
let deletuser_nickname = ref('')
let resetuser = ref('')
let resetuser_nickname = ref('')
let rolemenulist = ref([])
const userlisttable = reactive({
    tableData: [],
    pNum: 1,
    pageSize: 1,
    total: 0,
    query_data: ''
}
)
const user_form = reactive({
    name: '',
    pwd: null,
    real_pwd: null,
    nick_name: null,
    phone: null,
    email: null,
    role_id:null
})
let edituser_form = reactive({
    name: '',
    nick_name: null,
    phone: null,
    email: null,
    role_id: null
})
//编辑用户
const handleEdit = (index, row) => {
    userid.value = row.id
    editdialogFormVisible.value = true
    // edituser_form=row//直接将数据赋值到表单上
    api.get_userby_id(row.id).then(res => {
        console.log(res.data)
        edituser_form.name = res.data.data.name
        edituser_form.nick_name = res.data.data.nick_name
        edituser_form.phone = res.data.data.phone
        edituser_form.email = res.data.data.email
        edituser_form.role_id = res.data.data.role_id
    })

}
const validatePass2 = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请输入确认密码'))
    } else if (value !== user_form.pwd) {
        callback(new Error("两次密码不一致"))
    } else {
        callback()
    }
}
const validatePass3 = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请输入手机号'))
    } else if (!/^1[3456789]\d{9}$/i.test(value)) {
        callback(new Error("手机号格式错误"))
    } else {
        callback()
    }
}
const validatePass4 = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请输入邮箱'))
    } else if (!/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-z0-9_-])+/i.test(value)) {
        callback(new Error("邮箱格式错误"))
    } else {
        callback()
    }
}
//用来校验用户表单数据
const userform_rule = reactive({
    name: [{ required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 5, message: '用户名长度为 3 ——— 5', trigger: 'blur' }],
    pwd: [{ required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 10, message: '密码长度为 3 ——— 10', trigger: 'blur' }],
    real_pwd: [{ required: true, message: "请输入确认密码", trigger: 'blur' }, { validator: validatePass2, trigger: 'blur' }],
    nick_name: [{ required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 1, max: 5, message: '昵称长度为 1——— 5', trigger: 'blur' }],
    phone: [{ validator: validatePass3, trigger: 'blur' }],
    email: [{ validator: validatePass4, trigger: 'blur' }]
})

onMounted(() => {
    getUserlist()
    get_rolelist()
})
//获取角色列表
const get_rolelist = () => {
    api.get_role_data().then(res => {
        rolemenulist.value = res.data.data
    })
}
//获取用户列表
const getUserlist = () => {
    let params = { 'pnum': userlisttable.pNum, 'psize': userlisttable.pageSize, 'name': userlisttable.query_data }
    api.get_userlist({ params }).then(res => {
        console.log(res.data.data.data)
        //更新用户列表数据
        userlisttable.tableData = res.data.data.data;
        //更新分页数据总数
        userlisttable.total = res.data.data.total
    })
}
const handleSizeChange = (val) => {
    console.log(val, 11)
    //修改每页显示多少条数据
    userlisttable.pageSize = val
    //重新获取用户列表数据
    getUserlist()
}
const handleCurrentChange = (val) => {
    console.log(val)
    //修改显示第几页数据
    userlisttable.pNum = val
    //重新获取用户列表数据
    getUserlist()
}
//搜索用户功能
const usersearch = () => {
    //初始化页数
    userlisttable.pNum = 1
    getUserlist()
}
// const edituserFormreset = () => {
//     //重置表单数据
//     editdialog_userform.value.resetFields()
//     //关闭对话框
//     editdialogFormVisible.value = false


// }
const userFormreset = () => {
    //重置表单数据
    dialog_userform.value.resetFields()
    //关闭对话框
    dialogFormVisible.value = false


}
//添加用户
const add_user = (userFormRef) => {
    userFormRef.validate((valid) => {
        if (valid) {
            console.log('验证通过，可以提交')
            api.add_userdata(user_form).then(res => {
                if (res.data.status == 200) {
                    ElMessage({
                        message: res.data.message,
                        type: 'success'
                    });
                    //注册成功，重置表单数据和重新获取数据库数据
                    getUserlist()
                    userFormreset()

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
//确认修改用户信息
const editadd_user = (edituser_form) => {
    api.upgrade_userinfo(userid.value, edituser_form).then(res => {
        if (res.data.status == 200) {
            ElMessage({
                message: res.data.message,
                type: 'success'
            });
            //注册成功，重置表单数据
            getUserlist()
            editdialogFormVisible.value = false

        } else {
            ElMessage.error({
                message: res.data.message,
                type: 'success'
            })
        }
    })
}
//删除用户按钮
const handleDelete = (index, row) => {
    userid.value = row.id
    deletuser.value = row.name
    deletuser_nickname.value = row.nick_name
    deletdialogFormVisible.value = true
}
//确认删除用户
const delet_user = () => {
    api.delet_userinfo(userid.value).then(res => {
        if (res.status == 200) {
            ElMessage({
                message: res.data.message,
                type: 'success'
            });
            //注册成功，重置表单数据
            getUserlist()
            deletdialogFormVisible.value = false

        } else {
            ElMessage.error({
                message: res.data.message,
                type: 'success'
            })
        }
    })
}
//重置密码操作
const handleReset = (index, row) => {
    userid.value = row.id
    resetuser.value = row.name
    resetuser_nickname.value = row.nick_name
    resetdialogFormVisible.value = true
}
//确认重置密码
const reset_user = () => {
    api.reset_userpwd(userid.value).then(res => {
        if (res.data.status == 200) {
            console.log(res)
            ElMessage({
                message: res.data.message,
                type: 'success'
            });
            //注册成功，重置表单数据
            getUserlist()
            resetdialogFormVisible.value = false

        } else {
            ElMessage.error({
                message: res.data.message,
                type: 'success'
            })
        }
    })
}
</script>
<style scoped>
.box-card {
    margin-top: 20px;
}

.table {
    margin-top: 10px;
}
</style>


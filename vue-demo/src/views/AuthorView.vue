<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">home</el-breadcrumb-item>
        <el-breadcrumb-item>权限管理</el-breadcrumb-item>
        <el-breadcrumb-item>角色列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-col :span="1">
            <el-button type="primary" :icon="CirclePlus">增加用户</el-button>
        </el-col>
        <el-row>
            <el-table :data="tableData.rolelist" stripe class="table">
                <el-table-column type="expand">
                    <template #default="scope">
                        <el-row v-for="(m, i) in scope.row.menus" :key="m.id"
                            :class="['padding-l100 bottom', i === 0 ? 'top' : '']">
                            <el-col :span="2"><el-tag class="margin-t10" closable @click="removeMenu(scope.row, m.id)">{{
                                m.name }}</el-tag></el-col>
                            <el-col :span="1"><el-icon class="margin-t15">
                                    <CaretRight />
                                </el-icon></el-col>
                            <el-col :span="21"><el-tag class="margin-t10" v-for="cm in m.children" :key="cm.id"
                                    type="success" closable @click="removeMenu(scope.row, cm.id)">{{ cm.name
                                    }}</el-tag></el-col>
                        </el-row>
                    </template>
                </el-table-column>
                <el-table-column prop="id" label="id" />
                <el-table-column prop="name" label="名称" />
                <el-table-column prop="desc" label="详情" />
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button size="small">编辑</el-button>
                        <el-button size="mini" type="success" @click="showMenuDialog(scope.row)">分配权限</el-button>
                        <el-button size="mini" type="danger">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
    </el-card>
    <el-dialog v-model="menuDialogVisible" title="分配权限" width="40%" :before-close="handleClose">
        <el-tree show-checkbox :data="menuList" :props="menuProps" @node-click="handleNodeClick" node-key="id" ref="treeRef"
            default-expand-all="true" />
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="menuDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="sumbitMenu">确定</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import { ArrowRight, CirclePlus } from '@element-plus/icons-vue'
import api from '@/api/index'
import { ref, reactive, onMounted, nextTick } from "vue"
let menuDialogVisible = ref(false)
let menuList = reactive([])
let keyList = reactive([])
let rid = ref(null)
const treeRef = ref(null)
const menuProps = {
    children: 'children',
    label: 'name',
}
const tableData = reactive({
    rolelist: []
})


onMounted(() => {
    get_roledata()
    getMenuList()
})
//获取角色列表数据
const get_roledata = () => {
    api.get_role_data().then(res => {
        tableData.rolelist = res.data.data
    })
}

// 删除角色权限
const removeMenu = (row, mid) => {
    console.log(row.id, mid)
    ElMessageBox.confirm(
        '确实要删除该角色的权限吗？',
        '提示',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        })

        .then(() => {
            api.del_role_menu(row.id, mid).then(res => {
                ElMessage({
                    type: 'success',
                    message: '删除成功!',
                })
                get_roledata()
            })
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '已取消删除'
            })
        })
}

const showMenuDialog = (row) => {
    menuDialogVisible.value = true
    // 初始化选中的菜单id
    keyList = []
    // 获取1级菜单
    row.menus.forEach(item => {
        // 获取2级菜单
        item.children.forEach(citem => {
            //记录选中的菜单id
            keyList.push(citem.id)
        })
    });
    // console.log(keyList)
    // 给树结构设置默认选中
    nextTick(() => { //当前dom渲染完成后执行

        treeRef.value.setCheckedKeys(keyList)
    })
    // 给角色id赋值
    rid.value = row.id
}
const getMenuList = () => {
    api.get_menu_data().then(res => {
        menuList = res.data.data
    })
}
const sumbitMenu = () => {
    // 获取菜单的ID
    let mids = [
        treeRef.value.getCheckedKeys(),
        treeRef.value.getHalfCheckedKeys()
    ]
    mids = mids.join(',')
    // 获取角色ID
    // console.log(rid.value)
    // 提交数据
    api.set_menu(rid.value, { 'mids': mids }).then(res => {
        // console.log(res.data)
        get_roledata()
        menuDialogVisible.value = false
    })
}
</script>

<style scoped>
.box-card {
    margin-top: 20px;
}

.padding-l100 {
    padding-left: 100px;
}

.top {
    border-top: 1px solid #eee;
}

.bottom {
    border-bottom: 1px solid #eee;
}

.margin-t10 {
    margin: 10px;
}

.margin-t15 {
    margin-top: 15px;
}
</style>
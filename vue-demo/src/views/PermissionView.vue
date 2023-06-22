<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">home</el-breadcrumb-item>
        <el-breadcrumb-item>权限管理</el-breadcrumb-item>
        <el-breadcrumb-item>权限列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row>
            <el-table :data="tableData.menu" stripe class="table">
                <el-table-column prop="id" label="id" />
                <el-table-column prop="name" label="名字" />
                <el-table-column prop="path" label="路径" />
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-tag class="ml-2" type="success" v-if="scope.row.level == 1">一级</el-tag>
                        <el-tag class="ml-2" type="info" v-else>二级</el-tag>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
    </el-card>
</template>
<script setup>
import api from '@/api';
import { ArrowRight } from '@element-plus/icons-vue'
import { ref, reactive, onMounted } from 'vue'

let tableData = reactive({
    menu: [{ id: 1, name: 'baizhan', path: '/menu/python', level: 1 }, { id: 2, name: 'heima', path: '/menu/java', level: 2 }]
})

onMounted(() => {
    get_menulist_data()
})
const get_menulist_data = () => {
    api.get_menulist_data().then(res => {
        tableData.menu=res.data.data
    })
}
</script>

<style scoped>
.box-card {
    margin-top: 20px;
}
</style>
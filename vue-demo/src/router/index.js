import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/',
    name: 'home',
    component: HomeView,
    redirect: '/welcome',
    children: [
      {
        path: '/welcome',
        name: 'welcome',
        component: () => import('../views/WelComeView.vue')

      },
      {
        path: "/user_list",
        name: 'user_list',
        component: () => import('../views/UserView.vue')
      },
      {
        path: '/role_list',
        name: 'role_list',
        component: () => import('../views/PermissionView.vue')
      },
      {
        path: '/author_list',
        name: 'author_list',
        component: () => import('../views/AuthorView.vue')
      },
      {
        path: '/group_list',
        name: 'group_list',
        component: () => import('../views/GroupView.vue')
      }, {
        path: '/attribute_list',
        name: 'attribute_list',
        component: () => import('../views/AttributeView.vue')
      },
      {
        path: '/product_list',
        name: 'product_list',
        component: () => import('../views/ProductView.vue')
      }, {
        path: '/add_product',
        name: 'add_product',
        component: () => import('../views/AddProductView.vue')
      },
      {
        path: '/order_list',
        name: 'order_list',
        component: () => import('../views/OrderView.vue')
      },
      {
        path:'/data_list',
        name:'data_list',
        component:()=>import('../views/DataView.vue')
      }
    ]
  }
]


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
export default router
// 做router跳转的login_required验证
router.beforeEach((to, from, next) => {
  if (to.path === '/login') {
    next()
  } else {
    // 获取token值
    const token = sessionStorage.getItem('token')
    if (!token) {
      next('/login')
    }
    next()
  }
})


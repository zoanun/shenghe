import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    // mode: 'history',
    routes: [
        {
            path: '/',
            redirect: '/dashboard'
        },
        {
            path: '/',
            component: () => import('@/components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                {
                    path: '/dashboard',
                    component: () => import('@/components/page/Dashboard.vue'),
                    meta: { title: '系统首页' }
                },
                {
                    path: '/404',
                    component: () => import('@/components/common/404.vue'),
                    meta: { title: '404' }
                },
                {
                    path: '/403',
                    component: () => import('@/components/common/403.vue'),
                    meta: { title: '403' }
                },
                {
                    path: '/nsim', // National Standard Item Management
                    component: () => import('@/components/bodyExam/nsim.vue'),
                    meta: { title: '国标项目管理' }
                },
                {
                    path: '/nsde', // National standard data entry
                    component: () => import('@/components/bodyExam/nsde.vue'),
                    meta: { title: '国标数据录入' }
                },
                {
                    path: '/iss', // Item scoring standards
                    component: () => import('@/components/bodyExam/iss.vue'),
                    meta: { title: '项目打分标准' }
                }, {
                    path: '/nme', // Non-member entry
                    component: () => import('@/components/bodyExam/nme.vue'),
                    meta: { title: '非会员录入' }
                }, {
                    path: '/me', // Member entry
                    component: () => import('@/components/bodyExam/me.vue'),
                    meta: { title: '会员录入' }
                }
            ]
        },
        {
            path: '/login',
            component: () => import('@/components/page/Login.vue'),
            meta: { title: '登录' }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
});

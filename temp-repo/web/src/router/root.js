// 路由表
const constantRouterMap = [

    {
        path: '/',
        redirect: '/admin',
    },
    {
        path: '/adminLogin',
        name: 'adminLogin',
        component: () => import('/@/views/admin-login.vue'),
    },
    {
        path: '/adminRegister',
        name: 'adminRegister',
        component: () => import('/@/views/admin-register.vue'),
    },
    {
        path: '/admin',
        name: 'admin',
        redirect: '/admin/index',
        component: () => import('/@/views/main.vue'),
        children: [
            {path: 'thing', name: 'thing', component: () => import('/@/views/thing.vue')},
            {path: 'user', name: 'user', component: () => import('/@/views/user.vue')},
            {path: 'classification', name: 'classification', component: () => import('/@/views/classification.vue')},
            {path: 'loginLog', name: 'loginLog', component: () => import('/@/views/login-log.vue')},
            {path: 'opLog', name: 'opLog', component: () => import('/@/views/op-log.vue')},
            {path: 'errorLog', name: 'errorLog', component: () => import('/@/views/error-log.vue')},
            {path: 'courseinfo', name: 'courseinfo', component: () => import('/@/views/course-info.vue')},
            {path: 'score', name: 'score', component: () => import('/@/views/score.vue')},
            {path: 'active', name: 'active', component: () => import('/@/views/active.vue')},
            {path: 'jingju', name: 'jingju', component: () => import('/@/views/jingju.vue')},
            {path: 'getjingju', name: 'getjingju', component: () => import('/@/views/getjingju.vue')},
            {path: 'returnjingju', name: 'returnjingju', component: () => import('/@/views/returnjingju.vue')},
            {path: 'index', name: 'index', component: () => import('/@/views/index.vue')},
            {path: 'airline', name: 'airline', component: () => import('/@/views/airline.vue')},
            {path: 'diaodu', name: 'diaodu', component: () => import('/@/views/diaodu.vue')},
            {path: 'baoxiu', name: 'baoxiu', component: () => import('/@/views/baoxiu.vue')},
            {path: 'jingjucabinet', name: 'jingjucabinet', component: () => import('/@/views/jingjucabinet.vue')},
            {path:'adminreturnjingju', name:'adminreturnjingju', component: () => import('/@/views/adminreturnjingju.vue')},
        ]
    },
];

export default constantRouterMap;

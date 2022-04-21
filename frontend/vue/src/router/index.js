import { createRouter, createWebHistory } from 'vue-router'

const site_name = '神野研ポータル';

const routes = [
  {
    path: '/',
    component: () => import('../views/Home.vue'),
    meta: { title: 'トップページ' }
  },
  {
    path: '/user-login',
    component: () => import('../views/UserLogin.vue'),
    meta: { title: 'ログイン' }
  },
  {
    path: '/add-user',
    component: () => import('../views/AddUser.vue'),
    meta: { title: 'ユーザ登録' }
  },
  {
    path: '/user-menu',
    component: () => import('../views/UserMenu.vue'),
    meta: { title: 'ユーザメニュー' }
  },
  {
    path: '/tcu-portal',
    component: () => import('../views/TcuPortal.vue'),
    meta: { title: '大学ポータル' }
  },
  {
    path: '/schedule',
    component: () => import('../views/Schedule.vue'),
    meta: { title: 'スケジュール' }
  },
  {
    path: '/server',
    component: () => import('../views/Server.vue'),
    meta: { title: 'サーバ' }
  },
  {
    path: '/labo-members',
    component: () => import('../views/LaboMembers.vue'),
    meta: { title: '研究室名簿' }
  },
  {
    path: '/tcu-members',
    component: () => import('../views/TcuMembers.vue'),
    meta: { title: '全学名簿' }
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});
router.afterEach((to, from) => {
  document.title = to.meta.title + '｜' + site_name;
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }       
    },
    {
      path: '/migrations',
      name: 'migrations',
      component: () => import('../views/MigrationView.vue'),
      meta: { requiresAuth: true }      
    },
    {
      path: '/migrations/:migrationId',
      name: 'migrationsDetails',
      component: () => import('../components/MigrationListDetails.vue'),
      meta: { requiresAuth: true },
      props: true   
    },    
    {
      path: '/migrations/config',
      name: 'migrationsConfig',
      component: () => import('../views/MigrationConfigView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },    
    {
      path: '/migrations/config/create',
      name: 'migrationsConfigCreate',
      component: () => import('../views/MigrationConfigFormView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/migrations/config/edit/:configId',
      name: 'migrationsConfigEdit',
      component: () => import('../views/MigrationConfigEditView.vue'),
      props: true,
      meta: { requiresAuth: true, requiresAdmin: true }
    },        
    {
      path: '/repository',
      name: 'repository',
      component: () => import('../views/RepositoryView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/repository/create',
      name: 'repositoryCreate',
      component: () => import('../views/RepositoryFormView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/repository/edit/:repoId',
      name: 'repositoryEdit',
      component: () => import('../views/RepositoryEditView.vue'),
      props: true,
      meta: { requiresAuth: true, requiresAdmin: true }
    },    
    {
      path: '/users',
      name: 'users',
      component: () => import('../views/UsersView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/users/create',
      name: 'usersCreate',
      component: () => import('../views/UsersFormView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },  
    {
      path: '/users/edit/:userId',
      name: 'usersEdit',
      component: () => import('../views/UsersEditView.vue'),
      props: true,
      meta: { requiresAuth: true, requiresAdmin: true }
    },      
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    }                
  ]
})

router.beforeEach((to, from, next) => {
  const userRole = localStorage.getItem('role');
  
  if (to.meta.requiresAuth && userRole == null) {
    next({ name: 'login'});
  } else {
    if (to.meta.requiresAdmin && userRole !== 'Admin') {
      next({ name: 'home' });
    } else {
      next();
    }
  }

});

export default router

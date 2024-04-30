<template>
  <header>
      <nav>
        <ul class="nav-links" v-if="isLoggedIn">
          <li class="center"><RouterLink to="/">Home</RouterLink></li>
          <li class="forward" v-if="role === 'Admin'"><RouterLink to="/repository">Repository List</RouterLink></li>
          <li class="forward" v-if="role === 'Admin'"><RouterLink to="/migrations/config">Migration Config</RouterLink></li>
          <li class="forward" ><RouterLink to="/migrations">Migration History</RouterLink></li>
          <li class="forward"v-if="role === 'Admin'"><RouterLink to="/users">Users</RouterLink></li>
          <li class="forward" @click="logout">Logout</li>
        </ul>
      </nav>
  </header>
  </template>
  
  <script>
  import { RouterLink, RouterView } from 'vue-router'

  export default {
    data() {
      return {
        role: ''
      };
    },
    mounted() {
      this.role = localStorage.getItem('role');
    },
    computed: {
      isLoggedIn() {
        return localStorage.getItem('role') !== null;
      }
    },    
    methods: {
      logout() {
      localStorage.removeItem('role');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('fullname');
      
      window.location.href = '/login';
    }
    }
  };
  </script>
  
  <style scoped>
  .nav-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: #f0f0f0;
  }
  
  .nav-item {
    cursor: pointer;
  }
  
  .dropdown {
    position: relative;
  }
  
  .dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: #fff;
    border: 1px solid #ccc;
    padding: 5px;
    display: none;
  }
  
  .dropdown-menu span {
    display: block;
    cursor: pointer;
  }
  
  .dropdown-menu span:hover {
    background-color: #f0f0f0;
  }
  
  .show {
    display: block;
  }
  </style>
  
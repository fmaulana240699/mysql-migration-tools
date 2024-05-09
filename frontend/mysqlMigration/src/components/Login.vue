<template>
    <div class="form-mid">
      <h1>Login Form</h1>
      
      <form @submit.prevent="handleSubmit">
        
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="formData.username" placeholder="Username" required />
        </div>
        
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="formData.password" placeholder="Password" required />
        </div>

        <button type="submit" class="button-84">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import axiosLoginInstance from '@/config/axiosConfig';

  
  
  export default {
    name: 'FormComponent',
    setup() {
      const formData = ref({
        username: '',
        password: ''
      });
  
      const handleSubmit = async () => {
        if (validateForm()) {
          try {
            const response = await axiosLoginInstance.post(`/login/`, formData.value);

            // const fullname = response.data['user']['fullname']
            const username = response.data['user']['username']
            const role = response.data['user']['role']
            const accessToken = response.data['access']

  
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('username', username);
            localStorage.setItem('role', role);
            window.location.href = '/';

          } catch (error) {
            console.error('Error submitting form:', error);
          }
        } else {
          alert('Please fill in all fields.');
        }
      };
  
      const validateForm = () => {
        return (
          formData.value.username &&
          formData.value.password
        );
      };
  
      return {
        formData,
        handleSubmit,
      };
    },
  };
  </script>
  
  <style>
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  </style>
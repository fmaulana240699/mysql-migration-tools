<template>
    <div class="form-mid">
      <h1>Add New Repo Integration</h1>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="formData.name" placeholder="Name" required />
        </div>
        
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="formData.username" placeholder="Username" required />
        </div>
        
        <div class="form-group">
          <label for="token">Token:</label>
          <input type="password" id="token" v-model="formData.token" placeholder="Token" required />
        </div>  
        
        <div class="form-group">
          <label for="branch">Branch:</label>
          <input type="text" id="branch" v-model="formData.branch" placeholder="Branch Name" required />
        </div>        
        
        <div class="form-group">
          <label for="repo_url">Repository URL:</label>
          <input type="text" id="repo_url" v-model="formData.repo_url" placeholder="Repo URL" required />
        </div>
        
        <button type="submit" class="button-84">Submit</button>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import axiosInstance from '@/config/axiosConfig';
  
  export default {
    name: 'FormComponent',
    setup() {
      const author = localStorage.getItem('username');
      const formData = ref({
        name: '',
        username: '',
        token: '',
        branch: '',
        repo_url: '',
        author: author
      });
  
      const handleSubmit = async () => {
        if (validateForm()) {
          try {
            const response = await axiosInstance.post(`/repo/`, formData.value);
            console.log('Form submitted:', response.data);
            window.location.href = '/repository';
          } catch (error) {
            console.error('Error submitting form:', error);
          }
        } else {
          alert('Please fill in all fields.');
        }
      };
  
      const validateForm = () => {
        return (
          formData.value.name &&
          formData.value.username &&
          formData.value.token &&
          formData.value.branch &&
          formData.value.repo_url
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
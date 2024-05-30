<template>
    <div class="form-mid">
      <h1>Add New Repo Integration</h1>

      <div v-if="showAlert" class="alert">
        <span class="closebtn" @click="closeAlert">&times;</span> 
        <strong>Oops!</strong> {{ alertMessage }}
      </div>
      
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

      const showAlert = ref(false);
      const alertMessage = ref('');
  
      const handleSubmit = async () => {
        if (validateForm()) {
          try {
            const response = await axiosInstance.post(`/repo/`, formData.value);
            if (response.status === 200) {
              // console.log('Form submitted:', response.data);
              window.location.href = '/repository';
            } else {
              handleResponseError(response);
            }
          } catch (error) {
            console.error('Error submitting form:', error);
            handleAxiosError(error);
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

      const handleAxiosError = (error) => {
      if (error.response) {
        alertMessage.value = `Error submitting form: ${error.response.status} ${error.response.data.message || error.response.statusText}`;
      } else {
        alertMessage.value = `Error submitting form: ${error.message}`;
      }
      showAlert.value = true;
      };

      const handleResponseError = (response) => {
        alertMessage.value = `Error: ${response.status} ${response.statusText}`;
        showAlert.value = true;
      };

      const closeAlert = () => {
        showAlert.value = false;
        alertMessage.value = '';
      };
  
      return {
        formData,
        handleSubmit,
        showAlert,
        alertMessage,        
        closeAlert,
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
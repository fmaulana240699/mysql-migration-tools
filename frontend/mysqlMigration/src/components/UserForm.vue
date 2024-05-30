<template>
    <div class="form-mid">
      <h1>Add New User</h1>

      <div v-if="showAlert" class="alert">
        <span class="closebtn" @click="closeAlert">&times;</span> 
        <strong>Oops!</strong> {{ alertMessage }}
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="fullname">Fullname:</label>
          <input type="text" id="fullname" v-model="formData.fullname" placeholder="fullname" required />
        </div>
        
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="formData.username" placeholder="Username" required />
        </div>
        
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="formData.password" placeholder="password" required />
        </div>
        
        <div class="form-group">
          <label for="role">Role:</label>
          <input type="text" id="role" v-model="formData.role" placeholder="Role User" required />
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
      const formData = ref({
        fullname: '',
        username: '',
        password: '',
        role: '',
      });

      const showAlert = ref(false);
      const alertMessage = ref('');
  
      const handleSubmit = async () => {
        if (validateForm()) {
          try {
            const response = await axiosInstance.post(`/register/`, formData.value);
            if (response.status === 200) {
              // console.log('Form submitted:', response.data);
              window.location.href = '/users';
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
          formData.value.fullname &&
          formData.value.username &&
          formData.value.password &&
          formData.value.role
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
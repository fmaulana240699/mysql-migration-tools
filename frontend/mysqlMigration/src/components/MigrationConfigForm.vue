<template>
    <div class="form-mid">
      <h1>Add New Migration Config</h1>

      <div v-if="showAlert" class="alert">
        <span class="closebtn" @click="closeAlert">&times;</span> 
        <strong>Oops!</strong> {{ alertMessage }}
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="folder_location">Folder Location :</label>
          <input type="text" id="folder_location" v-model="formData.folder_location" placeholder="Folder Location" required />
        </div>
        
        <div class="form-group">
          <label for="db_host">Database Host :</label>
          <input type="text" id="db_host" v-model="formData.db_host" placeholder="Database Host" required />
        </div>
        
        <div class="form-group">
          <label for="db_user">Database Username :</label>
          <input type="text" id="db_user" v-model="formData.db_user" placeholder="Database Username" required />
        </div>
        
        <div class="form-group">
          <label for="db_name">Database Name :</label>
          <input type="text" id="db_name" v-model="formData.db_name" placeholder="Database Name" required />
        </div>

        <div class="form-group">
          <label for="db_password">Database Password :</label>
          <input type="password" id="db_password" v-model="formData.db_password" placeholder="Database Password" required />
        </div>    
        
        <div class="form-group">
          <label for="id_repo">Repo :</label>
          <select v-model="formData.id_repo">
            <option v-for="repo in repoList" :key="repo.id" :value="repo.id"> {{ repo.name }}</option>
          </select>
        </div>          
        
        <button type="submit" class="button-84">Submit</button>
      </form>
    </div>
  </template>
  
  <script>
import { ref, onMounted } from 'vue';
import axiosInstance from '@/config/axiosConfig';

export default {
  name: 'FormComponent',
  setup() {
    const author = localStorage.getItem('username');
    const repoList = ref([]);
    const formData = ref({
      folder_location: '',
      db_host: '',
      db_user: '',
      db_name: '',
      db_password: '',
      id_repo: '',
      author: author
    });

    const showAlert = ref(false);
    const alertMessage = ref('');

    const fetchRepos = async () => {
      try {
        const response = await axiosInstance.get(`/repo/`);
        repoList.value = response.data;
      } catch (error) {
        console.error("Error fetching repos:", error);
        alertMessage.value = 'Error fetching repos: ' + error.message;
        showAlert.value = true;
      }
    };

    const handleSubmit = async () => {
      if (validateForm()) {
        try {
          const response = await axiosInstance.post(`/migration/config/`, formData.value);
          if (response.status === 200) {
            // console.log('Form submitted:', response.data);
            window.location.href = '/migrations/config';
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
        formData.value.folder_location &&
        formData.value.db_host &&
        formData.value.db_user &&
        formData.value.db_name &&
        formData.value.db_password &&
        formData.value.id_repo
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

    onMounted(() => {
      fetchRepos();  // Fetch repos when the component is mounted
    });

    return {
      formData,
      repoList,
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
<template>
  <div class="form-mid">
    <h1>Update Migration Config</h1>
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="folder_location">Folder Location :</label>
        <input type="text" id="folder_location" v-model="formData.folder_location" required />
      </div>
      
      <div class="form-group">
        <label for="db_host">Database Host :</label>
        <input type="text" id="db_host" v-model="formData.db_host" required />
      </div>
      
      <div class="form-group">
        <label for="db_user">Database Username :</label>
        <input type="text" id="db_user" v-model="formData.db_user" required />
      </div>
      
      <div class="form-group">
        <label for="db_name">Database Name :</label>
        <input type="text" id="db_name" v-model="formData.db_name" required />
      </div>

      <div class="form-group">
        <label for="db_password">Database Password :</label>
        <input type="password" id="db_password" required />
      </div>    
      
      <div class="form-group">
        <label for="id_repo">Repo :</label>
        <input type="text" id="id_repo" v-model="formData.id_repo" required />
      </div>          
      
      <button type="submit" class="button-84">Submit</button>
    </form>
  </div>
</template>

<script>
import axiosInstance from '@/config/axiosConfig';

export default {
  name: 'FormComponent',

  props: {
    configId: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      formData: {
        folder_location: '',
        db_host: '',
        db_user: '',
        db_name: '',
        db_password: '',
        id_repo: ''
      },
    };
  },
  methods: {
    async handleSubmit() {
        try {
          const response = await axiosInstance.patch(`/migration/config/${this.configId}/`, this.formData);
          console.log('Form submitted:', response.data);
        } catch (error) {
          console.error('Error submitting form:', error);
        }
    },
    async fetchData() {
      try {
        const response = await axiosInstance.get(`/migration/config/${this.configId}`);
        this.formData = response.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
  mounted() {
    this.fetchData();
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
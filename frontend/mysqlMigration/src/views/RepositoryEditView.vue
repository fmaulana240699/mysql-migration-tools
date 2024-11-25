<template>
  <div class="form-mid">
    <h1>Update Repo Integration</h1>

    <div v-if="showAlert" class="alert">
      <span class="closebtn" @click="closeAlert">&times;</span>
      <strong>Oops!</strong> {{ alertMessage }}
    </div>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="formData.name" required />
      </div>

      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="formData.username" required />
      </div>

      <div class="form-group">
        <label for="branch">Branch:</label>
        <input type="text" id="branch" v-model="formData.branch" required />
      </div>

      <div class="form-group">
        <label for="token">Token:</label>
        <input type="password" id="token" v-model="formData.token"/>
      </div>

      <div class="form-group">
        <label for="repo_url">Repository URL:</label>
        <input type="text" id="repo_url" v-model="formData.repo_url" required />
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
    repoId: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      formData: {
        name: '',
        username: '',
        branch: '',
        token: '',
        repo_url: ''
      },
      showAlert: false,
      alertMessage: ''
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await axiosInstance.patch(`/repo/${this.repoId}/`, this.formData);
        console.log('Form submitted:', response.data);
        window.location.href = `/repository`;
      } catch (error) {
        this.handleError(error, 'Error submitting form');
      }
    },
    async fetchData() {
      try {
        const response = await axiosInstance.get(`/repo/${this.repoId}/`);
        this.formData = response.data;
      } catch (error) {
        this.handleError(error, 'Error fetching data');
      }
    },
    handleError(error, customMessage) {
      if (error.response) {
        this.alertMessage = `${customMessage}: ${error.response.status} ${error.response.data.message || error.response.statusText}`;
      } else {
        this.alertMessage = `${customMessage}: ${error.message}`;
      }
      this.showAlert = true;
    },
    closeAlert() {
      this.showAlert = false;
      this.alertMessage = '';
    }
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

.alert {
  padding: 20px;
  background-color: #f44336;
  color: white;
  margin-top: 20px;
  border-radius: 5px;
  position: relative;
}

.closebtn {
  position: absolute;
  top: 10px;
  right: 15px;
  color: white;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
}

.closebtn:hover {
  color: black;
}
</style>

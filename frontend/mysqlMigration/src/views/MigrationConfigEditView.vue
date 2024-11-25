<template>
  <div class="form-mid">
    <h1>Update Migration Config</h1>

    <div v-if="showAlert" class="alert">
      <span class="closebtn" @click="closeAlert">&times;</span>
      <strong>Oops!</strong> {{ alertMessage }}
    </div>

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
        <input type="password" id="db_password" v-model="formData.db_password"/>
      </div>

      <div class="form-group">
        <label for="id_repo">Repo :</label>
        <input type="text" id="id_repo" v-model="formData.id_repo" v-for="repo in repoList" :key="repo.id" :value="repo.name" disabled />
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
        name: '',
        id_repo: ''
      },
      repoList: '',
      showAlert: false,
      alertMessage: ''
    };
  },
  methods: {
    async handleSubmit() {
      try {
        if (!this.formData.db_password) {
          delete this.formData.db_password;
        }
        const response = await axiosInstance.patch(`/migration/config/${this.configId}/`, this.formData);
        window.location.href = `/migrations/config`;
      } catch (error) {
        this.handleError(error, 'Error submitting form');
      }
    },
    async fetchData() {
      try {
        const response = await axiosInstance.get(`/migration/config/${this.configId}`);
        this.formData = response.data;
      } catch (error) {
        this.handleError(error, 'Error fetching data');
      }
    },
    async fetchRepos() {
      try {
        const response = await axiosInstance.get(`/repo/${this.formData.id_repo}`);
        this.repoList = response.data;
      } catch (error) {
        this.handleError(error, 'Error fetching repos');
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
    this.fetchRepos();
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

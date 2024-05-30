<template>
  <div class="form-mid">
    <h1>Update User</h1>
    
    <div v-if="showAlert" class="alert">
      <span class="closebtn" @click="closeAlert">&times;</span>
      <strong>Oops!</strong> {{ alertMessage }}
    </div>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="fullname">Fullname:</label>
        <input type="text" id="fullname" v-model="formData.fullname" placeholder="Fullname" required />
      </div>
      
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="formData.username" placeholder="Username" required />
      </div>
      
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="formData.password" placeholder="Password" />
      </div>
      
      <div class="form-group">
        <label for="role">Role:</label>
        <input type="text" id="role" v-model="formData.role" placeholder="Role" required />
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
    userId: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      formData: {
        fullname: '',
        username: '',
        password: '',
        role: ''
      },
      showAlert: false,
      alertMessage: ''
    };
  },
  methods: {
    async handleSubmit() {
      try {
        if (!this.formData.password) {
          delete this.formData.password;
        }
        const response = await axiosInstance.patch(`/users/${this.userId}/`, this.formData);
        console.log('Form submitted:', response.data);
        this.$router.push({ name: 'users' });
      } catch (error) {
        this.handleError(error, 'Error submitting form');
      }
    },
    async fetchData() {
      try {
        const response = await axiosInstance.get(`/users/${this.userId}`);
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

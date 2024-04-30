<template>
  <div class="form-mid">
    <h1>Update User</h1>
    
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
        <input type="password" id="password" v-model="formData.password" placeholder="password" />
      </div>
      
      <div class="form-group">
        <label for="repo_url">Role:</label>
        <input type="text" id="repo_url" v-model="formData.role" placeholder="Repo URL" required />
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
    };
  },
  methods: {
    async handleSubmit() {
        try {
          if (!this.formData.password) {
            delete this.formData.password;
          }
          const response = await axiosInstance.patch(`/users/${this.userId}/`, this.formData);
          console.log(response)
          console.log('Form submitted:', response.data);
        } catch (error) {
          console.error('Error submitting form:', error);
        }
        this.$router.push({ name: 'users'});
    },
    async fetchData() {
      try {
        const response = await axiosInstance.get(`/users/${this.userId}`);
        this.formData = response.data

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
@/config/axiosConfig
<template>
<div class="container">
    <div v-if="showAlert" class="alert">
      <span class="closebtn" @click="closeAlert">&times;</span>
      <strong>Oops!</strong> {{ alertMessage }}
    </div>
    <table class="scrollable-table" ref="migrationHistory">
      <thead>
        <tr>
          <th> Id </th>
          <th> SQL Query </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="migration in migrations" :key="migration.id">
            <td> {{ migration.id }} </td>
            <td> {{ migration.sql_query }} </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axiosInstance from '@/config/axiosConfig';

export default {
  props: {
    migrationId: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      migrations: [],
      showAlert: false,
      alertMessage: '',
    };
  },
  mounted() {
    this.fetchItems();
  },
  methods: {
    async fetchItems() {
      try {
        const response = await axiosInstance.get(`/migration/${this.migrationId}`);
        this.migrations = response;
        console.log(this.migrations);
      } catch (error) {
        this.handleError(error, 'Error fetching items');
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
};
</script>
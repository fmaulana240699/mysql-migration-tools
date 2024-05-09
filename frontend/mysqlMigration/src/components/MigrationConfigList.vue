<template>
<div class="container">
    <a class="testing" href="/migrations/config/create"><button class="button-84"> Add New Migration Config </button></a>
    <table>
      <thead>
        <tr>
          <th> Id </th>
          <th> Folder Location </th>
          <th> Database Host </th>
          <th> Database User </th>
          <th> Database Name </th>
          <th> Database Password </th>
          <th> Id Repo </th>
          <th> Author </th>
          <th colspan="2"> Action </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="migration_config in migrations" :key="migration_config.id">
            <td> {{ migration_config.id }} </td>
            <td> {{ migration_config.folder_location }} </td>
            <td> {{ migration_config.db_host }} </td>
            <td> {{ migration_config.db_user }} </td>
            <td> {{ migration_config.db_name }} </td>
            <td> ********* </td>
            <td> {{ migration_config.id_repo }} </td>
            <td> {{ migration_config.author }} </td>
            <td> <button @click="editMigrationConfig(migration_config.id)"> <svg width="35px" height="35px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                 <path d="M21.2799 6.40005L11.7399 15.94C10.7899 16.89 7.96987 17.33 7.33987 16.7C6.70987 16.07 7.13987 13.25 8.08987 12.3L17.6399 2.75002C17.8754 2.49308 18.1605 2.28654 18.4781 2.14284C18.7956 1.99914 19.139 1.92124 19.4875 1.9139C19.8359 1.90657 20.1823 1.96991 20.5056 2.10012C20.8289 2.23033 21.1225 2.42473 21.3686 2.67153C21.6147 2.91833 21.8083 3.21243 21.9376 3.53609C22.0669 3.85976 22.1294 4.20626 22.1211 4.55471C22.1128 4.90316 22.0339 5.24635 21.8894 5.5635C21.7448 5.88065 21.5375 6.16524 21.2799 6.40005V6.40005Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                 <path d="M11 4H6C4.93913 4 3.92178 4.42142 3.17163 5.17157C2.42149 5.92172 2 6.93913 2 8V18C2 19.0609 2.42149 20.0783 3.17163 20.8284C3.92178 21.5786 4.93913 22 6 22H17C19.21 22 20 20.2 20 18V13" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                 </svg> </button> </td>
            <td> <button @click="deleteMigrationConfig(migration_config.id)"> <svg width="35px" height="35px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                 <path d="M10 12V17" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                 <path d="M14 12V17" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                 <path d="M4 7H20" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                 <path d="M6 10V18C6 19.6569 7.34315 21 9 21H15C16.6569 21 18 19.6569 18 18V10" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                 <path d="M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7H9V5Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                 </svg> </button></td>            
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axiosInstance from '@/config/axiosConfig';

export default {
  name: 'MigrationComponent',

  data() {
    return {
      selectedConfigId: null,
      migrations: [],
    };
  },
  methods: {
    async fetchRepos() {
      try {
        const response = await axiosInstance.get(`/migration/config/`);
        this.migrations = response.data
      } catch (error) {
        console.error("Error fetching repos:", error);
      }
    },
    editMigrationConfig(configId) {
      this.$router.push({ name: 'migrationsConfigEdit', params: { configId } });
    },
    async deleteMigrationConfig(configId) {
      try {
        const response = await axiosInstance.delete(`/migration/config/delete/`, {data: {"id": configId}});
      } catch (error) {
        console.error("Error deleting repos:", error);
      }

      window.location.reload();
    },    
  },
  mounted() {
    this.fetchRepos();
  },    
};
</script>
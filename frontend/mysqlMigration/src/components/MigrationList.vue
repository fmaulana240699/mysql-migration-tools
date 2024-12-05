<template>
<div class="container">
  <div v-if="showAlert" class="alert">
    <span class="closebtn" @click="closeAlert">&times;</span>
    <strong>Oops!</strong> {{ alertMessage }}
  </div>
  <div class="dropdown" @click="toggleDropdown">
      <button class="dropbtn">Export Data</button>
      <div :class="{ 'dropdown-content': true, 'show': showDropdown }" id="myDropdown">
        <a @click="exportPDF('1_day')">1 Day</a>
        <a @click="exportPDF('1_week')">1 Week</a>
        <a @click="exportPDF('1_month')">1 Month</a>
      </div>
  </div>
  <div class="scrollable-table">
    <table ref="migrationHistory">
      <thead>
        <tr>
          <th>Id</th>
          <th> Engineer Name </th>
          <th> Status Query </th>
          <th> Error Log </th>
          <th> File Name </th>
          <th> Database Name </th>
          <th> Created At </th>
          <th> Updated At </th>
          <th> Action </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="migrations.length === 0">
          <td colspan="10" style="text-align: center;">No data available</td>
        </tr>
        <tr v-for="migration in migrations" :key="migration.id">
            <td> {{ migration.id }} </td>
            <td> {{ migration.engineer_name }} </td>
            <td> {{ migration.status_query }} </td>
            <td> {{ migration.error_log }} </td>
            <td> {{ migration.file_name }} </td>
            <td> {{ migration.db_name }} </td>
            <td> {{ migration.created_at }} </td>
            <td> {{ migration.updated_at }} </td>
            <td> <button @click="detailsPage(migration.id)"> <svg fill="#000000" height="40px" width="40px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 57.945 57.945" xml:space="preserve">
                <g>
                	<path d="M57.655,27.873c-7.613-7.674-17.758-11.9-28.568-11.9c-0.026,0-0.051,0.002-0.077,0.002c-0.013,0-0.025-0.002-0.037-0.002
                		c-0.036,0-0.071,0.005-0.106,0.005C18.14,16.035,8.08,20.251,0.52,27.873l-0.23,0.232c-0.389,0.392-0.386,1.025,0.006,1.414
                		c0.195,0.193,0.45,0.29,0.704,0.29c0.257,0,0.515-0.099,0.71-0.296l0.23-0.232c5.245-5.287,11.758-8.841,18.856-10.402
                		c-2.939,2.385-4.823,6.022-4.823,10.094c0,7.168,5.832,13,13,13s13-5.832,13-13c0-4.116-1.928-7.784-4.922-10.167
                		c7.226,1.522,13.858,5.107,19.184,10.476c0.389,0.393,1.023,0.395,1.414,0.006C58.041,28.898,58.044,28.265,57.655,27.873z
                		 M39.973,28.972c0,6.065-4.935,11-11,11s-11-4.935-11-11c0-6.029,4.878-10.937,10.893-10.995c0.048,0,0.096-0.003,0.144-0.003
                		C35.058,17.995,39.973,22.92,39.973,28.972z"/>
                	<path d="M36,27.972c-0.552,0-1,0.448-1,1c0,3.309-2.691,6-6,6s-6-2.691-6-6s2.691-6,6-6c0.552,0,1-0.448,1-1s-0.448-1-1-1
                		c-4.411,0-8,3.589-8,8s3.589,8,8,8s8-3.589,8-8C37,28.42,36.552,27.972,36,27.972z"/>
                </g> </svg> </button> </td>
        </tr>
        <tr>
          <td colspan="9" style="text-align: center;">
            <button  v-if="prevPage"  class="button-84"  @click="navigatePage(prevPage)">  Previous</button>
            <button v-if="nextPage" class="button-84" @click="navigatePage(nextPage)"> Next </button>
          </td>
        </tr>
      </tbody>
    </table>
    <br><br>
  </div>
  </div>
</template>

<script>
import axiosInstance from '@/config/axiosConfig';

export default {
  data() {
    return {
      migrations: [],
      nextPage: null,
      prevPage: null,
      showDropdown: false,
      showAlert: false,
      alertMessage: '',
    };
  },
  mounted() {
    this.fetchItems();
  },
  // computed: {
  //   canNavigatePrev() {
  //     return this.currentPage > 1;
  //   },
  //   canNavigateNext() {
  //     return this.nextPage && this.migrations.length > 5;
  //   },
  // },
  methods: {
    async fetchItems(url = '/migration/') {
      try {
        const response = await axiosInstance.get(url);
        this.migrations = response.data.results;
        this.nextPage = response.data.next;
        this.prevPage = response.data.previous;
        // console.log(this.migrations.db_name);
      } catch (error) {
        this.handleError(error, 'Error fetching items');
      }
    },
    // getCurrentPageFromUrl(url) {
    //   const params = new URLSearchParams(url.split("?")[1]);
    //   return parseInt(params.get("page")) || 1;
    // },
    async navigatePage(url){
      if (url){
        this.fetchItems(url);
      }
    },
    async detailsPage(migrationId) {
      window.location.href = `/migrations/${migrationId}`;
    },
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    async exportPDF(timeRange) {
      try {
        const response = await axiosInstance.get(`/migration/export/?time_range=${timeRange}`, {responseType: 'blob'});
        // Create a Blob object from the response data
        const blob = new Blob([response.data], { type: 'application/pdf' });

        // Create a URL for the Blob
        const url = window.URL.createObjectURL(blob);

        // Create a link element
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'exported_file.pdf'); // Set the filename for download

        // Append the link to the document body and click it to trigger download
        document.body.appendChild(link);
        link.click();

        // Remove the link from the document body
        document.body.removeChild(link);

        // Release the URL object
        window.URL.revokeObjectURL(url);
      } catch (error) {
        this.handleError(error, 'Error exporting PDF');
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
<style>
 /* Dropdown Button */
 .dropbtn {
  align-items: center;
  background-color: initial;
  background-image: linear-gradient(#464d55, #25292e);
  border-radius: 8px;
  border-width: 0;
  box-shadow: 0 10px 20px rgba(0, 0, 0, .1),0 3px 6px rgba(0, 0, 0, .05);
  box-sizing: border-box;
  color: #fff;
  cursor: pointer;
  display: inline-flex;
  flex-direction: column;
  font-family: expo-brand-demi,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
  font-size: 18px;
  height: 52px;
  justify-content: center;
  line-height: 1;
  margin: 0;
  outline: none;
  overflow: hidden;
  padding: 0 32px;
  text-align: center;
  text-decoration: none;
  transform: translate3d(0, 0, 0);
  transition: all 150ms;
  vertical-align: baseline;
  white-space: nowrap;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}

/* Dropdown button on hover & focus */
.dropbtn:hover, .dropbtn:focus {
  box-shadow: rgba(0, 1, 0, .2) 0 2px 8px;
  opacity: .85;
}

/* The container <div> - needed to position the dropdown content */
.dropdown {
  position: relative;
  display: inline-block;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

/* Links inside the dropdown */
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

/* Change color of dropdown links on hover */
.dropdown-content a:hover {background-color: #ddd;}

/* Show the dropdown menu (use JS to add this class to the .dropdown-content container when the user clicks on the dropdown button) */
.show {display:block;}
</style>
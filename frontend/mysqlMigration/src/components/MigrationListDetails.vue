<template>
<div class="container">
  <!-- <button class="button-84" @click="exportToPDF">Export to PDF</button> -->
    <table class="scrollable-table" ref="migrationHistory">
      <thead>
        <tr>
          <th> Id </th>
          <th> SQL Query </th>
          <!-- <th> Error Log </th>
          <th> File Name </th>
          <th> Database Name </th>
          <th> Created At </th>
          <th> Updated At </th>
          <th> Action </th> -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="migration in migrations" :key="migration.id">
            <td> {{ migration.id }} </td>
            <!-- <td> {{ migration.author }} </td> -->
            <td> {{ migration.sql_query }} </td>
            <!-- <td> {{ migration.error_log }} </td> -->
            <!-- <td> {{ migration.file_name }} </td> -->
            <!-- <td> {{ migration.db_name }} </td> -->
            <!-- <td> {{ migration.created_at }} </td> -->
            <!-- <td> {{ migration.updated_at }} </td> -->
            <!-- <td> <button> <svg fill="#000000" height="40px" width="40px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
	 viewBox="0 0 57.945 57.945" xml:space="preserve">
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
</g>
</svg> </button> </td> -->
        </tr>
      </tbody>
    </table>
    <!-- <button class="button-84" @click="fetchItems(prevPage)" :disabled="!prevPage">Previous</button> -->
    <!-- <button class="button-84" @click="fetchItems(nextPage)" :disabled="!nextPage">Next</button> -->
  </div>
</template>

<script>
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
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
        console.error('Error fetching items:', error);
      }
    },
    // exportToPDF() {
    //   const table = this.$refs.migrationHistory;

    //   html2canvas(table).then(canvas => {
    //     const imgData = canvas.toDataURL('image/png');
    //     const pdf = new jsPDF();
    //     const imgProps = pdf.getImageProperties(imgData);
    //     const pdfWidth = pdf.internal.pageSize.getWidth();
    //     const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

    //     pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
    //     pdf.save('export.pdf');
    //   });
    // }
  },
};
</script>
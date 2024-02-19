<template>
    <div class="container-md mb-4"> <!-- Adjusted container width -->
      <h3 class="text-center mb-4 my-4 ">APN Data Viewer</h3>
      <div class="justify-content-center"> <!-- Centering the row -->
        <div style =" display: flex; justify-content: center;flex-direction: column;">
          <input  type="text" v-model="search" v-on:input="filterOptions" placeholder="Search"><br>
            <select  v-model="selectedApn" v-bind:size="20" >
                  <option disabled value="">Please select one</option>
                  <option v-for="apn in filteredOptions" :key="apn.apn" :value="apn.apn">{{ apn.apn }}</option>
            </select>
        </div>
        <div>
           <button type="button" class="btn btn-primary my-5" @click="fetchApnDetails">Submit</button>
        </div>

        <div id="apnData" >
          <div v-html="apnTable" ></div>
        </div>
      </div>
    </div>
</template>



<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedApn: '',       // Selected APN from dropdown
      apnData: [],           // Array to store APN data
      apnTable: '',           // HTML table to display APN details
      search: ''
    };
  },
  computed: {
                filteredOptions() {
                    return this.apnData.filter(apn => {
                        return apn.apn.includes(this.search.toLowerCase());
                    });
                }
  },
  mounted() {
    this.fetchApnData();
  },
  methods: {
    fetchApnData() {
      try {
        axios.get('http://localhost:5000/api/apn')
          .then((res) => {
            console.log(res);
            this.apnData = res.data.data;
          })
          .catch((error) => {
            console.error('Error fetching APN data:', error);
          });
      } catch (error) {
        console.error('Error fetching APN data:', error);
      }
    },
    filterOptions() {
                    this.filteredOptions = this.apnData.filter(apn => {
                        return apn.apn.includes(this.search.toLowerCase());
                    });
                    console.log("hello");
                    console.log(this.filteredOptions);
    },
    fetchApnDetails() {
      if (this.selectedApn) {
        axios.get(`http://localhost:5000/api/apn/${this.selectedApn}`)
          .then((res) => {
            console.log(res);
            console.log("hello")
            console.log(this.selectedApn);
            this.displayData(res.data);
          })
          .catch((error) => {
            console.error('Error fetching APN details:', error);
          });
      } else {
        console.error('No APN selected');
      }
    },
    displayData(res) {
      if (res && res.status === 'success' && res.data) {
        let tableHTML = '<h5 class="my-5">APN Details</h5><table  class="table table-hover">'
        let data = res.data[0];
        console.log(data);
        for (let key in data) {
          if (key !== "properties") {
            tableHTML += '<tr><th scope="col">' + key + '</th><td>' + data[key] + '</td></tr>';
          } else {
            for (let subKey in data[key]) {
              if (Array.isArray(data[key][subKey])) {
                tableHTML += '<tr><th scope="col">' + subKey + '</th><td>' + data[key][subKey].join('<br>') + '</td></tr>';
              } else {
                tableHTML += '<tr><th scope="col">' + subKey + '</th><td>' + data[key][subKey] + '</td></tr>';
              }
            }
          }
        }
        tableHTML += '</table>';
        this.apnTable = tableHTML;
      } else {
        console.error('Invalid or missing response data');
      }
    },
  }
};
</script>

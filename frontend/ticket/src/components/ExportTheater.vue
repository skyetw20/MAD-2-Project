<template>
  <div v-if="isAdmin" class="container mt-5">
    <div v-if="successMessage" class="alert alert-success mt-4">
      {{ successMessage }}
    </div>
    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">Export Theater Details</h5>
        <form @submit.prevent="exportJob">
          <div class="mb-3">
            <label for="theater" class="form-label">Select Theater:</label>
            <select v-model="selectedTheater" class="form-control" id="theater">
              <option
                v-for="theater in theaters"
                :key="theater.id"
                :value="theater.id"
              >
                {{ theater.name }} - {{ theater.place }}
              </option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">Export CSV</button>
        </form>
      </div>
    </div>
    <div class="mt-4"></div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      theaters: [],
      successMessage: "",
      selectedTheater: null,
    };
  },
  computed: {
    isAdmin() {
      const userDetails = JSON.parse(localStorage.getItem("userDetails"));
      return userDetails && userDetails.role === "admin";
    },
  },
  async beforeRouteEnter(to, from, next) {
    const userDetails = JSON.parse(localStorage.getItem("userDetails"));
    const isAdmin = userDetails && userDetails.role === "admin";
    if (isAdmin) {
      next();
    } else {
      alert("You are not allowed to access this page.");
      next("/");
    }
  },
  async mounted() {
    await this.fetchTheaters();
  },
  methods: {
    async fetchTheaters() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/theaters");
        this.theaters = response.data.theaters;
      } catch (error) {
        console.error("Error fetching theater list:", error);
      }
    },
    async exportJob() {
      try {
        const userDetails = JSON.parse(localStorage.getItem("userDetails"));
        const userId = userDetails ? userDetails.userId : null;

        if (!userId) {
          console.error("User not logged in");
          return;
        }

        const theaterdata = {
          theater_id: this.selectedTheater,
        };

        const response = await axios.post(
          "http://127.0.0.1:5000/exporttheater",
          theaterdata,
          {
            headers: {
              Authorization: "Bearer " + userDetails.access_token,
            },
          }
        );

        if (response.status === 200) {
          this.successMessage =
            "Export job sent, you'll recieve the report in your email";
          this.errorMessage = "";
          setTimeout(() => {
            this.successMessage = "";
            this.$router.push("/admin");
          }, 10000); 
        } else {
          this.errorMessage = "Export job failed. Please try again.";
          this.successMessage = "";
        }
      } catch (error) {
        this.errorMessage = "Export job failed. Please try again....";
        this.successMessage = "";
      }
    },
  },
};
</script>

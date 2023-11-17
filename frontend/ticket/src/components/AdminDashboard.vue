<template>
  <div v-if="isAdmin" class="container mt-5">
    <h1 class="text-dark">Admin Dashboard</h1>

    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title">Account Details</h5>
        <p class="card-text">
          <strong>Name:</strong> {{ userDetails.username }}
        </p>
        <p class="card-text"><strong>Email:</strong> {{ userDetails.email }}</p>
      </div>
    </div>

    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">Shows Statistics</h5>
        <p>Total Number of Shows: {{ showStatistics.totalShows }}</p>
      </div>
    </div>

    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">Theaters Statistics</h5>
        <p>Total Theaters: {{ theaterStatistics.totalTheaters }}</p>
        <p>
          Total Capacity of All Theaters: {{ theaterStatistics.totalCapacity }}
        </p>
        <p>Total Seats Booked: {{ theaterStatistics.totalSeatsBooked }}</p>
        <p>
          Vacant Seats:
          {{
            theaterStatistics.totalCapacity - theaterStatistics.totalSeatsBooked
          }}
        </p>

      </div>
    </div>
    <div class="mt-4">
      <router-link class="btn btn-primary mr-2" to="/showManage"
        >Show Manage</router-link
      >
      <router-link class="btn btn-primary mr-2" to="/theaterManage"
        >Theater Manage</router-link
      >
      <router-link class="btn btn-primary mr-2" to="/addShow"
        >Add Show</router-link
      >
      <router-link class="btn btn-primary" to="/addTheater"
        >Add Theater</router-link
      >
    </div>

    <div class="mt-4"></div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userDetails: {},
      showStatistics: {},
      theaterStatistics: {},
    };
  },

  computed: {
    isAdmin() {
      return (
        this.userDetails &&
        this.userDetails.role &&
        this.userDetails.role === "admin"
      );
    },
  },
  async beforeRouteEnter(to, from, next) {
    const userDetails = JSON.parse(localStorage.getItem("userDetails"));
    const isAdmin = userDetails && userDetails.role === "admin";
    if (isAdmin) {
      next();
    } else {
      alert("You are not allowed to access the admin dashboard.");
      next("/");
    }
  },
  async mounted() {
    await this.fetchUserDetails();
    if (this.isAdmin) {
      await this.fetchShowStatistics();
      await this.fetchTheaterStatistics();
    }
  },
  methods: {
    async fetchUserDetails() {
      try {
        const userDetails = JSON.parse(localStorage.getItem("userDetails"));
        this.userDetails = userDetails;
      } catch (error) {
        console.error("Error fetching user details:", error);
      }
    },
    async fetchShowStatistics() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/shows");
        this.showStatistics.totalShows = response.data.shows.length;
      } catch (error) {
        console.error("Error fetching show statistics:", error);
      }
    },
    async fetchTheaterStatistics() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/theaters");
        const theaters = response.data.theaters;
        this.theaterStatistics.totalTheaters = theaters.length;
        this.theaterStatistics.totalCapacity = theaters.reduce(
          (total, theater) => total + theater.capacity,
          0
        );
        this.theaterStatistics.totalSeatsBooked = theaters.reduce(
          (total, theater) => total + theater.capacity_booked,
          0
        );
      } catch (error) {
        console.error("Error fetching theater statistics:", error);
      }
    },
  },
};
</script>

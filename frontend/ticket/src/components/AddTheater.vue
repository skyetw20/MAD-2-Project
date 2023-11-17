<template>
  <div  v-if="isAdmin" class="container mt-5">
    <h1 class="text-dark">Add Theater</h1>

    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">Add New Theater</h5>
        <form @submit.prevent="addTheater">
          <div class="form-group">
            <label for="name">Theater Name</label>
            <input
              type="text"
              class="form-control"
              v-model="theaterName"
              required
            />
          </div>
          <div class="form-group">
            <label for="place">Place</label>
            <input type="text" class="form-control" v-model="place" required />
          </div>
          <div class="form-group">
            <label for="capacity">Capacity</label>
            <input
              type="number"
              class="form-control"
              v-model="capacity"
              required
            />
          </div>
          <div class="form-group">
            <label for="rating">Rating</label>
            <input
              type="number"
              class="form-control"
              v-model="rating"
              step="0.1"
              required
            />
          </div>
          <div class="form-group">
            <label for="capacity_booked">Capacity Booked</label>
            <input
              type="number"
              class="form-control"
              v-model="capacityBooked"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary">Add Theater</button>
        </form>
        <p class="mt-3">{{ message }}</p>
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
      theaterName: "",
      place: "",
      capacity: 0,
      rating: 0,
      capacityBooked: 0,
      message: "",
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
  methods: {
    async addTheater() {
      try {
        const userDetails = JSON.parse(localStorage.getItem("userDetails"));
        const response = await axios.post(
          "http://127.0.0.1:5000/addtheater",
          {
            email: userDetails.email,
            name: this.theaterName,
            place: this.place,
            capacity: this.capacity,
            rating: this.rating,
            capacity_booked: this.capacityBooked,
          },
          {
            headers: {
              Authorization: "Bearer " + userDetails.access_token,
            },
          }
        );
        this.message = response.data.message;
      } catch (error) {
        console.error("Error adding theater:", error);
        this.message = "An error occurred while adding the theater.";
      }
    },
  },
};
</script>

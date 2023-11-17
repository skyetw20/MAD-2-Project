<template>
  <div v-if="isAdmin" class="container mt-5">
    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">Add New Show</h5>
        <form @submit.prevent="addShow">
          <div class="form-group">
            <label for="name">Show Name</label>
            <input
              type="text"
              class="form-control"
              v-model="showName"
              required
            />
          </div>
          <div class="form-group">
            <label for="duration">Duration</label>
            <input
              type="number"
              class="form-control"
              v-model="duration"
              required
            />
          </div>
          <div class="form-group">
            <label for="price">Price</label>
            <input
              type="number"
              class="form-control"
              v-model="price"
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
            <label for="tag">Tag</label>
            <input type="text" class="form-control" v-model="tag" required />
          </div>
          <div class="form-group">
            <label for="theaters">Select Theaters</label>
            <select
              v-model="selectedTheaters"
              class="form-control"
              id="theaters"
              multiple
            >
              <option
                v-for="theater in theaters"
                :key="theater.id"
                :value="theater.id"
              >
                {{ theater.name }} - {{ theater.place }}
              </option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">Add Show</button>
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
      showName: "",
      duration: 0,
      price: 0,
      rating: 0,
      tag: "",
      message: "",
      selectedTheaters: [],
      theaters: [],
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
        console.error("Error fetching theaters:", error);
      }
    },
    async addShow() {
      try {
        const userDetails = JSON.parse(localStorage.getItem("userDetails"));
        const response = await axios.post(
          "http://127.0.0.1:5000/addshow",
          {
            email: userDetails.email,
            name: this.showName,
            duration: this.duration,
            price: this.price,
            rating: this.rating,
            tag: this.tag,
            theaters: this.selectedTheaters,
          },
          {
            headers: {
              Authorization: "Bearer " + userDetails.access_token,
            },
          }
        );
        this.message = response.data.message;
      } catch (error) {
        console.error("Error adding show:", error);
        this.message = "An error occurred while adding the show.";
      }
    },
  },
};
</script>

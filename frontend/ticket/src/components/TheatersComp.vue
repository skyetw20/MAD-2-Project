<template>
  <div class="container mt-5">
    <h1 class="text-dark">Theaters</h1>

    <!-- Filters -->
    <div class="mb-3">
      <label for="filterCity" class="text-dark">Select City:</label>
      <select v-model="selectedCity" class="form-control" id="filterCity">
        <option value="">All</option>
        <option v-for="city in uniqueCities" :key="city">{{ city }}</option>
      </select>
    </div>

    <div class="row">
      <div
        class="col-md-4"
        v-for="theater in sortedFilteredTheaters"
        :key="theater.id"
      >
        <div class="card bg-dark text-light mb-3">
          <img
            class="card-img-top"
            src="https://via.placeholder.com/300x200"
            alt="Theater Image"
          />
          <div class="card-body">
            <h5 class="card-title">{{ theater.name }}</h5>
            <p class="card-text">City: {{ theater.place }}</p>
            <p class="card-text">
              Available Seats: {{ theater.capacity - theater.capacity_booked }}
            </p>
            <p class="card-text">Rating: {{ theater.rating }}</p>
            <router-link
              :to="{
                name: 'ViewTheater',
                params: {
                  theaterId: theater.id,
                },
              }"
              class="btn btn-primary"
            >
              View Details
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      theaters: [],
      selectedCity: "",
    };
  },
  computed: {
    uniqueCities() {
      const cities = new Set();
      this.theaters.forEach((theater) => cities.add(theater.place));
      return Array.from(cities);
    },
    sortedFilteredTheaters() {
      const filtered = this.selectedCity
        ? this.theaters.filter((theater) => theater.place === this.selectedCity)
        : this.theaters;

      return filtered.slice().sort((a, b) => b.rating - a.rating);
    },
  },
  mounted() {
    this.fetchTheaters();
  },
  methods: {
    async fetchTheaters() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/theaters");
        this.theaters = response.data.theaters;

        console.log("Fetched Theaters:", this.theaters);
      } catch (error) {
        console.error("Error fetching theaters:", error);
      }
    },
  },
};
</script>

<style scoped>
body {
  background-color: #343a40;
}
</style>

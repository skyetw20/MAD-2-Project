<template>
  <div class="container mt-5">
    <h1 class="text-dark">All Shows</h1>

    <!-- Filters -->
    <div class="mb-3">
      <select v-model="selectedTag" class="form-control" id="filterTag">
        <option value="">All</option>
        <option v-for="tag in uniqueTags" :key="tag">{{ tag }}</option>
      </select>
    </div>

    <div class="row">
      <div class="col-md-4" v-for="show in filteredShows" :key="show.id">
        <div class="card bg-dark text-light mb-3">
          <img
            class="card-img-top"
            src="https://picsum.photos/id/100/300/200"
            alt="Show Image"
          />
          <div class="card-body">
            <h5 class="card-title">{{ show.name }}</h5>
            <p class="card-text">Duration: {{ show.duration }} mins</p>
            <p class="card-text">Rating: {{ show.rating }}</p>
            <p class="card-text">Tag: {{ show.tag }}</p>
            <p class="card-text">Ticket Price: {{ show.ticket_price }}</p>
            <router-link
              :to="{
                name: 'Booking',
                params: {
                  showId: show.id,
                  showName: show.name,
                  ticketPrice: show.ticket_price,
                },
              }"
              class="btn btn-primary"
            >
              Book Now
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
      shows: [],
      selectedTag: "",
    };
  },
  computed: {
    uniqueTags() {
      const tags = new Set();
      this.shows.forEach((show) => tags.add(show.tag));
      return Array.from(tags);
    },
    filteredShows() {
      const filtered = this.selectedTag
        ? this.shows.filter((show) => show.tag === this.selectedTag)
        : this.shows;

      return filtered.slice().sort((a, b) => b.rating - a.rating);
    },
  },
  mounted() {
    this.fetchShows();
  },
  methods: {
    async fetchShows() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/shows");
        this.shows = response.data.shows;

        console.log("Fetched Shows:", this.shows);
      } catch (error) {
        console.error("Error fetching shows:", error);
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

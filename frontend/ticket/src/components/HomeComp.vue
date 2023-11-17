<template>
  <div class="container mt-5">
    <div class="mt-4">
      <h2 class="text-dark">Popular Shows</h2>
      <div class="row">
        <div class="col-md-4" v-for="show in popularShows" :key="show.id">
          <div class="card bg-dark text-light mb-3">
            <img
              class="card-img-top"
              src="https://picsum.photos/id/200/300/200"
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

    <div class="mt-4">
      <h2 class="text-dark">Popular Theaters</h2>
      <div class="row">
        <div
          class="col-md-4"
          v-for="theater in popularTheaters"
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
              <p class="card-text">{{ theater.address }}</p>
              <p class="card-text">Capacity: {{ theater.capacity }}</p>
              <p class="card-text">Phone: {{ theater.phone }}</p>
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
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      popularShows: [],
      popularTheaters: [],
    };
  },
  async mounted() {
    await this.fetchPopularShows();
    await this.fetchPopularTheaters();
  },
  methods: {
    async fetchPopularShows() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/shows");
        this.popularShows = response.data.shows.slice(0, 6);
      } catch (error) {
        console.error("Error fetching popular shows:", error);
      }
    },
    async fetchPopularTheaters() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/theaters");
        this.popularTheaters = response.data.theaters.slice(0, 6);
      } catch (error) {
        console.error("Error fetching popular theaters:", error);
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

<template>
  <div class="container mt-5">
    <div v-if="theater" class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">{{ theater.name }}</h5>
        <p class="card-text">Place: {{ theater.place }}</p>
        <p class="card-text">Capacity: {{ theater.capacity }}</p>
        <p class="card-text">Capacity Booked: {{ theater.capacity_booked }}</p>
        <p class="card-text">Rating: {{ theater.rating }}</p>
      </div>
    </div>
    <div class="card bg-light text-dark mt-4">
      <div class="card-body">
        <h5 class="card-title text-dark">Available Shows</h5>
        <div class="row">
          <div class="col-md-4" v-for="show in availableShows" :key="show.id">
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
    </div>
    <div class="mt-4"></div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      theater: null,
      availableShows: [],
    };
  },
  async mounted() {
    await this.fetchTheater();
    await this.fetchAvailableShows();
  },
  methods: {
    async fetchTheater() {
      try {
        const theaterId = this.$route.params.theaterId;
        const response = await axios.get(`http://127.0.0.1:5000/theaters`);
        // console.log(response.data.theaters)
        for (const theat of response.data.theaters) {
          // console.log(theaterId)
          if (theat.id === Number(theaterId)) {
            this.theater = theat;
            // console.log(theat.id);
          }
        }

        // console.log(this.theater);
      } catch (error) {
        console.error("Error fetching theater:", error);
      }
    },
    async fetchAvailableShows() {
      try {
        const theaterId = this.$route.params.theaterId;
        const Showsresponse = await axios.get(`http://127.0.0.1:5000/shows`);
        const relationResponse = await axios.get(
          `http://127.0.0.1:5000/relation`
        );
        // console.log()
        const showIds = [];
        for (const relation of relationResponse.data.realtions) {
          // console.log(relation.showid);
          if (relation.theaterid === Number(theaterId)) {
            showIds.push(relation.showid);
          }
        }
        console.log(showIds);
        this.availableShows = Showsresponse.data.shows.filter((show) =>
          showIds.includes(show.id)
        );
        console.log(this.availableShows);
      } catch (error) {
        console.error("Error fetching available shows:", error);
      }
    },
  },
};
</script>

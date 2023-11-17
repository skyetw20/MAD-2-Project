<template>
  <div class="container mt-5">
    <h1 class="text-dark">Book Now</h1>

    <div class="card bg-dark text-light mb-3">
      <div class="card-body">
        <h5 class="card-title">Show Information</h5>
        <p class="card-text">Show Name: {{ showName }}</p>
        <p class="card-text">Ticket Price: {{ ticketPrice }}</p>
      </div>
    </div>

    <form @submit.prevent="bookTickets" v-if="userDetails">
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
      <div class="mb-3">
        <label for="timing" class="form-label">Select Timing:</label>
        <select v-model="selectedTiming" class="form-control" id="timing">
          <option v-for="timing in timings" :key="timing">{{ timing }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="date" class="form-label">Select Date:</label>
        <input
          v-model="selectedDate"
          type="date"
          class="form-control"
          id="date"
          required
        />
      </div>
      <div class="mb-3">
        <label for="seats" class="form-label">Number of Seats:</label>
        <input
          v-model="numSeats"
          type="number"
          class="form-control"
          id="seats"
          min="1"
          :max="availableSeats"
          required
        />
      </div>
      <p>Total Price: {{ totalPrice }}</p>
      <button type="submit" class="btn btn-primary">Book Tickets</button>
    </form>
    <div v-else>
      <div class="alert alert-warning">
        You need to login to book tickets. Please login first.
      </div>
      <router-link to="/login" class="btn btn-primary">Login</router-link>
    </div>
    <div v-if="successMessage" class="alert alert-success mt-3">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="alert alert-danger mt-3">
      {{ errorMessage }}
    </div>
    <div class="mt-4"></div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userDetails: JSON.parse(localStorage.getItem("userDetails")),
      showName: this.$route.params.showName,
      ticketPrice: this.$route.params.ticketPrice,
      theaters: [],
      selectedTheater: null,
      selectedTiming: null,
      selectedDate: null,
      numSeats: 1,
      successMessage: "",
      errorMessage: "",
    };
  },
  computed: {
    timings() {
      return ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM", "10:00 PM"];
    },
    availableSeats() {
      if (this.selectedTheater) {
        const selectedTheater = this.theaters.find(
          (theater) => theater.id === this.selectedTheater
        );
        if (selectedTheater) {
          return selectedTheater.capacity - selectedTheater.capacity_booked;
        }
      }
      return 0;
    },
    totalPrice() {
      return this.numSeats * this.ticketPrice;
    },
  },
  async mounted() {
    await this.fetchTheaters();
    if (this.userDetails) {
      await this.fetchTheaters();
    }
  },

  methods: {
    async fetchTheaters() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/theaters");
        const relationResponse = await axios.get(
          "http://127.0.0.1:5000/relation"
        );
        const showId = this.$route.params.showId;
        // console.log(relationResponse.data.realtions.showid);
        const theaterIds = [];
        for (const relation of relationResponse.data.realtions) {
          // console.log(relation.showid);
          if (relation.showid === Number(showId)) {
            theaterIds.push(relation.theaterid);
          }
        }

        console.log(theaterIds);
        this.theaters = response.data.theaters.filter((theater) =>
          theaterIds.includes(theater.id)
        );
      } catch (error) {
        console.error("Error fetching theaters:", error);
      }
    },
    async bookTickets() {
      try {
        const userDetails = JSON.parse(localStorage.getItem("userDetails"));
        const userId = userDetails ? userDetails.userId : null;

        if (!userId) {
          console.error("User not logged in");
          return;
        }

        const bookingData = {
          show_id: this.$route.params.showId,
          theater_id: this.selectedTheater,
          time: this.selectedTiming,
          date: this.selectedDate,
          num_seats: this.numSeats,
          total_price: this.totalPrice,
          user_id: userId,
        };

        const response = await axios.post(
          "http://127.0.0.1:5000/bookings",
          bookingData,
          {
            headers: {
              Authorization: "Bearer " + userDetails.access_token,
            },
          }
        );

        if (response.status === 200) {
          this.successMessage = "Booking successful!";
          this.errorMessage = "";
          setTimeout(() => {
            this.successMessage = "";
            this.$router.push("/account");
          }, 3000);
        } else {
          this.errorMessage = "Booking failed. Please try again.";
          this.successMessage = "";
        }
      } catch (error) {
        this.errorMessage = "Error booking tickets. Please try again.";
        this.successMessage = "";
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

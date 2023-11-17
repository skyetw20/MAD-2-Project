<template>
  <div class="container mt-5">
    <h1 class="text-dark">My Account</h1>

    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title">Account Details</h5>
        <p class="card-text"><strong>Name:</strong> {{ user.name }}</p>
        <p class="card-text"><strong>Email:</strong> {{ user.email }}</p>
      </div>
    </div>

    <div class="card bg-dark text-dark mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">Bookings</h5>
        <table class="table table-dark">
          <thead>
            <tr>
              <th scope="col">Show Name</th>
              <th scope="col">Theater</th>
              <th scope="col">Date</th>
              <th scope="col">Time</th>
              <th scope="col">Seats</th>
              <th scope="col">Price</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(booking, index) in user.bookings" :key="index">
              <td>{{ booking.show }}</td>
              <td>{{ booking.theater }}</td>
              <td>{{ booking.date }}</td>
              <td>{{ booking.time }}</td>
              <td>{{ booking.seats }}</td>
              <td>{{ booking.price }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div style="margin-bottom: 20px;"></div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      user: {
        name: "",
        email: "",
        bookings: [],
      },
    };
  },
  async mounted() {
    await this.fetchAccountDetails();
  },
  methods: {
    async fetchAccountDetails() {
      try {
        const userDetails = JSON.parse(localStorage.getItem("userDetails")); 
        if (!userDetails || !userDetails.userId) {
          console.error("User ID not found in local storage");
          return;
        }
        console.log(userDetails.access_token)
        const response = await axios.get(
          `http://127.0.0.1:5000/account?user_id=${userDetails.userId}`,
          {
            headers: {
              Authorization:"Bearer "+ userDetails.access_token
            }
          }
        );
        this.user = response.data;
      } catch (error) {
        console.error("Error fetching account details:", error);
      }
    },
  },
};
</script>
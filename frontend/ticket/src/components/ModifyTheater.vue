<template>
  <div class="container mt-5">
    <h1 class="text-dark">Modify Theater</h1>

    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">Modify Theater</h5>
        <form @submit.prevent="updateTheater">
          <div class="form-group">
            <label for="newName">New Theater Name</label>
            <input type="text" class="form-control" v-model="newTheaterName" />
          </div>
          <div class="form-group">
            <label for="newPlace">New Place</label>
            <input type="text" class="form-control" v-model="newPlace" />
          </div>
          <div class="form-group">
            <label for="newCapacity">New Capacity</label>
            <input type="number" class="form-control" v-model="newCapacity" />
          </div>
          <div class="form-group">
            <label for="newRating">New Rating</label>
            <input
              type="number"
              class="form-control"
              v-model="newRating"
              step="0.1"
            />
          </div>
          <div class="form-group">
            <label for="newCapacityBooked">New Capacity Booked</label>
            <input
              type="number"
              class="form-control"
              v-model="newCapacityBooked"
            />
          </div>
          <button type="submit" class="btn btn-primary">Update Theater</button>
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
      theaterId: this.$route.params.theaterId,
      newTheaterName: "",
      newPlace: "",
      newCapacity: 0,
      newRating: 0,
      newCapacityBooked: 0,
      message: "",
    };
  },
  async mounted() {
    await this.fetchTheaterDetails();
  },
  methods: {
    async fetchTheaterDetails() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/theaters`);
        const theater = response.data.theaters.find(
          (theater) => theater.id === parseInt(this.theaterId)
        );
        if (theater) {
          this.newTheaterName = theater.name;
          this.newPlace = theater.place;
          this.newCapacity = theater.capacity;
          this.newRating = theater.rating;
          this.newCapacityBooked = theater.capacity_booked;
        }
      } catch (error) {
        console.error("Error fetching theater details:", error);
      }
    },
    async updateTheater() {
      try {
        const userDetails = JSON.parse(localStorage.getItem("userDetails"));
        const response = await axios.put(
          "http://127.0.0.1:5000/updatetheater",
          {
            email: userDetails.email,
            theater_id: this.theaterId,
            new_name: this.newTheaterName,
            new_place: this.newPlace,
            new_capacity: this.newCapacity,
            new_rating: this.newRating,
            new_capacity_booked: this.newCapacityBooked,
          },
          {
            headers: {
              Authorization: "Bearer " + userDetails.access_token,
            },
          }
        );
        this.message = response.data.message;
      } catch (error) {
        console.error("Error updating theater:", error);
        this.message = "An error occurred while updating the theater.";
      }
    },
  },
};
</script>

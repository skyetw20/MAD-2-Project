<template>
  <div class="container mt-5">
    <h1 class="text-dark">Modify Show</h1>

    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">Modify Show</h5>
        <form @submit.prevent="updateShow">
          <div class="form-group">
            <label for="newName">New Show Name</label>
            <input type="text" class="form-control" v-model="newShowName" />
          </div>
          <div class="form-group">
            <label for="newDuration">New Duration</label>
            <input type="number" class="form-control" v-model="newDuration" />
          </div>
          <div class="form-group">
            <label for="newPrice">New Price</label>
            <input type="number" class="form-control" v-model="newPrice" />
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
            <label for="newTag">New Tag</label>
            <input type="text" class="form-control" v-model="newTag" />
          </div>
          <button type="submit" class="btn btn-primary">Update Show</button>
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
      showId: this.$route.params.showId,
      newShowName: "",
      newDuration: 0,
      newPrice: 0,
      newRating: 0,
      newTag: "",
      message: "",
    };
  },
  async mounted() {
    await this.fetchShowDetails();
  },
  methods: {
    async fetchShowDetails() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/shows`);
        const show = response.data.shows.find(
          (show) => show.id === parseInt(this.showId)
        );
        if (show) {
          this.newShowName = show.name;
          this.newDuration = show.duration;
          this.newPrice = show.ticket_price;
          this.newRating = show.rating;
          this.newTag = show.tag;
        }
      } catch (error) {
        console.error("Error fetching show details:", error);
      }
    },
    async updateShow() {
      try {
        const userDetails = JSON.parse(localStorage.getItem("userDetails"));
        const response = await axios.put(
          "http://127.0.0.1:5000/updateshow",
          {
            email: userDetails.email,
            show_id: this.showId,
            new_name: this.newShowName,
            new_duration: this.newDuration,
            new_price: this.newPrice,
            new_rating: this.newRating,
            new_tag: this.newTag,
          },
          {
            headers: {
              Authorization: "Bearer " + userDetails.access_token,
            },
          }
        );
        this.message = response.data.message;
      } catch (error) {
        console.error("Error updating show:", error);
        this.message = "An error occurred while updating the show.";
      }
    },
  },
};
</script>

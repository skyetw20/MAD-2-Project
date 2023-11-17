<template>
  <div v-if="isAdmin" class="container mt-5">
    <div v-if="deletedMessage" class="alert alert-success mt-4">
      {{ deletedMessage }}
    </div>
    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">Show List</h5>
        <table class="table table-dark">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Name</th>
              <th scope="col">Rating</th>
              <th scope="col">Tag</th>
              <th scope="col">Duration (mins)</th>
              <th scope="col">Ticket Price</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(show, index) in shows" :key="index">
              <td>{{ show.id }}</td>
              <td>{{ show.name }}</td>
              <td>{{ show.rating }}</td>
              <td>{{ show.tag }}</td>
              <td>{{ show.duration }}</td>
              <td>{{ show.ticket_price }}</td>
              <td>
                <router-link
                  :to="{
                    name: 'modifyShow',
                    params: {
                      showId: show.id,
                    },
                  }"
                  class="btn btn-primary btn-sm"
                >
                  Update
                </router-link>
                <button
                  class="btn btn-danger btn-sm ml-2"
                  @click="deleteShow(show.id)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
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
      shows: [],
      deletedMessage: "",
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
    await this.fetchShows();
  },
  methods: {
    async fetchShows() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/shows");
        this.shows = response.data.shows;
      } catch (error) {
        console.error("Error fetching show list:", error);
      }
    },
    modifyShow(show) {
      this.$router.push(`/modifyshow/${show.id}`);
    },
    async deleteShow(showId) {
      if (confirm("Are you sure you want to delete this show?")) {
        try {
          const userDetails = JSON.parse(localStorage.getItem("userDetails"));
          const response = await axios.delete(
            "http://127.0.0.1:5000/deleteshow",
            {
              data: {
                email: userDetails.email,
                show_id: showId,
              },
              headers: {
                Authorization: "Bearer " + userDetails.access_token,
              },
            }
          );

          console.log(response);
          await this.fetchShows();
          this.deletedMessage = response.data.message;
        } catch (error) {
          console.error("Error deleting show:", error);
        }
      }
    },
  },
};
</script>

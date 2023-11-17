<template>
  <div v-if="isAdmin" class="container mt-5">
    <div v-if="deletedMessage" class="alert alert-success mt-4">
      {{ deletedMessage }}
    </div>
    <div class="card bg-dark text-light mt-4">
      <div class="card-body">
        <h5 class="card-title text-light">Theater List</h5>
        <table class="table table-dark">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Name</th>
              <th scope="col">Place</th>
              <th scope="col">Capacity</th>
              <th scope="col">Capacity Booked</th>
              <th scope="col">Rating</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(theater, index) in theaters" :key="index">
              <td>{{ theater.id }}</td>
              <td>{{ theater.name }}</td>
              <td>{{ theater.place }}</td>
              <td>{{ theater.capacity }}</td>
              <td>{{ theater.capacity_booked }}</td>
              <td>{{ theater.rating }}</td>
              <td>
                <router-link
                  :to="{
                    name: 'modifyTheater',
                    params: {
                      theaterId: theater.id,
                    },
                  }"
                  class="btn btn-primary btn-sm"
                >
                  Update
                </router-link>
                <button
                  class="btn btn-danger btn-sm ml-2"
                  @click="deleteTheater(theater.id)"
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
      theaters: [],
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
    await this.fetchTheaters();
  },
  methods: {
    async fetchTheaters() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/theaters");
        this.theaters = response.data.theaters;
      } catch (error) {
        console.error("Error fetching theater list:", error);
      }
    },

    async deleteTheater(theaterId) {
      if (confirm("Are you sure you want to delete this theater?")) {
        try {
          const userDetails = JSON.parse(localStorage.getItem("userDetails"));
          const response = await axios.delete(
            "http://127.0.0.1:5000/deletetheater",
            {
              data: {
                email: userDetails.email,
                theater_id: theaterId,
              },
              headers: {
                Authorization: "Bearer " + userDetails.access_token,
              },
            }
          );
          console.log(response);
          await this.fetchTheaters();
          this.deletedMessage = response.data.message;
        } catch (error) {
          console.error("Error deleting theater:", error);
        }
      }
    },
  },
};
</script>

<template>
  <div class="container mt-5">
    <h1 class="text-dark">Login</h1>

    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          v-model="email"
          type="email"
          class="form-control"
          id="email"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          v-model="password"
          type="password"
          class="form-control"
          id="password"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>

    <p class="mt-3">
      Don't have an account? <router-link to="/signup">Sign Up</router-link>
    </p>

    <div v-if="message" class="alert alert-info mt-3">{{ message }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
      message: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/login", {
          email: this.email,
          password: this.password,
        });

        if (response.status === 200) {
          this.message = response.data.message;
          // console.log(response.data)
          const userDetails = {
            userId: response.data.user_id,
            username: response.data.username,
            role: response.data.role,
            email: response.data.email,
            access_token:response.data.access_token
          };
          console.log(userDetails)
          localStorage.setItem("userDetails", JSON.stringify(userDetails));

          this.$router.push("/account");
        }
      } catch (error) {
        if (error.response) {
          this.message = error.response.data.message;
        } else {
          this.message = "An error occurred while logging in.";
        }
      }
    },
  },
  mounted() {
    let user = localStorage.getItem("userDetails");
    if (user) {
      alert("You are already logged in.");
      this.$router.push({ name: "Home" });
    }
  },
};
</script>

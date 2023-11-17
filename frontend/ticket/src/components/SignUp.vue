<template>
  <div class="container mt-5">
    <h1 class="text-dark">Sign Up</h1>

    <form @submit.prevent="signup">
      <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input
          v-model="name"
          type="text"
          class="form-control"
          id="name"
          required
        />
      </div>
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
      <div class="mb-3">
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <input
          v-model="confirmPassword"
          type="password"
          class="form-control"
          id="confirmPassword"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Sign Up</button>
    </form>

    <p class="mt-3">
      Already have an account? <router-link to="/login">Login</router-link>
    </p>

    <div v-if="message" class="alert" :class="messageClass">{{ message }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      message: "",
      messageClass: "",
    };
  },
  methods: {
    async signup() {
      if (this.password !== this.confirmPassword) {
        this.message = "Passwords do not match.";
        this.messageClass = "alert-danger";
        return;
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/signup", {
          name: this.name,
          email: this.email,
          password: this.password,
        });

        if (response.status === 200) {
          this.message = response.data.message;
          this.messageClass = "alert-success";
        }
      } catch (error) {
        if (error.response) {
          this.message = error.response.data.message;
          this.messageClass = "alert-danger";
        } else {
          this.message = "An error occurred while signing up.";
          this.messageClass = "alert-danger";
        }
      }
    },
  },
};
</script>

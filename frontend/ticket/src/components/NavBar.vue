<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <router-link to="/" class="navbar-brand">TicketBooking</router-link>
    <button
      class="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarNav"
      aria-controls="navbarNav"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link to="/" class="nav-link">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/shows" class="nav-link">Shows</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/theaters" class="nav-link">Theaters</router-link>
        </li>
      </ul>
      <ul class="navbar-nav">
        <template v-if="loggedIn">
          <li class="nav-item">
            <router-link to="/account" class="nav-link">My Account</router-link>
          </li>
          <li class="nav-item">
            <router-link @click="logout" to="/" class="nav-link"
              >Logout</router-link
            >
          </li>
        </template>
        <template v-else>
          <li class="nav-item">
            <router-link to="/login" class="btn btn-primary ml-2"
              >Login</router-link
            >
          </li>
          <li class="nav-item">
            <router-link to="/signup" class="btn btn-secondary ml-2"
              >Sign Up</router-link
            >
          </li>
        </template>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      loggedIn: false,
    };
  },
  created() {
    this.checkLoggedIn();
  },
  watch: {
    $route: "checkLoggedIn", 
  },
  methods: {
    checkLoggedIn() {
      this.loggedIn = this.isLoggedIn();
    },
    isLoggedIn() {
      return localStorage.getItem("userDetails") !== null;
    },
    logout() {
      localStorage.removeItem("userDetails");
      this.loggedIn = false;
    },
  },
};
</script>

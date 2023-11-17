<template>
  <footer class="footer bg-dark text-light py-5">
    <div class="container">
      <div class="row">
        <div class="col-md-4">
          <h4>Navigation</h4>
          <ul class="list-unstyled">
            <li><router-link class="text-light" to="/">Home</router-link></li>
            <li>
              <router-link class="text-light" to="/shows">Shows</router-link>
            </li>
            <li>
              <router-link class="text-light" to="/theaters"
                >Theaters</router-link
              >
            </li>
            <li v-if="isAdmin" class="mb-2">
              <router-link class="text-light btn btn-primary" to="/admin"
                >Admin Dashboard</router-link
              >
            </li>
            <li v-if="isAdmin" class="mb-2">
              <router-link class="text-light btn btn-primary" to="/addShow"
                >Add Show</router-link
              >
            </li>
            <li v-if="isAdmin" class="mb-2">
              <router-link class="text-light btn btn-primary" to="/addTheater"
                >Add Theater</router-link
              >
            </li>
            <li v-if="isAdmin" class="mb-2">
              <router-link class="btn btn-primary mr-2" to="/showManage"
                >Show Manage</router-link
              >
            </li>
            <li v-if="isAdmin" class="mb-2">
              <router-link class="btn btn-primary mr-2" to="/theaterManage"
                >Theater Manage</router-link
              >
            </li>
            <li v-if="isAdmin" class="mb-2">
              <router-link class="btn btn-primary mr-2" to="/ExportTheater"
                >Export Jobs</router-link
              >
            </li>
          </ul>
        </div>
        <div class="col-md-4">
          <h4>Contact Us</h4>
          <form>
            <div class="form-group">
              <input type="text" class="form-control" placeholder="Name" />
            </div>
            <div class="form-group">
              <input type="email" class="form-control" placeholder="Email" />
            </div>
            <div class="form-group">
              <textarea
                class="form-control"
                rows="3"
                placeholder="Message"
              ></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
        </div>
        <div class="col-md-4">
          <h4>Subscribe</h4>
          <p>Subscribe to our newsletter for updates.</p>
          <div class="input-group">
            <input type="email" class="form-control" placeholder="Email" />
            <div class="input-group-append">
              <button class="btn btn-secondary" type="button">Subscribe</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "FooterComp",
  data() {
    return {
      userDetails: null,
    };
  },
  computed: {
    isAdmin() {
      return this.userDetails && this.userDetails.role === "admin";
    },
  },
  watch: {
    userDetails: {
      handler(newVal) {
        this.userDetails = newVal;
      },
      immediate: true,
    },
  },
  mounted() {
    this.userDetails = JSON.parse(localStorage.getItem("userDetails"));
  },
};
</script>



<style scoped>
.footer {
  background-color: #343a40;
}
</style>

<style scoped>
.footer {
  background-color: #343a40;
}
</style>

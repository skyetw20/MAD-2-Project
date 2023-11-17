<template>
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  <NavBar></NavBar>
  <!-- <HomeComp></HomeComp>
  <ShowsList></ShowsList>
  <TheatersComp></TheatersComp>
  <LoginComp></LoginComp>
  <SignUp></SignUp>
  <AccountComp></AccountComp> -->
  <router-view></router-view>

  <FooterComp></FooterComp>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import FooterComp from "./components/FootComp.vue";

export default {
  name: "App",
  components: {
    NavBar,
    FooterComp,
  },
};
</script>
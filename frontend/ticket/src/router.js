// router.js
import { createRouter, createWebHistory } from "vue-router";
import ShowsList from "./components/ShowsList.vue";
import HomeComp from "./components/HomeComp.vue";
import TheatersComp from "./components/TheatersComp.vue";
import LoginComp from "./components/LoginComp.vue";
import SignUp from "./components/SignUp.vue";
import AccountComp from "./components/AccountComp.vue";
import BookNow from "./components/BookNow.vue";
import AdminDash from "./components/AdminDashboard.vue";
import ShowManage from "./components/ShowManage.vue";
import TheaterManage from "./components/TheaterManage.vue";
import AddShow from "./components/AddShow.vue";
import AddTheater from "./components/AddTheater.vue";
import ModifyShow from "./components/ModifyShow.vue";
import ModifyTheater from "./components/ModifyTheater.vue";
import ViewTheater from "./components/ViewTheater.vue";
import ExportTheater from "./components/ExportTheater.vue";
const routes = [
  { path: "/", component: HomeComp, name: "Home" },
  { path: "/shows", component: ShowsList, name: "Shows" },
  { path: "/theaters", component: TheatersComp, name: "Theaters" },
  { path: "/login", component: LoginComp, name: "Login" },
  { path: "/signup", component: SignUp, name: "Signup" },
  { path: "/account", component: AccountComp, name: "Account" },
  { path: "/admin", component: AdminDash, name: "Admin" },
  { path: "/showManage", component: ShowManage, name: "showManage" },
  { path: "/theaterManage", component: TheaterManage, name: "theaterManage" },
  { path: "/addshow", component: AddShow, name: "addShow" },
  { path: "/addTheater", component: AddTheater, name: "addTheater" },
  { path: "/modifyshow/:showId", component: ModifyShow, name: "modifyShow" },
  {
    path: "/modifyTheater/:theaterId",
    component: ModifyTheater,
    name: "modifyTheater",
  },
  {
    path: "/book/:showId/:showName/:ticketPrice",
    name: "Booking",
    component: BookNow,
  },
  {
    path: "/viewTheater/:theaterId",
    name: "ViewTheater",
    component: ViewTheater,
  },
  {
    path: "/exportTheater",
    component: ExportTheater,
    name: "ExportTheater",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

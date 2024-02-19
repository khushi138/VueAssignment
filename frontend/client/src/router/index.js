import Vue from 'vue';
import Router from 'vue-router';
import HomeComp from "@/components/HomeComp.vue";

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'HomeComp',
      component: HomeComp,
    }
  ],
});

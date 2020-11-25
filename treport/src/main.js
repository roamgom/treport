import Vue from 'vue'
import App from './App.vue'

import axios from 'axios'
import Vuetify from 'vuetify'

import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'


Vue.prototype.$http = axios
Vue.use(Vuetify)
// Vue.use(VueAxios, axios)

Vue.config.productionTip = false

new Vue({
  vuetify: new Vuetify({
    icons: {
      iconfont: 'md',
    },
  }),
  render: h => h(App),
}).$mount('#app')

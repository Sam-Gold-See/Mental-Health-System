import {
	createSSRApp
} from "vue";

import * as Pinia from "pinia"

import App from "./App.vue";

import "@/static/base.scss";

import "@/static/iconfont.css";

import Navbar from "@/pages/component/common/Navbar.vue";

export function createApp() {
	const app = createSSRApp(App);

	app.use(Pinia.createPinia());

	app.component("Navbar", Navbar);

	return {
		app,
	};
}

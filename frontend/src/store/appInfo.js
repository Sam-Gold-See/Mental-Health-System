import { defineStore } from 'pinia'
export const useAppInfoStore = defineStore('appInfo', {
    state: () => {
        return {
            statusBar: 0,
            navBarHeight: 0,
            screenWidth: 0,
            screenHeight: 0,
            deviceId: '',
            deviceBrand: '',
            appVersion: '',
        }
    },
    actions: {
        setInfo(statusBar, navBarHeight, screenWidth, screenHeight, deviceId, deviceBrand, appVersion) {
            this.statusBar = statusBar;
            this.navBarHeight = navBarHeight;
            this.screenWidth = screenWidth;
            this.screenHeight = screenHeight;
            this.deviceId = deviceId;
            this.deviceBrand = deviceBrand;
            this.appVersion = appVersion;
        },
        getInfo() {
            return {
                statusBar: this.statusBar,
                navBarHeight: this.navBarHeight,
                screenWidth: this.screenWidth,
                screenHeight: this.screenHeight,
                deviceId: this.deviceId,
                deviceBrand: this.deviceBrand,
                appVersion: this.appVersion
            }
        }
    }
});
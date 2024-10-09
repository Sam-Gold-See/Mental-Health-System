<script setup>
import { onLaunch } from '@dcloudio/uni-app';

import { useAppInfoStore } from '@/store/appInfo';

const appInfoStore = useAppInfoStore();

const saveDeviceInfo = (e) => {
  let statusBar = e.statusBarHeight;

  if (statusBar == 0) 
    statusBar = 20;

  const naveBarHeight = 45;
  const deviceId = e.deviceId;
  const deviceBrand = e.deviceBrand;

  appInfoStore.setInfo(
    statusBar,
    naveBarHeight,
    e.screenWidth,
    e.screenHeight,
    deviceId,
    deviceBrand
  )
};

onLaunch(() => {
  uni.getSystemInfo({
    success: (e) => {
      saveDeviceInfo(e);
      console.log(e);
    },
  });
});
</script>

<style>
/*每个页面公共css */
</style>

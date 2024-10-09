<template>
  <view
    class="navbar" 
    :style="{
      height:
        appInfoStore.getInfo().navBarHeight +
        appInfoStore.getInfo().statusBar +
        'px',
      'padding-top':appInfoStore.getInfo().statusBar + 'px',
    }"
  >
    <view class="left">
      
      <view
        class="iconfont icon-back"
        v-if="showLeft"
        @click="leftClick"
      ></view>

    </view>

    <view class="content">
        <view v-if="title">{{ title }}</view>
        <slot></slot>
      </view>

    <view class="right">
      <slot name="right"></slot>
    </view>

  </view>

  <view :style="{
    height:
      appInfoStore.getInfo().navBarHeight +
      appInfoStore.getInfo().statusBar +
      'px',}"
  ></view>

</template>

<script setup>

import { useAppInfoStore } from '@/store/appInfo';
const appInfoStore = useAppInfoStore();

const props = defineProps({
  title: {
    type: String,
  },
  showLeft: {
    type: Boolean,
    default: true,
  },
  leftClick: {
    type: Function,
  }
});

const leftClick = () => { 
  if (props.leftClick) {
    props.leftClick();
  } else {
    uni.navigateBack();
  }
}

</script>

<style lang="scss" scoped>
.navbar {
  background:linear-gradient(to right, #9060df, #6356de);
  width: 100%;
  position: fixed;
  z-index: 100;
  display: flex;
  color: white;
  justify-content: center;
  padding: 0px 10px;
  .left{
    width: 20px;
  }
  .content{
    text-align: center;
    flex: 1;
  }
  .right{
    width: 20px;
  }
}
</style>
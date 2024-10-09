<template>
	<view class="changeInfo">
		<view class="nav-box">
			<view class="title">编辑个人资料</view>
			<navigator 
			open-type="switchTab" 
			url="/pages/personal/personal" 
			class="iconfont iconfanhui icon-nav" 
			></navigator>
		</view>
		<view class="box">
			<view class="img-box">
				<image 
				class="img" 
				:src="src"
				@click="chooseImg"
				></image>
				<view class="text">点击更换头像</view>
			</view>
		</view>
		<view class="info-box">
			<navigator open-type="redirect" url="/pages/modify/modify?title=userName" class="text-box">
				<view class="left">昵称</view>
				<view class="iconfont iconchangyongicon- icon-box"></view>
				<view class="right">{{user.userName}}</view>
			</navigator>
			<navigator open-type="redirect" url="/pages/modify/modify?title=douyinId" class="text-box">
				<view class="left">手机号</view>
				<view class="iconfont iconchangyongicon- icon-box"></view>
				<view class="right">{{user.userId}}</view>
			</navigator>
			<navigator open-type="redirect" url="/pages/modify/modify?title=intrduction" class="text-box">
				<view class="left">简介</view>
				<view class="iconfont iconchangyongicon- icon-box"></view>
				<view class="right">{{user.intrduction}}</view>
			</navigator>
			<picker :range="school" @change="bindSchoolChange">
				<view class="text-box">
					<view class="left">学校</view>
					<view class="iconfont iconchangyongicon- icon-box"></view>
					<view class="right">{{user.school}}</view>	
				</view>
			</picker>
			<picker :range="sex" @change="bindSexChange">
				<view class="text-box">
					<view class="left">性别</view>
					<view class="iconfont iconchangyongicon- icon-box">	</view>
					<view class="right">{{user.sex}}</view>
				</view>
			</picker>
			<picker mode="date" :value="user.birthday"  @change="bindDateChange">
				<view class="text-box">
					<view class="left">生日</view>
					<view class="iconfont iconchangyongicon- icon-box"></view>
					<view class="right">{{user.birthday}}</view>
				</view>
			</picker>
			<picker mode="region"  @change="bindCityChange">
				<view class="text-box">
					<view class="left">地区</view>
					<view class="iconfont iconchangyongicon- icon-box"></view>
					<view class="right">{{user.city}}</view>
				</view>
			</picker>	
		</view>
	</view>
</template>
 
<script setup>
import { ref, onMounted } from 'vue';

const src = ref('../../static/pig.jpg');
const user = ref({
  userName: "张三",
  userId: "123435",
  intrduction: "我爱睡觉",
  school: "",
  sex: "",
  birthday: '',
  city: ''
});

const school = ['清华大学', '北京大学', "复旦大学", '南京大学', '华南师范大学'];
const sex = ['男', '女'];

const chooseImg = () => {
  uni.chooseImage({
    count: 1,
    sourceType: ['album'],
    sizeType: ['original', 'compressed'],
    success: (res) => {
      src.value = res.tempFilePaths[0];
    }
  });
};

const bindSchoolChange = (e) => {
  user.value.school = school[e.detail.value]; // changed from e.target.value to e.detail.value
  uni.setStorage({
    key: 'school',
    data: user.value.school,
  });
};

const bindSexChange = (e) => {
  user.value.sex = sex[e.detail.value];
  uni.setStorage({
    key: 'sex',
    data: user.value.sex,
  });
};

const bindDateChange = (e) => {
  user.value.birthday = e.detail.value; // changed from e.target.value to e.detail.value
  uni.setStorage({
    key: 'birthday',
    data: e.detail.value,
  });
};

const bindCityChange = (e) => {
  user.value.city = e.detail.value[0]; // changed from e.target.value[0] to e.detail.value[0]
  uni.setStorage({
    key: 'city',
    data: user.value.city,
  });
};

onMounted(() => {
  // 加载数据
  uni.getStorage({
    key: 'userName',
    success: (res) => {
      user.value.userName = res.data;
    }
  });
  uni.getStorage({
    key: 'userId',
    success: (res) => {
      user.value.userId = res.data;
    }
  });
  uni.getStorage({
    key: 'intrduction',
    success: (res) => {
      user.value.intrduction = res.data;
    }
  });
  uni.getStorage({
    key: 'school',
    success: (res) => {
      user.value.school = res.data;
    }
  });
  uni.getStorage({
    key: 'sex',
    success: (res) => {
      user.value.sex = res.data;
    }
  });
  uni.getStorage({
    key: 'birthday',
    success: (res) => {
      user.value.birthday = res.data;
    }
  });
  uni.getStorage({
    key: 'city',
    success: (res) => {
      user.value.city = res.data;
    }
  });
});
</script>
 
<style>
.changeInfo{
	width: 100%;
	height: 100%;
	background: #000000;
}
.nav-box{
	height: 50px;
	position: relative;
	margin: 0 auto;
	padding-top: 30px;
}
.title{
	text-align: center;
	color: #FFFFFF;
	font-size: 18px;
}
.icon-nav{
	position: absolute;
	top:30px;
	left: 10px;
	color: #FFFFFF;
}
.box{
	width: 100%;
	height: 150px;
	margin: 0 auto;
	border-top:1px solid #333333;
	border-bottom:1px solid #333333;
}
.img-box{
	text-align: center;
}
.img{
	margin-top: 20px;
	width: 70px;
	height: 70px;
	border-radius: 50%;
}
.text{
	margin-top: 13px;
	color: #999999;
	font-size: 13px;
}
.info-box{
	padding:0 10px;
}
.text-box{
	width: 100%;
	height: 52px;
	line-height: 52px;
	
}
.left{
	float: left;
	font-size: 15px;
	color: #FFFFFF;
}
.right{
	float: right;
	font-size: 15px;
	margin-right: 7px;
	color: #999999;
}
.icon-box{
	float: right;
	font-size: 15px;
	color:  #999999;
	width: 10px;
}
</style>
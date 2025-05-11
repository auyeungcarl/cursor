<template>
	<view class="page">
		<!-- App导航栏 -->
		<view class="app-bar">
		</view>
		<!-- 页面内容 -->
		<view class="main-content">
			<image class="logo" src="/static/logo.png"></image>
			<view class="text-area">
				<text class="title">{{title}}</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: 'Hello'
			}
		},
		onLoad() {

		},
		methods: {
			// 跳转到登录页面
			// goToMine() {
			// 	uni.navigateTo({ url: '/pages/login/login' });
			// }
		}
	}
</script>

<style>
	.page {
		min-height: 100vh;
		background: #fff;
		display: flex;
		flex-direction: column;
	}
	.app-bar {
		height: 80rpx;
		background: #fff;
		display: flex;
		align-items: center;
		justify-content: center;
		border-bottom: 1rpx solid #eee;
	}
	.app-title {
		font-size: 32rpx;
		color: #222;
		font-weight: bold;
	}
	.main-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-bottom: 40rpx;
		border-radius: 40rpx;
	}
	.text-area {
		display: flex;
		justify-content: center;
	}
	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
</style>

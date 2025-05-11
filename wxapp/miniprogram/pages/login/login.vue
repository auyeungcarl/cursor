<template>
	<view class="login-page">
		<!-- Logo和品牌名 -->
		<view class="logo-section">
			<image class="logo" src="/static/logo.png" mode="aspectFit"></image>
			<view class="brand-name">ZhenXuanZe 臻选选择</view>
			<view class="brand-slogan">产品优选 商品连锁</view>
		</view>

		<!-- 按钮区 -->
		<view class="button-section">
			<button class="login-btn" @click="handleLogin" :disabled="!agree">授权登录</button>
			<button class="home-btn" @click="goHome">返回首页</button>
		</view>

		<!-- 协议勾选区 -->
		<view class="protocol-section">
			<label class="checkbox-label">
				<checkbox :checked="agree" @click.stop="agree = !agree" color="#f44" style="transform:scale(0.8)"/>
				<text>同意</text>
				<text class="protocol-link" @click.stop="openProtocol('user')">《用户协议》</text>
				<text>和</text>
				<text class="protocol-link" @click.stop="openProtocol('privacy')">《隐私政策》</text>
			</label>
		</view>
	</view>
</template>

<script>
import config from '@/config/index.js'

export default {
	data() {
		return {
			userInfo: null,
			agree: false, // 协议勾选状态
			token: '' // 存储登录token
		}
	},
	computed: {
		genderText() {
			if (!this.userInfo) return ''
			const genderMap = {
				0: '未知',
				1: '男',
				2: '女'
			}
			return genderMap[this.userInfo.gender] || '未知'
		}
	},
	methods: {
		// 返回上一页
		goBack() {
			uni.navigateBack()
		},
		// 返回首页
		goHome() {
			uni.reLaunch({ url: '/pages/index/index' })
		},
		// 打开协议页面
		openProtocol(type) {
			// 这里可以跳转到协议详情页
			if (type === 'user') {
				uni.navigateTo({ url: '/pages/protocol/user' })
			} else {
				uni.navigateTo({ url: '/pages/protocol/privacy' })
			}
		},
		// 处理登录
		async handleLogin() {
			if (!this.agree) {
				uni.showToast({ title: '请先同意协议', icon: 'none' })
				return
			}
			try {
				uni.showLoading({ title: '登录中...' })
				// 只用uni.login获取code
				const loginRes = await uni.login()
				if (loginRes.errMsg !== 'login:ok') {
					throw new Error('微信登录失败')
				}

				// 调用后端登录接口
				const res = await uni.request({
					url: `${config.baseUrl}/auth/wx-login?code=${loginRes.code}`,
					method: 'POST'
				})

				console.log('调用后端登录接口：', res)
				if (res.statusCode === 200 && res.data.code === 200) {
					// 保存token
					uni.setStorageSync('token', res.data.data.token)
					// 设置登录状态
					uni.setStorageSync('isLogin', true)
					// 跳转到个人中心页
					uni.switchTab({
						url: '/pages/userinfo/profile'
					})
				} else {
					throw new Error(res.data.msg || '登录失败')
				}
			} catch (error) {
				console.error('登录失败：', error)
				uni.showToast({
					title: error.message || '登录失败，请重试',
					icon: 'none'
				})
			}
		},
		formatRegion(userInfo) {
			if (!userInfo) return ''
			return [userInfo.country, userInfo.province, userInfo.city].filter(Boolean).join(' ')
		},
		// 主动获取微信头像昵称
		async getWxProfile() {
			try {
				const res = await uni.getUserProfile({ desc: '用于完善用户资料' })
				if (res && res.userInfo) {
					// 只更新头像和昵称
					this.userInfo.avatarUrl = res.userInfo.avatarUrl
					this.userInfo.nickName = res.userInfo.nickName
					// 存储到本地
					let stored = uni.getStorageSync('userInfo') || {}
					stored.avatarUrl = res.userInfo.avatarUrl
					stored.nickName = res.userInfo.nickName
					uni.setStorageSync('userInfo', stored)
				}
			} catch (e) {
				uni.showToast({ title: '用户取消授权', icon: 'none' })
			}
		},
		// 获取手机号
		async getPhoneNumber(e) {
			console.log('开始获取手机号，事件详情：', e.detail)
			
			if (e.detail.errMsg !== 'getPhoneNumber:ok') {
				uni.showToast({ title: '获取手机号失败', icon: 'none' })
				return
			}
			
			try {
				uni.showLoading({ title: '更新手机号...' })
				// 直接使用微信返回的手机号
				const phoneNumber = e.detail.phoneNumber
				
				// 更新本地用户信息
				this.userInfo.phoneNumber = phoneNumber
				uni.setStorageSync('userInfo', this.userInfo)
				
				// 调用更新用户信息接口
				await this.updateUserInfo()
				
				uni.hideLoading()
				uni.showToast({ title: '手机号更新成功', icon: 'success' })
				setTimeout(() => {
					uni.reLaunch({ url: '/pages/userinfo/profile' })
				}, 1000)
			} catch (error) {
				console.error('获取手机号失败：', error)
				uni.hideLoading()
				uni.showModal({
					title: '获取手机号失败',
					content: error.message || '请稍后重试',
					showCancel: false
				})
			} finally {
				this.showPhoneButton = false
			}
		},
		
		// 更新用户信息
		async updateUserInfo() {
			try {
				const res = await uni.request({
					url: `${config.baseUrl}/user/updateUserInfo`,
					method: 'PUT',
					header: {
						'Authorization': `Bearer ${this.token}`
					},
					data: this.userInfo
				})
				
				if (res.statusCode !== 200) throw new Error('更新用户信息失败')
				return res.data.data
			} catch (error) {
				console.error('更新用户信息失败：', error)
				throw error
			}
		}
	}
}
</script>

<style lang="scss">
.login-page {
	min-height: 100vh;
	background: #fff;
}
.logo-section {
	display: flex;
	flex-direction: column;
	align-items: center;
	margin: 60rpx 0 40rpx 0;
	.logo {
		width: 200rpx;
		height: 200rpx;
		margin-bottom: 20rpx;
	}
	.brand-name {
		font-size: 40rpx;
		font-weight: bold;
		color: #b22222;
		margin-bottom: 10rpx;
	}
	.brand-slogan {
		font-size: 28rpx;
		color: #888;
	}
}
.button-section {
	display: flex;
	flex-direction: column;
	align-items: center;
	margin: 40rpx 0 20rpx 0;
	.login-btn {
		width: 80vw;
		background: #f44;
		color: #fff;
		border-radius: 50rpx;
		font-size: 34rpx;
		margin-bottom: 30rpx;
	}
	.home-btn {
		width: 80vw;
		background: #fff;
		color: #f44;
		border: 2rpx solid #f44;
		border-radius: 50rpx;
		font-size: 34rpx;
	}
}
.protocol-section {
	display: flex;
	justify-content: center;
	margin-top: 30rpx;
	.checkbox-label {
		display: flex;
		align-items: center;
		font-size: 28rpx;
		color: #333;
		.protocol-link {
			color: #f44;
			margin: 0 6rpx;
			text-decoration: underline;
		}
	}
}
.user-info-box {
	margin-top: 40rpx;
	padding: 30rpx;
	background-color: #f8f8f8;
	border-radius: 12rpx;

	.avatar-box {
		display: flex;
		justify-content: center;
		margin-bottom: 30rpx;

		.avatar {
			width: 150rpx;
			height: 150rpx;
			border-radius: 75rpx;
		}
	}

	.info-list {
		.info-item {
			display: flex;
			margin-bottom: 20rpx;
			font-size: 28rpx;
			line-height: 1.5;

			.label {
				color: #666;
				width: 120rpx;
			}

			.value {
				color: #333;
				flex: 1;
			}
		}
	}
}
.avatar-btn {
	width: 60vw;
	background: #f5f5f5;
	color: #f44;
	border-radius: 50rpx;
	font-size: 28rpx;
	margin: 0 auto;
	border: 2rpx solid #f44;
}
.arrow-icon {
	color: #f44;
	font-size: 32rpx;
	margin-left: 16rpx;
	cursor: pointer;
}
.phone-value {
	word-break: break-all;
	font-size: 28rpx;
	color: #333;
}
.phone-btn {
	width: 80vw;
	background: #f44;
	color: #fff;
	border-radius: 50rpx;
	font-size: 34rpx;
	margin: 20rpx auto;
}
</style> 
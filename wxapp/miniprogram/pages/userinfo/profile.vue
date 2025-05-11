<template>
  <view class="profile-page">
    <!-- 顶部区域：标题和用户信息 -->
    <view class="profile-header">
      <view class="profile-user-box" @click="handleUserClick">
        <view class="user-info-row">
          <image class="profile-avatar" :src="userInfo.avatarUrl || '/static/default-avatar.png'" mode="aspectFill" />
          <view class="profile-username">{{isLogin ? (userInfo.nickname || userInfo.nickName || '微信用户') : '未登录'}}</view>
          <button class="profile-edit-btn" size="mini" plain v-if="isLogin" @click.stop="goToUserInfo">修改信息</button>
        </view>
      </view>
    </view>

    <!-- 用户类型与权益区 -->
    <view class="profile-benefit-box">
      <view class="benefit-item">
        <text class="benefit-icon vip">VIP</text>
        <text class="benefit-label">普通用户</text>
      </view>
      <view class="benefit-item">
        <text class="benefit-label">会员权益</text>
        <text class="benefit-action">领取福利</text>
      </view>
      <view class="benefit-item">
        <text class="benefit-label">卡券</text>
        <text class="benefit-count">0</text>
      </view>
    </view>

    <!-- 我的订单区 -->
    <view class="profile-section">
      <view class="section-title">我的订单</view>
      <view class="order-list">
        <view class="order-item">
          <image class="order-icon" src="/static/order-pay.png" />
          <text>待付款</text>
          <view class="order-badge">2</view>
        </view>
        <view class="order-item">
          <image class="order-icon" src="/static/order-send.png" />
          <text>待发货</text>
        </view>
        <view class="order-item">
          <image class="order-icon" src="/static/order-receive.png" />
          <text>待收货</text>
        </view>
        <view class="order-item">
          <image class="order-icon" src="/static/order-comment.png" />
          <text>待评价</text>
        </view>
        <view class="order-item">
          <image class="order-icon" src="/static/order-all.png" />
          <text>全部订单</text>
        </view>
      </view>
    </view>

    <!-- 我的服务区 -->
    <view class="profile-section">
      <view class="section-title">我的服务</view>
      <view class="service-list">
        <view class="service-item">
          <image class="service-icon" src="/static/service-main.png" />
          <text>主产品订单</text>
        </view>
        <view class="service-item">
          <image class="service-icon" src="/static/service-vip.png" />
          <text>VIP订单</text>
        </view>
        <view class="service-item">
          <image class="service-icon" src="/static/service-fav.png" />
          <text>我的收藏</text>
        </view>
        <view class="service-item">
          <image class="service-icon" src="/static/service-group.png" />
          <text>我的团购</text>
        </view>
      </view>
    </view>

    <!-- 分享与管理区 -->
    <view class="profile-section">
      <view class="service-list">
        <view class="service-item">
          <image class="service-icon" src="/static/service-share.png" />
          <text>我的分享</text>
        </view>
        <view class="service-item">
          <image class="service-icon" src="/static/service-address.png" />
          <text>地址管理</text>
        </view>
        <view class="service-item">
          <image class="service-icon" src="/static/service-about.png" />
          <text>关于我们</text>
        </view>
      </view>
    </view>

    <!-- 退出登录按钮 -->
    <view class="logout-box" v-if="isLogin">
      <button class="logout-btn" type="warn" @click="handleLogout">退出登录</button>
    </view>
  </view>
</template>

<script>
import config from '@/config/index.js'

export default {
  name: 'ProfilePage',
  data() {
    return {
      isLogin: false,
      userInfo: {}
    }
  },
  onShow() {
    // 每次页面显示时检查登录状态
    this.checkLoginStatus()
  },
  methods: {
    async checkLoginStatus() {
      const token = uni.getStorageSync('token')
      const isLogin = !!token
      this.isLogin = isLogin
      
      if (isLogin) {
        // 获取最新的用户信息
        try {
          const res = await uni.request({
            url: `${config.baseUrl}/user/getUserInfo`,
            method: 'GET',
            header: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          })
          
          if (res.statusCode === 200 && res.data.code === 200) {
            const userData = res.data.data
            this.userInfo = {
              ...userData,
              nickName: userData.nickname || userData.nickName || '微信用户'
            }
            // 更新本地存储
            uni.setStorageSync('userInfo', this.userInfo)
          }
        } catch (error) {
          console.error('获取用户信息失败：', error)
        }
      } else {
        this.userInfo = {}
      }
    },
    handleUserClick() {
      if (!this.isLogin) {
        uni.navigateTo({
          url: '/pages/login/login'
        })
      }
    },
    goToUserInfo() {
      uni.navigateTo({
        url: '/pages/userinfo/userinfo'
      })
    },
    handleLogout() {
      uni.showModal({
        title: '提示',
        content: '确定要退出登录吗？',
        success: (res) => {
          if (res.confirm) {
            // 清空本地存储的用户信息
            uni.removeStorageSync('isLogin')
            uni.removeStorageSync('userInfo')
            // 更新页面状态
            this.isLogin = false
            this.userInfo = {}
            // 提示用户
            uni.showToast({
              title: '已退出登录',
              icon: 'success'
            })
          }
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100vh;
  background: #fff;
  padding-bottom: 40rpx;
}
.profile-header {
  background: #f33;
  color: #fff;
  padding: 75rpx 0 180rpx 0;
  text-align: center;
  .profile-user-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 20rpx;
    .user-info-row {
      display: flex;
      align-items: center;
      width: 100%;
      padding: 0 40rpx;
      position: relative;
    }
    .profile-avatar {
      width: 140rpx;
      height: 140rpx;
      border-radius: 70rpx;
      background: #eee;
      position: absolute;
      left: 90rpx;
      border: 4rpx solid rgba(255, 255, 255, 0.8);
    }
    .profile-username {
      font-size: 36rpx;
      position: absolute;
      left: 250rpx;
      font-weight: 500;
      line-height: 1.4;
    }
    .profile-info {
      font-size: 28rpx;
      position: absolute;
      left: 250rpx;
      top: 60rpx;
      color: rgba(255, 255, 255, 0.9);
      line-height: 1.4;
    }
    .profile-edit-btn {
      font-size: 30rpx;
      color: #f33;
      background: #fff;
      border: 1rpx solid #f33;
      border-radius: 20rpx;
      padding: 8rpx 28rpx;
      margin: 0;
      position: absolute;
      right: 90rpx;
      line-height: 1.5;
      top: 50%;
      transform: translateY(-50%);
    }
  }
}
.profile-benefit-box {
  display: flex;
  justify-content: space-around;
  background: #fff;
  margin: -80rpx 20rpx 30rpx 20rpx;
  border-radius: 30rpx;
  box-shadow: 0 2rpx 8rpx #f3f3f3;
  padding: 40rpx 0;
  .benefit-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    .benefit-icon.vip {
      color: #f90;
      font-weight: bold;
      font-size: 32rpx;
      margin-bottom: 12rpx;
    }
    .benefit-label {
      font-size: 28rpx;
      color: #333;
      margin-bottom: 8rpx;
    }
    .benefit-action {
      color: #f33;
      font-size: 26rpx;
      margin-top: 4rpx;
    }
    .benefit-count {
      color: #f33;
      font-size: 26rpx;
      margin-top: 4rpx;
    }
  }
}
.profile-section {
  margin: 30rpx 20rpx 0 20rpx;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx #f3f3f3;
  padding: 30rpx 0 0 0;
  .section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #222;
    margin-left: 30rpx;
    margin-bottom: 20rpx;
  }
  .order-list, .service-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    padding-bottom: 30rpx;
  }
  .order-item, .service-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 16rpx 0;
    position: relative;
    .order-icon, .service-icon {
      width: 64rpx;
      height: 64rpx;
      margin-bottom: 10rpx;
    }
    text {
      font-size: 26rpx;
      color: #333;
    }
    .order-badge {
      position: absolute;
      top: 0;
      right: 10rpx;
      background: #f33;
      color: #fff;
      font-size: 22rpx;
      border-radius: 20rpx;
      padding: 2rpx 8rpx;
    }
  }
}
.logout-box {
  margin: 40rpx 40rpx 0 40rpx;
  .logout-btn {
    width: 100%;
    background: #fff;
    color: #f33;
    border: 2rpx solid #f33;
    border-radius: 30rpx;
    font-size: 30rpx;
    font-weight: bold;
    margin-top: 20rpx;
  }
}
</style> 
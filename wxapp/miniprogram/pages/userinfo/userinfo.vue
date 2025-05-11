<template>
  <view class="userinfo-page">
    <view class="user-info-box" v-if="userInfo">
      <view class="avatar-box" @click="chooseAvatar">
        <image class="avatar" :src="userInfo.avatarUrl" mode="aspectFill"></image>
        <view class="avatar-edit">
          <text class="edit-icon">📷</text>
        </view>
      </view>
      <view class="info-list">
        <view class="info-item">
          <text class="label">昵称：</text>
          <view class="value-wrapper">
            <input 
              class="value input" 
              type="text" 
              v-model="userInfo.nickname" 
              placeholder="请输入昵称" 
              maxlength="20"
              @blur="saveUserInfo"
            />
          </view>
        </view>
        <view class="info-item">
          <text class="label">手机号：</text>
          <view class="value-wrapper">
            <input 
              class="value input" 
              type="number" 
              v-model="userInfo.phone" 
              placeholder="请输入手机号" 
              maxlength="11"
              @blur="validateAndSavePhone"
            />
          </view>
        </view>
        <view class="info-item">
          <text class="label">性别：</text>
          <view class="value-wrapper">
            <picker 
              class="value picker" 
              mode="selector" 
              :range="genderOptions" 
              range-key="label" 
              :value="genderIndex" 
              @change="handleGenderChange"
            >
              <view class="picker-text">{{genderText}}</view>
            </picker>
          </view>
        </view>
        <view class="info-item">
          <text class="label">地区：</text>
          <view class="value-wrapper">
            <picker 
              class="value picker" 
              mode="region" 
              @change="handleRegionChange"
            >
              <view class="picker-text">{{ formatRegion(userInfo) || '请选择地区' }}</view>
            </picker>
          </view>
        </view>
      </view>
    </view>
    <view class="save-btn-wrapper">
      <button class="save-btn" @tap="handleSave">保存修改</button>
    </view>
  </view>
</template>

<script>
import config from '@/config/index.js'

export default {
  data() {
    return {
      userInfo: null,
      genderOptions: [
        { label: '未知', value: 0 },
        { label: '男', value: 1 },
        { label: '女', value: 2 }
      ]
    }
  },
  computed: {
    genderText() {
      if (!this.userInfo) return '未知'
      const genderMap = { 0: '未知', 1: '男', 2: '女' }
      return genderMap[this.userInfo.gender] || '未知'
    },
    genderIndex() {
      if (!this.userInfo) return 0
      return this.genderOptions.findIndex(item => item.value === this.userInfo.gender)
    }
  },
  methods: {
    formatRegion(userInfo) {
      if (!userInfo) return ''
      // 按照省市区顺序展示
      return [userInfo.province, userInfo.city, userInfo.country].filter(Boolean).join(' ')
    },
    async getWxProfile() {
      try {
        const res = await uni.getUserProfile({ desc: '用于完善用户资料' })
        if (res && res.userInfo) {
          this.userInfo.avatarUrl = res.userInfo.avatarUrl
          this.userInfo.nickName = res.userInfo.nickName
          this.saveUserInfo()
        }
      } catch (e) {
        uni.showToast({ title: '用户取消授权', icon: 'none' })
      }
    },
    handleGenderChange(e) {
      const index = e.detail.value
      this.userInfo.gender = this.genderOptions[index].value
      this.saveUserInfo()
    },
    handleRegionChange(e) {
      const [province, city, country] = e.detail.value
      this.userInfo.province = province
      this.userInfo.city = city
      this.userInfo.country = country
      this.saveUserInfo()
    },
    validateAndSavePhone() {
      if (this.userInfo.mobile && !/^1[3-9]\d{9}$/.test(this.userInfo.mobile)) {
        uni.showToast({ title: '请输入正确的手机号', icon: 'none' })
        this.userInfo.mobile = ''
        return
      }
      this.saveUserInfo()
    },
    saveUserInfo() {
      uni.setStorageSync('userInfo', this.userInfo)
    },
    chooseAvatar() {
      uni.showActionSheet({
        itemList: ['拍照', '从相册选择'],
        success: (res) => {
          const sourceType = res.tapIndex === 0 ? ['camera'] : ['album']
          uni.chooseImage({
            count: 1,
            sourceType: sourceType,
            success: (res) => {
              const tempFilePath = res.tempFilePaths[0]
              // 上传图片到服务器
              this.uploadAvatar(tempFilePath)
            }
          })
        }
      })
    },
    uploadAvatar(filePath) {
      // 这里应该调用上传接口，将图片上传到服务器
      // 示例代码，实际使用时需要替换为真实的上传接口
      uni.showLoading({ title: '上传中...' })
      
      // 模拟上传过程
      setTimeout(() => {
        uni.hideLoading()
        // 更新头像
        this.userInfo.avatarUrl = filePath
        this.saveUserInfo()
        uni.showToast({ title: '头像更新成功', icon: 'success' })
      }, 1000)
    },
    async handleSave() {
      try {
        uni.showLoading({ title: '保存中...' })
        const token = uni.getStorageSync('token')
        const res = await uni.request({
          url: `${config.baseUrl}/user/updateUserInfo`,
          method: 'PUT',
          header: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          data: {
            nickname: this.userInfo.nickName,
            phone: this.userInfo.mobile,
            gender: this.userInfo.gender,
            province: this.userInfo.province,
            city: this.userInfo.city,
            country: this.userInfo.country,
            avatarUrl: this.userInfo.avatarUrl
          }
        })
        
        if (res.statusCode === 200 && res.data.code === 200) {
          uni.showToast({ title: '保存成功', icon: 'success' })
          // 更新本地存储
          this.saveUserInfo()
        } else {
          uni.showToast({ title: res.data.msg || '保存失败', icon: 'none' })
        }
      } catch (error) {
        uni.showToast({ title: '保存失败，请重试', icon: 'none' })
      } finally {
        uni.hideLoading()
      }
    },
    async getUserInfo() {
      try {
        const token = uni.getStorageSync('token')
        if (!token) {
          uni.showToast({ title: '请先登录', icon: 'none' })
          return
        }
        
        console.log('获取用户信息，token:', token)
        const res = await uni.request({
          url: `${config.baseUrl}/user/getUserInfo`,
          method: 'GET',
          header: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        
        console.log('获取用户信息响应:', res)
        if (res.statusCode === 200 && res.data.code === 200) {
          // 处理返回的用户信息，将nickname映射到nickName
          const userData = res.data.data
          this.userInfo = {
            ...userData,
            nickName: userData.nickname || userData.nickName || '未设置昵称'
          }
          // 更新本地存储
          uni.setStorageSync('userInfo', this.userInfo)
        } else {
          uni.showToast({ title: res.data.msg || '获取用户信息失败', icon: 'none' })
        }
      } catch (error) {
        console.error('获取用户信息失败：', error)
        uni.showToast({ title: '获取用户信息失败，请重试', icon: 'none' })
      }
    }
  },
  async onLoad() {
    // 先尝试从本地获取
    this.userInfo = uni.getStorageSync('userInfo') || {}
    // 然后从服务器获取最新数据
    await this.getUserInfo()
  }
}
</script>

<style lang="scss">
.userinfo-page {
  min-height: 100vh;
  background: #fff;
}
.user-info-box {
  margin: 40rpx 0 0 0;
  padding: 30rpx;
  background-color: #f8f8f8;
  border-radius: 12rpx;
}
.avatar-box {
  display: flex;
  justify-content: center;
  margin-bottom: 30rpx;
  position: relative;
  
  .avatar {
    width: 150rpx;
    height: 150rpx;
    border-radius: 75rpx;
  }
  
  .avatar-edit {
    position: absolute;
    right: 50%;
    bottom: 0;
    transform: translateX(75rpx);
    width: 40rpx;
    height: 40rpx;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 20rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    
    .edit-icon {
      color: #fff;
      font-size: 24rpx;
    }
  }
}
.info-list {
  .info-item {
    display: flex;
    align-items: center;
    margin-bottom: 20rpx;
    font-size: 28rpx;
    line-height: 1.5;
    
    .label {
      color: #666;
      width: 120rpx;
    }
    
    .value-wrapper {
      flex: 1;
      background: #fff;
      border: 1px solid #eee;
      border-radius: 8rpx;
      padding: 0 20rpx;
      height: 80rpx;
      display: flex;
      align-items: center;
      
      .value {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        
        &.input {
          border: none;
          background: transparent;
          padding: 0;
        }
        
        &.picker {
          .picker-text {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
          }
        }
      }
    }
  }
}
.save-btn-wrapper {
  padding: 40rpx 30rpx;
  
  .save-btn {
    width: 100%;
    height: 88rpx;
    line-height: 88rpx;
    text-align: center;
    background: #f44;
    color: #fff;
    border-radius: 44rpx;
    font-size: 32rpx;
    
    &:active {
      opacity: 0.8;
    }
  }
}
</style> 
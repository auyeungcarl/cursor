// 检查用户是否已登录
export const checkLogin = () => {
  const phone = uni.getStorageSync('phone')
  const userInfo = uni.getStorageSync('userInfo')
  return !!(phone && userInfo)
}

// 跳转到登录页面
export const redirectToLogin = () => {
  uni.navigateTo({
    url: '/pages/login/login'
  })
}

// 检查登录状态，如果未登录则跳转到登录页面
export const checkLoginAndRedirect = () => {
  if (!checkLogin()) {
    redirectToLogin()
    return false
  }
  return true
}

// 获取用户信息
export const getUserInfo = () => {
  return {
    phone: uni.getStorageSync('phone'),
    userInfo: uni.getStorageSync('userInfo')
  }
}

// 清除登录信息
export const clearLoginInfo = () => {
  uni.removeStorageSync('phone')
  uni.removeStorageSync('userInfo')
} 
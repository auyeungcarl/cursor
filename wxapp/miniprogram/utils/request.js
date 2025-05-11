import { checkLoginAndRedirect } from './auth'

// 配置基础URL
const BASE_URL = 'http://localhost:8080/api'; // 后端服务地址

// 请求拦截器
const requestInterceptor = (config) => {
	// 检查是否需要登录
	if (config.needLogin !== false) {
		if (!checkLoginAndRedirect()) {
			return Promise.reject(new Error('未登录'))
		}
	}
	// 获取token
	const token = uni.getStorageSync('token');
	if (token) {
		config.header = {
			...config.header,
			'Authorization': `Bearer ${token}`
		};
	}
	return config;
};

// 响应拦截器
const responseInterceptor = (response) => {
	const { statusCode, data } = response;
	
	if (statusCode === 200) {
		// 处理后端统一返回格式
		if (data.code === 200) {
			return data.data;
		}
		return Promise.reject(new Error(data.msg || '请求失败'));
	}
	
	// 处理401未授权的情况
	if (statusCode === 401) {
		uni.removeStorageSync('token');
		uni.removeStorageSync('userInfo');
		uni.showToast({
			title: '登录已过期，请重新登录',
			icon: 'none'
		});
		setTimeout(() => {
			uni.navigateTo({
				url: '/pages/login/login'
			});
		}, 1500);
		return Promise.reject(new Error('登录已过期'));
	}
	
	return Promise.reject(new Error(data.msg || '请求失败'));
};

// 将对象转换为URL参数字符串
const objectToQueryString = (obj) => {
	if (!obj) return '';
	return '?' + Object.keys(obj)
		.map(key => `${encodeURIComponent(key)}=${encodeURIComponent(obj[key])}`)
		.join('&');
};

// 封装请求方法
const request = (options) => {
	const { url, method = 'GET', data, params, header = {} } = options;
	
	// 构建完整URL（包含查询参数）
	const fullUrl = `${BASE_URL}${url}${objectToQueryString(params)}`;
	
	// 应用请求拦截器
	const config = requestInterceptor({
		url: fullUrl,
		method,
		data,
		header
	});
	
	// 如果拦截器返回了rejected promise，直接返回
	if (config instanceof Promise) {
		return config
	}
	
	return new Promise((resolve, reject) => {
		uni.request({
			...config,
			success: (res) => {
				try {
					const result = responseInterceptor(res);
					resolve(result);
				} catch (error) {
					reject(error);
				}
			},
			fail: (error) => {
				console.error('请求失败:', error);
				uni.showToast({
					title: '网络请求失败，请检查网络连接',
					icon: 'none'
				});
				reject(new Error('网络请求失败'));
			}
		});
	});
};

// 导出请求方法
export default {
	get: (url, params, header) => request({ url, method: 'GET', params, header }),
	post: (url, data, header) => request({ url, method: 'POST', data, header }),
	put: (url, data, header) => request({ url, method: 'PUT', data, header }),
	delete: (url, data, header) => request({ url, method: 'DELETE', data, header })
}; 
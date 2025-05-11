package com.example.wxapp.service;

import com.example.wxapp.entity.User;

public interface UserService {
    /**
     * 微信登录
     * @param code 微信登录code
     * @return 用户信息
     */
    User wxLogin(String code);

    /**
     * 根据openId获取用户信息
     * @param openId 微信openId
     * @return 用户信息
     */
    User getByOpenId(String openId);

    /**
     * 根据ID获取用户信息
     * @param id 用户ID
     * @return 用户信息
     */
    User getById(Long id);

    /**
     * 更新用户信息
     * @param user 用户信息
     * @return 是否成功
     */
    boolean updateUser(User user);
} 
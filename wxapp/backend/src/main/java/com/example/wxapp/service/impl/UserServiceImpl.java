package com.example.wxapp.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.wxapp.entity.User;
import com.example.wxapp.mapper.UserMapper;
import com.example.wxapp.service.UserService;
import com.example.wxapp.utils.WxUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.sql.Timestamp;
import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    private final WxUtils wxUtils;


    @Override
    public User wxLogin(String code) {
        // 获取微信用户openId
        String openId = wxUtils.getOpenId(code);
        
        // 查询用户是否存在
        User user = getByOpenId(openId);
        if (user == null) {
            // 用户不存在，创建新用户
            user = new User();
            user.setOpenId(openId);
            user.setCreateTime(LocalDateTime.now());
            user.setUpdateTime(LocalDateTime.now());
            save(user);
        }
        return user;
    }

    @Override
    public User getByOpenId(String openId) {
        return getOne(new LambdaQueryWrapper<User>()
                .eq(User::getOpenId, openId));
    }

    @Override
    public User getById(Long id) {
        return super.getById(id);
    }

    @Override
    public boolean updateUser(User user) {
        return updateById(user);
    }
} 
package com.example.wxapp.service;

import com.example.wxapp.entity.User;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

/**
 * UserServiceImpl单元测试类
 * 使用Spring Boot测试环境
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class UserServiceTestV1 {

    @Autowired
    private UserService userService;

    @Test
    public void testGetByOpenId() {
        // 准备测试数据
        String openId = "xcxvcxx";

        // 执行测试
        User user = userService.getByOpenId(openId);

        // 打印结果
        System.out.println("user: " + user);
    }

    @Test
    public void testGetById() {
        // 准备测试数据
        Long userId = 1L;

        // 执行测试
        User user = userService.getById(userId);

        // 打印结果
        System.out.println("user: " + user);
    }

    @Test
    public void testUpdateUser() {
        // 准备测试数据
        User user = new User();
        user.setId(1L);
        user.setNickname("测试用户");

        // 执行测试
        boolean result = userService.updateUser(user);

        // 打印结果
        System.out.println("update result: " + result);
    }
}
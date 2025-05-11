package com.example.wxapp.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.example.wxapp.entity.User;
import com.example.wxapp.mapper.UserMapper;
import com.example.wxapp.service.impl.UserServiceImpl;
import com.example.wxapp.utils.WxUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.powermock.api.mockito.PowerMockito;
import org.powermock.core.classloader.annotations.PrepareForTest;
import org.powermock.modules.junit4.PowerMockRunner;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * UserServiceImpl单元测试类
 */
@RunWith(PowerMockRunner.class)
@PrepareForTest({UserServiceImpl.class, UserMapper.class})
public class UserServiceTest {

    private UserServiceImpl userService;
    
    @Mock
    private UserMapper userMapper;

    @Mock
    private WxUtils wxUtils;

    @Before
    public void setUp() throws Exception {
        // 创建被测试类的实例
        userService = new UserServiceImpl(wxUtils);
        
        // 创建mock对象
        userMapper = PowerMockito.mock(UserMapper.class);
        
        // 注入mock对象到父类
        PowerMockito.field(UserServiceImpl.class, "baseMapper").set(userService, userMapper);
    }

    @Test
    public void testWxLogin_NewUser() throws Exception {
        // 准备测试数据
        String code = "test_code";
        String openId = "test_open_id";
        User expectedUser = new User();
        expectedUser.setOpenId(openId);

        // 设置mock行为
        when(wxUtils.getOpenId(code)).thenReturn(openId);
        when(userMapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(null);
        when(userMapper.insert(any(User.class))).thenReturn(1);

        // 执行测试
        User result = userService.wxLogin(code);

        // 验证结果
        assertNotNull(result);
        assertEquals(openId, result.getOpenId());
        verify(wxUtils).getOpenId(code);
        verify(userMapper).selectOne(any(LambdaQueryWrapper.class));
        verify(userMapper).insert(any(User.class));
    }

    @Test
    public void testWxLogin_ExistingUser() throws Exception {
        // 准备测试数据
        String code = "test_code";
        String openId = "test_open_id";
        User existingUser = new User();
        existingUser.setId(1L);
        existingUser.setOpenId(openId);
        existingUser.setNickname("测试用户");

        // 设置mock行为
        when(wxUtils.getOpenId(code)).thenReturn(openId);
        when(userMapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(existingUser);

        // 执行测试
        User result = userService.wxLogin(code);

        // 验证结果
        assertNotNull(result);
        assertEquals(existingUser.getId(), result.getId());
        assertEquals(existingUser.getOpenId(), result.getOpenId());
        assertEquals(existingUser.getNickname(), result.getNickname());
        verify(wxUtils).getOpenId(code);
        verify(userMapper).selectOne(any(LambdaQueryWrapper.class));
        verify(userMapper, never()).insert(any(User.class));
    }

    @Test
    public void testGetByOpenId() {
        // 准备测试数据
        String openId = "test_open_id";
        User expectedUser = new User();
        expectedUser.setId(1L);
        expectedUser.setOpenId(openId);
        expectedUser.setNickname("测试用户");

        // 设置mock行为
        when(userMapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(expectedUser);

        // 执行测试
        User result = userService.getByOpenId(openId);

        // 验证结果
        assertNotNull(result);
        assertEquals(expectedUser.getId(), result.getId());
        assertEquals(expectedUser.getOpenId(), result.getOpenId());
        assertEquals(expectedUser.getNickname(), result.getNickname());
        verify(userMapper).selectOne(any(LambdaQueryWrapper.class));
    }

    @Test
    public void testGetById() {
        // 准备测试数据
        Long userId = 1L;
        User expectedUser = new User();
        expectedUser.setId(userId);
        expectedUser.setNickname("测试用户");

        // 设置mock行为
        when(userMapper.selectById(userId)).thenReturn(expectedUser);

        // 执行测试
        User result = userService.getById(userId);

        // 验证结果
        assertNotNull(result);
        assertEquals(expectedUser.getId(), result.getId());
        assertEquals(expectedUser.getNickname(), result.getNickname());
        verify(userMapper).selectById(userId);
    }

    @Test
    public void testUpdateUser() {
        // 准备测试数据
        User user = new User();
        user.setId(1L);
        user.setNickname("新昵称");

        // 设置mock行为
        when(userMapper.updateById(user)).thenReturn(1);

        // 执行测试
        boolean result = userService.updateUser(user);

        // 验证结果
        assertTrue(result);
        verify(userMapper).updateById(user);
    }

    @Test
    public void testUpdateUser_Failed() {
        // 准备测试数据
        User user = new User();
        user.setId(1L);
        user.setNickname("新昵称");

        // 设置mock行为
        when(userMapper.updateById(user)).thenReturn(0);

        // 执行测试
        boolean result = userService.updateUser(user);

        // 验证结果
        assertFalse(result);
        verify(userMapper).updateById(user);
    }
} 
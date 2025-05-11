package com.example.wxapp.controller;

import com.example.wxapp.common.Result;
import com.example.wxapp.entity.User;
import com.example.wxapp.service.UserService;
import com.example.wxapp.utils.JwtUtils;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;

@Api(tags = "用户接口")
@RestController
@RequestMapping("/user")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    private final JwtUtils jwtUtils;

    @ApiOperation("获取用户信息")
    @GetMapping("/getUserInfo")
    public Result<User> getUserInfo(
            @ApiParam(value = "认证token", required = true)
            @RequestHeader("Authorization") String token) {
        // 从token中获取用户ID
        Long userId = jwtUtils.getUserIdFromToken(token.replace("Bearer ", ""));
        
        // 获取用户信息
        User user = userService.getById(userId);
        return Result.success(user);
    }

    @ApiOperation("更新用户信息")
    @PutMapping("/updateUserInfo")
    public Result<Boolean> updateUserInfo(
            @ApiParam(value = "认证token", required = true)
            @RequestHeader("Authorization") String token,
            @ApiParam(value = "用户信息", required = true)
            @RequestBody User user) {
        // 从token中获取用户ID
        Long userId = jwtUtils.getUserIdFromToken(token.replace("Bearer ", ""));
        user.setId(userId);
        user.setUpdateTime(LocalDateTime.now());
        // 更新用户信息
        boolean success = userService.updateUser(user);
        return Result.success(success);
    }
} 
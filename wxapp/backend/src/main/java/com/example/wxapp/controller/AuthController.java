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

import java.util.HashMap;
import java.util.Map;

@Api(tags = "认证接口")
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final UserService userService;
    private final JwtUtils jwtUtils;

    @ApiOperation("微信登录")
    @RequestMapping("/wx-login" )
    public Result<Map<String, Object>> wxLogin(
            @ApiParam(value = "微信登录凭证", required = true)
            @RequestParam String code) {
        // 微信登录
        User user = userService.wxLogin(code);
        
        // 生成token
        String token = jwtUtils.generateToken(user.getId());
        
        // 返回结果
        Map<String, Object> result = new HashMap<>();
        result.put("token", token);
        result.put("userInfo", user);
        
        return Result.success(result);
    }
} 
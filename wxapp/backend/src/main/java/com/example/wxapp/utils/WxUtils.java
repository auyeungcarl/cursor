package com.example.wxapp.utils;

import cn.hutool.http.HttpUtil;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class WxUtils {

    @Value("${wx.appid}")
    private String appid;

    @Value("${wx.secret}")
    private String secret;

    private static final String WX_CODE2SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session";

    /**
     * 获取微信用户openId
     * @param code 微信登录code
     * @return openId
     */
    public String getOpenId(String code) {
        String url = WX_CODE2SESSION_URL + "?appid=" + appid + "&secret=" + secret + "&js_code=" + code + "&grant_type=authorization_code";
        String response = HttpUtil.get(url);
        JSONObject json = JSONUtil.parseObj(response);
        if (json.containsKey("errcode") && json.getInt("errcode") != 0) {
            throw new RuntimeException("获取openId失败：" + json.getStr("errmsg"));
        }
        return json.getStr("openid");
    }
} 
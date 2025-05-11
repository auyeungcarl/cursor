package com.example.wxapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.mybatis.spring.annotation.MapperScan;

@SpringBootApplication
@MapperScan("com.example.wxapp.mapper")
public class WxAppApplication {
    public static void main(String[] args) {
        SpringApplication.run(WxAppApplication.class, args);
    }
} 
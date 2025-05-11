package com.example.wxapp.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.wxapp.entity.User;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserMapper extends BaseMapper<User> {
} 
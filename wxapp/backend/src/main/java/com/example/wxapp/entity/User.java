package com.example.wxapp.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("user")
@ApiModel(description = "用户实体")
public class User {
    @ApiModelProperty(value = "用户ID", example = "1")
    @TableId(type = IdType.AUTO)
    private Long id;

    @ApiModelProperty(value = "微信openId", example = "oX8Yt5J...")
    private String openId;

    @ApiModelProperty(value = "手机号", example = "oX8Yt5J...")
    private String phone;

    @ApiModelProperty(value = "用户昵称", example = "张三")
    private String nickname;

    @ApiModelProperty(value = "头像URL", example = "https://example.com/avatar.jpg")
    private String avatarUrl;

    @ApiModelProperty(value = "性别：0-未知，1-男，2-女", example = "1")
    private Integer gender;

    @ApiModelProperty(value = "国家", example = "中国")
    private String country;

    @ApiModelProperty(value = "省份", example = "广东")
    private String province;

    @ApiModelProperty(value = "城市", example = "深圳")
    private String city;

    @ApiModelProperty(value = "创建时间", example = "2024-01-01 12:00:00")
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    @ApiModelProperty(value = "更新时间", example = "2024-01-01 12:00:00")
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;

    @ApiModelProperty(value = "是否删除：0-未删除，1-已删除", example = "0")
    @TableLogic
    private Integer deleted;
} 
-- 创建用户表
CREATE TABLE IF NOT EXISTS `user` (
    `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `open_id` varchar(64) NOT NULL COMMENT '微信openId',
    `phone` varchar(64) DEFAULT NULL COMMENT '手机号',
    `nickname` varchar(32) DEFAULT NULL COMMENT '用户昵称',
    `avatar_url` varchar(255) DEFAULT NULL COMMENT '头像URL',
    `gender` tinyint DEFAULT '0' COMMENT '性别(0:未知,1:男,2:女)',
    `country` varchar(32) DEFAULT NULL COMMENT '国家',
    `province` varchar(32) DEFAULT NULL COMMENT '省份',
    `city` varchar(32) DEFAULT NULL COMMENT '城市',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除,1:已删除)',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_open_id` (`open_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表'; 
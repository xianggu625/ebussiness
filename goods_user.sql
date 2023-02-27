/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 110000
 Source Host           : localhost:3306
 Source Schema         : ebusiness

 Target Server Type    : MySQL
 Target Server Version : 110000
 File Encoding         : 65001

 Date: 10/02/2023 15:01:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for goods_user
-- ----------------------------
DROP TABLE IF EXISTS `goods_user`;
CREATE TABLE `goods_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `password` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of goods_user
-- ----------------------------
INSERT INTO `goods_user` VALUES (1, 'linda', '24c8f01350b011f4388a729d3d3c5fd9c0027bb95c3bb3a6f5b26636391a859f', 'cindy@126.com');
INSERT INTO `goods_user` VALUES (2, 'cindy', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'cindy@126.com');
INSERT INTO `goods_user` VALUES (3, 'jerry', '481f6cc0511143ccdd7e2d1b1b94faf0a700a8b49cd13922a70b5ae28acaa8c5', 'cindy@126.com');
INSERT INTO `goods_user` VALUES (4, 'susan', '9e69e7e29351ad837503c44a5971edebc9b7e6d8601c89c284b1b59bf37afa80', 'cindy@126.com');
INSERT INTO `goods_user` VALUES (5, 'peter', '87c3bbd5b9a829bef126aeeb3ba9949b4aa168b1320a4349afee66ea624a28f9', 'cindy@126.com');

SET FOREIGN_KEY_CHECKS = 1;

## 主要功能
1. 用户认证
   - 微信小程序登录
   - JWT token生成与验证
2. 用户管理
   - 用户信息获取
   - 用户信息更新

## API接口
### 认证接口
- POST /auth/wx-login：微信小程序登录
  - 请求参数：code（微信登录code）
  - 返回：token和用户信息

### 用户接口
- GET /user/info：获取用户信息
  - 请求头：Authorization: Bearer {token}
  - 返回：用户详细信息

- PUT /user/info：更新用户信息
  - 请求头：Authorization: Bearer {token}
  - 请求体：用户信息对象
  - 返回：更新后的用户信息

## 开发环境要求
- JDK 1.8+
- Maven 3.6+
- MySQL 8.0+
- Redis 6.0+

## 快速开始
1. 克隆项目
2. 配置数据库
   - 创建数据库
   - 修改application-dev.yml中的数据库配置
3. 运行项目
   ```bash
   mvn spring-boot:run
   ```

## 部署说明
1. 打包
   ```bash
   mvn clean package
   ```
2. 运行jar包
   ```bash
   java -jar target/wxapp-1.0.0.jar
   ```

## 注意事项
1. 请确保配置文件中的敏感信息（如数据库密码、Redis密码等）在生产环境中使用加密配置
2. 建议使用环境变量或配置中心管理不同环境的配置
3. 生产环境部署时请修改JWT密钥

## 开发规范
1. 代码规范
   - 遵循阿里巴巴Java开发手册
   - 使用Lombok简化代码
2. 接口规范
   - RESTful API设计规范
   - 统一响应格式
3. 注释规范
   - 类注释：说明类的用途
   - 方法注释：说明方法的功能、参数、返回值

## 单元测试
1. 测试框架
   - JUnit 4
   - PowerMock
   - Mockito

2. 测试规范
   - 所有Service层方法必须编写单元测试
   - 测试类命名规范：被测试类名 + Test
   - 测试方法命名规范：test + 被测试方法名
   - 每个测试方法必须包含：准备数据、执行测试、验证结果三个步骤

3. 运行测试
   ```bash
   mvn test
   ```

4. PowerMock使用示例
   ```java
   @RunWith(PowerMockRunner.class)
   @PrepareForTest(被测试类.class)
   public class 测试类 {
       @Before
       public void setUp() {
           // 初始化测试环境
       }
       
       @Test
       public void test方法() {
           // 准备测试数据
           // 设置mock行为
           // 执行测试
           // 验证结果
       }
   }
   ```

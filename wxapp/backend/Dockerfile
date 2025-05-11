FROM  williamyeh/java8:latest
# 作者信息
MAINTAINER carl "838644308@qq.com"
# 将本地文件tmp挂载到容器
VOLUME /tmp
# 拷贝jar
RUN mkdir appsystems
ADD target/*.jar appsystems/apps/
ADD src/main/resources/*.yml appsystems/config/

# 设置暴露的端口号
#EXPOSE 8082
# 执行命令
ENTRYPOINT ["java","-jar","-Dspring.profiles.active=prd","-Dspring.config.location=appsystems/config/","appsystems/apps/netease-1.0-SNAPSHOT.jar"]
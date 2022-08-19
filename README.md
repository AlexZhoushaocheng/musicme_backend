# musicme_backend
个人实践学习项目，使用flask框架的web后端，“爬虫”功能，并没有真的自动化爬取，因为本项目的需求是实现对某个音乐的搜索，把想要的音乐下载或者保存到本地，
保存到本地为了二次使用。

数据保存使用的数据库是mariadb和minio。 

## 开发
export FLASK_ENV=development

## 功能
* 搜索：根据关键词搜索音乐
* 下载：直接下载音乐
* 收集：将音乐存储到本地数据库中

## 环境依赖
* java 用到的代理需要java环境，jdk 11测试可行。
* 浏览器驱动：
    1. chrome测试可用，但是浏览器和驱动的版本有较严格的对应关系，浏览器升级后驱动可能无效。
    2. edge浏览器可用，默认使用此项。部署新的环境时需要安装此浏览器。

## 驱动
chromedriver镜像站:[https://registry.npmmirror.com/binary.html?path=chromedriver/](https://registry.npmmirror.com/binary.html?path=chromedriver/)
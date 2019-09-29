本專案為 flask server 的 demo

## Flask

* 執行flask `python main.py`

* [Flask官網](http://flask.pocoo.org/)

* [中文官網](http://docs.jinkan.org/docs/flask/)

## 執行預備步驟
* 建立python3的virtualenv
* pip install -r requirements.txt
* 啟用`SQLite`DB相關指令
    * `flask initdb`初始化DB，產生data.db
    * `flask forge`幫DB增加初始資料
    * `flask admin`建立帳號
* `flask run`啟動server

## 部屬筆記(Nginx+Gunicorn+Supervisor)
* 主檔案位置為`/var/www/myflask`
* git clone 下載即可
### Nginx
* 設定檔案位置為`/etc/nginx/nginx.conf`
```
events {
}
http {
    server {
    listen 80;
    server_name 34.80.16.93; # 这是HOST机器的外部域名，用地址也行
            location / {
                proxy_pass http://127.0.0.1:8080; # 这里是指向 gunicorn host 的服务地址
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            }
    }
}
```
### Gunicorn
* pip install 安裝
* 執行`gunicorn -w 4 -b 127.0.0.1:8080 app:app –reload –max-requests 1`
* Supervisor代為執行
### Supervisor
* pip install 安裝
* 設定檔案位置為 ` /etc/supervisor/conf.d/myflask.conf `
```
directory=/var/www/myflask/
command=gunicorn -w 4 -b 127.0.0.1:8080 app:app –reload –max-requests 1
autostart=true
autorestart=true
stderr_logfile=/var/log/myflask.err.log
stdout_logfile=/var/log/flask.out.log
```

### 參考
* [如何使用Nginx, Gunicorn與Supervisor 部署一個Flask App](https://peterli.website/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8nginx-gunicorn%E8%88%87supervisor-%E9%83%A8%E7%BD%B2%E4%B8%80%E5%80%8Bflask-app/)
* []()

## todo
* GCP
    * 固定IP
* blueprint
* 引入docker
    * [Docker 實戰系列（一）：一步一步帶你 dockerize 你的應用](https://larrylu.blog/step-by-step-dockerize-your-app-ecd8940696f4)
    * [Docker構建nginx+uwsgi+flask映象](https://www.itread01.com/content/1546680669.html)
    * [Flask + uWSGI + nginx + mysql + Docker-compose 搭建环境](https://blog.szfszf.top/tech/flask-uwsgi-nginx-mysql-docker-compose-%E6%90%AD%E5%BB%BA%E7%8E%AF%E5%A2%83/)
* 工廠函數
* 架nginx、uWSGI、
    * [在 Ubuntu 上使用 uWSGI 和 Nginx 部署 Flask 项目](https://lufficc.com/blog/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu)
    * [Linux搭建Python web环境（nginx + flask + uwsgi)](https://www.jianshu.com/p/85692a94e99b)
    * [Supervisor安装与配置（Linux/Unix进程管理工具）](https://blog.csdn.net/xyang81/article/details/51555473)
    [nicehorse06/nginx_demo](https://github.com/nicehorse06/nginx_demo)
    * [使用Nginx和uWSGI部署Flask程序](http://www.xumenger.com/nginx-flask-python-20180331/)
    * [How To Serve Flask Applications with uWSGI and Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)
* [greyli/watchlist](https://github.com/greyli/watchlist)
    * 理解並部署GCP，[PythonAnywhere的部署上線參考](https://read.helloflask.com/c11-deploy)
    * 架nginx、uWSGI
        * [在 Ubuntu 上使用 uWSGI 和 Nginx 部署 Flask 项目](https://lufficc.com/blog/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu)
    * 執行自動單元測試
    * 增加更多功能
    * 加入並理解blueprint、工廠函數
* 參考此書 [Flask Web开发实战：入门、进阶与原理解析](http://helloflask.com/book/)
    * 參考其多項目的源碼 [helloflask](https://github.com/greyli/helloflask) 
    * [Flask Web开发实战 - 目录](http://helloflask.com/book/contents/)
* 用 flask 做一些 Slack api 的應用
    * [slack api](https://api.slack.com/)
* [[請益] 技術深化求指點：Python 或 Java？](https://www.ptt.cc/bbs/Soft_Job/M.1558755539.A.9B7.html) 
    * 參考此文章的網友`sxy67230`而有以下todo
    * 研究與nginx、uwsgit、gunicorn的部屬協作
    * 研究與docker的協作

## 其他參考的API

[Star War API](https://swapi.co/)

## 其他參考資料

* [Python Web Flask 實戰開發教學 - 簡介與環境建置](https://blog.techbridge.cc/2017/06/03/python-web-flask101-tutorial-introduction-and-environment-setup/) 此篇有講到幫 Flask 設定 script 跟 manager 幫助開發

* [化整為零的次世代網頁開發標準: WSGI](http://blog.ez2learn.com/2010/01/27/introduction-to-wsgi/) WSGI 為幫助Python跟web server溝通的橋樑

* [Flask REST demo](https://github.com/udemy-course/flask-rest-demo) 可參考

* [李辉 Flask 入门教程](https://read.helloflask.com/)

* [[Day26] 柚子放學後的網頁生活 - Flask intro](https://ithelp.ithome.com.tw/articles/10209103)

* [瓶子裡裝甚麼藥，使用Flask輕輕鬆鬆打造一個RESTful API ](https://ithelp.ithome.com.tw/users/20111432/ironman/1635)

* [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) 看起來很厲害的youtube教學

* [Explore Flask](http://exploreflask.com/en/latest/) flask最佳實踐

### API相關參考資料
* [[Python] 使用 Python 和 Flask 設計 RESTful API](https://blog.taiker.space/python-shi-yong-python-he-flask-she-ji-restful-api/)
* [REST APIs with Flask 系列教學文 [1]](https://medium.com/@twilightlau94/rest-apis-with-flask-%E7%B3%BB%E5%88%97%E6%95%99%E5%AD%B8%E6%96%87-1-5405216d3166)
* [以資料庫為開發核心，利用通用 API 玩轉後端資料存取的概念與實作](https://ithelp.ithome.com.tw/users/20111421/ironman/1615)
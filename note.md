# [李辉 Flask 入门教程](https://read.helloflask.com/)

* template_demo為簡易的執行flask與模板功能
* db_demo為簡易執行db與flask連動
* one_final_app_demo為最終watch list app模樣，主要功能都在app.py，另有單元測試
* [greyli/watchlist](https://github.com/greyli/watchlist)為作者的watch list的demo，有依功能分成不同資料夾

## 第 2 章：Hello, Flask!

`router範例移置quick_start_official底下`

### 程序发现机制
* 如果執行`flask run`，Flask會預設程式名為`app.py`或`wsgi.py`
* 如果用其他名稱，須設置環境變量`FLASK_APP`為該名稱

### 管理环境变量
* 如果檔名為預設值，不用設定`FLASK_APP`
* `FLASK_ENV`用來設置運行環境，預設為`production`，可以設置成`development`來開啟 debug mode
* 可藉由`python-dotenv`套件來專門設定環境變量

### 修改视图函数名?
* view的名稱與URL無關可以任意取
* 代表路由的 endpoint，可用來生成URL，可使用`url_for()`來生成
* `url_for()`的第一個參數就是該endpoint，view的名稱

## 第 4 章：静态文件
### 生成静态文件 URL
* `url_for`可以在template中直接使用，因為模板會帶入一些常用的函數

## 第 5 章：数据库
### 使用 SQLAlchemy 操作数据库
* 使用`SQLAlchemy`來做ORM使用，這裡下載`Flask-SQLAlchemy`，此為官方擴展包

### 创建数据库表
* 以下指令進入flask shell 並創建db
```
$ flask shell
>>> from app import db
>>> db.create_all()
```

*  以下命令可刪除表
`db.drop_all()`

### 创建、读取、更新、删除
* 跟Django orm類似，操作可參考[创建数据库模型](https://read.helloflask.com/c5-database#chuang-jian-shu-ju-ku-mo-xing)

## 第 6 章：模板优化
* 加入errorhandler裝飾器可以設定404的route

```
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    return render_template('404.html', user=user), 404  # 返回模板和状态码
```

* context_processor裝飾器可以把很常用到的變量放到模板中，需回傳dict

```
@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}
```

### 第 7 章：表单
* 表單手動驗證不可靠，如要擴展可參考套件WTForms 的擴展 [Flask-WTF](https://github.com/lepture/flask-wtf)，其中也包含CSRF功能
* CSRF防護原理為在表單裡添加一組隱藏隨機字串，同時cookie中也添加一樣的隨機字串，在提交時同事比對兩個值是否一致來判斷是否為用戶的請求

### 第 8 章：用户认证
* 實際密碼產生hash的方法
```
>>> from werkzeug.security import generate_password_hash, check_password_hash
>>> pw_hash = generate_password_hash('dog')  # 为密码 dog 生成密码散列值
>>> pw_hash  # 查看密码散列值
'pbkdf2:sha256:50000$mm9UPTRI$ee68ebc71434a4405a28d34ae3f170757fb424663dc0ca15198cb881edc0978f'
>>> check_password_hash(pw_hash, 'dog')  # 检查散列值是否对应密码 dog
True
>>> check_password_hash(pw_hash, 'cat')  # 检查散列值是否对应密码 cat
False
```

* 登入的功能主要靠`flask-login` 
* 其提供登出登入功能`login_user`、`login_required`
* 並且提供view的登入認證保護，提供裝飾器`login_required`
* 目前權限限制，登入後
    * 才可編輯電影資料
    * 才可編輯用戶資料
    * 才可看到登出功能

## 第 9 章：测试
### 單元測試
* [使用unitest來寫單元測試](https://read.helloflask.com/c9-test#dan-yuan-ce-shi)
* 測試的class需繼承`unittest.TestCase`
* class內的方法
    * `setUp()`為測試前調用
    * `tearDown()`為測試完畢調用
    * `test_`開頭的被視為測試方法
    * 會用斷言方法做測試判斷，如`self.assertEqual(rv, 'Hello!')`

* 執行`python test_watchlist.py`即可做單元測試

* 如果要進一步地知道覆蓋率可參考套件`coverage.py`

* todo，補完`pass`掉的測試功能，[第 9 章：测试](https://read.helloflask.com/c9-test)

## 第 10 章：组织你的代码

## 第 11 章：部署上线
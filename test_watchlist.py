# -*- coding: utf-8-*-
import unittest

from app import app, db, Movie, User, forge, initdb


class WatchlistTestCase(unittest.TestCase):

    def setUp(self):
        # 更新配置
        app.config.update(
            # 測試時狀態TESTING打開可以過濾一些多餘的訊息
            TESTING=True,
            # 改使用memory當作db做測試，不會用到開發時的db
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        # 用來創建db和表
        db.create_all()

        user = User(name='Test', username='test')
        user.set_password('123')
        movie = Movie(title='Test Movie Title', year='2019')
        db.session.add_all([user, movie])
        db.session.commit()

        # 創建測試客服端，來模擬瀏覽器，如果調用get()相當於對server發送GET請求
        self.client = app.test_client()
        self.runner = app.test_cli_runner()  # 創建測試命令行

    def tearDown(self):
        # 清除memory表的資料
        db.session.remove()
        # drop memory上的資料庫
        db.drop_all()

    # 測試 app 是否存在
    def test_app_exit(self):
        self.assertIsNotNone(app)

    # 測試程式是否在測試模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    # 測試404頁面
    def test_404_page(self):
        response = self.client.get('/nothing')
        # as_text設為True可得到Unicode格式的主體
        data = response.get_data(as_text=True)
        # 測試抓到的頁面有無以下資料
        self.assertIn('Page Not Found - 404', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)

    # 測試主頁
    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Test\'s Watchlist', data)
        self.assertIn('Test Movie Title', data)
        self.assertEqual(response.status_code, 200)

    # 用於測試的輔助方法，将 follow_redirects 参数设为 True 可以跟随重定向，最终返回的会是重定向后的响应
    def login(self):
        self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)

    # 測試創建條目
    def test_create_item(self):
        self.login()

        # 測試創建條目
        response = self.client.post('/', data=dict(
            title='New Movie', year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item created.', data)
        self.assertIn('New Movie', data)

        # 測試創建條目，但標題為空
        response = self.client.post('/', data=dict(
            title='', year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('New Movie', data)

        # 測試創建條目，但年份為空
        response = self.client.post('/', data=dict(
            title='New Movie',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('Invalid input.', data)

    def test_update_item(self):
        self.login()

        # 測試更新條目
        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        self.assertIn('Edit item', data)
        self.assertIn('Test Movie Title', data)
        self.assertIn('2019', data)

        # 測試更新條目操作
        response = self.client.post('/movie/edit/1', data=dict(
            title='New Movie Edited', year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item updated.', data)
        self.assertIn('New Movie Edited', data)

        # 測試更新條目操作，但電影標題為空
        response = self.client.post('/movie/edit/1', data=dict(
            title='', year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item updated.', data)
        self.assertIn('New Movie Edited', data)

        # 測試更新條目操作，但電影年份為空
        response = self.client.post('/movie/edit/1', data=dict(
            title='New Movie Edited again', year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item updated.', data)
        self.assertIn('New Movie Edited', data)

        # 測試刪除項目
    def test_delete_item(self):
        self.login()

        response = self.client.post('/movie/delete/1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item deleted.', data)
        self.assertNotIn('Test Movie Title', data)

        # 測試登入功能

        # 測試登入保護
    def test_login_protect(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertNotIn('logout', data)
        self.assertNotIn('settings', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)

        # 測試登入
    def test_login(self):
        response = self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Login success', data)
        self.assertIn('logout', data)
        self.assertIn('settings', data)
        self.assertIn('Delete', data)
        self.assertIn('Edit', data)
        self.assertIn('<form method="post">', data)

        # 測試登入使用錯誤密碼
        response = self.client.post('/login', data=dict(
            username='test',
            password='456'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password', data)

        # 测试使用错误的用户名登录
        response = self.client.post('/login', data=dict(
            username='wrong',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password', data)

        # 测试使用空的用户名登录
        response = self.client.post('/login', data=dict(
            username='',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid input', data)

        # 测试使用空的密碼登录
        response = self.client.post('/login', data=dict(
            username='test',
            password=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid input', data)

        # 測試登出
    def test_logout(self):
        self.login()
        response = self.client.post('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Goodbye.', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('settings', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('<form method="post">', data)

        # 測試設置
    def test_settings(self):
        self.login()

        # 測試設置頁面
        response = self.client.get('/settings')
        data = response.get_data(as_text=True)
        self.assertIn('Settings', data)
        self.assertIn('Your Name', data)

        # 測試更新頁面
        response = self.client.post('/settings', data=dict(
            name='Grey Li',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Settings updated.', data)
        self.assertIn('Grey Li', data)

        # 測試更新頁面，名稱為空
        response = self.client.post('/settings', data=dict(
            name='',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Settings, updated', data)
        self.assertIn('Invalid input', data)

        # 測試命令，app.test_cli_runner()會返回一個命令運行氣的實例，
        # 測試時用self.runner來保存它，並通過invoke()執行命令
        # 測試判斷方法為查看執行後資料庫是否變化，或判斷命令行輸出是否包含預期字元

        # 建立資料
    def test_forge_command(self):
        result = self.runner.invoke(forge)
        self.assertIn('Done.', result.output)
        self.assertNotEqual(Movie.query.count(), 0)

        # 測試初始化數據庫
    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', result.output)

        # 测试生成管理员账户
    def test_admin_command(self):
        db.drop_all()
        db.create_all()
        result = self.runner.invoke(
            args=['admin', '--username', 'grey', '--password', '123'])
        self.assertIn('Creating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'grey')
        self.assertTrue(User.query.first().validate_password('123'))

    # 测试更新管理员账户
    def test_admin_command_update(self):
        # 使用 args 参数给出完整的命令参数列表
        result = self.runner.invoke(
            args=['admin', '--username', 'peter', '--password', '456'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'peter')
        self.assertTrue(User.query.first().validate_password('456'))


# unittest的執行代碼
if __name__ == '__main__':
    unittest.main()
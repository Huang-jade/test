"""
用户管理类
"""
import hashlib

class User:
    def __init__(self, user_id, name, email, hashed_password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        
    def verify_password(self, password):
        return self.hashed_password == self._hash_password(password)
        
    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
        
    def __str__(self):
        return f"用户ID: {self.user_id}, 姓名: {self.name}, 邮箱: {self.email}"

class UserManager:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        
    def authenticate_user(self):
        print("\n用户认证")
        print("1. 登录")
        print("2. 注册")
        
        choice = input("请选择 (1-2): ")
        
        if choice == '1':
            return self._login()
        elif choice == '2':
            return self._register()
        else:
            print("无效选择")
            return None
            
    def _login(self):
        email = input("邮箱: ")
        password = input("密码: ")
        
        user = self.db_handler.get_user_by_email(email)
        if user and user.verify_password(password):
            print(f"登录成功! 欢迎 {user.name}")
            return user
        else:
            print("邮箱或密码错误")
            return None
            
    def _register(self):
        print("\n用户注册")
        name = input("姓名: ")
        email = input("邮箱: ")
        password = input("密码: ")
        
        # 检查邮箱是否已存在
        if self.db_handler.get_user_by_email(email):
            print("该邮箱已注册")
            return None
            
        user_id = self.db_handler.get_next_user_id()
        hashed_password = User._hash_password(password)
        user = User(user_id, name, email, hashed_password)
        
        self.db_handler.save_user(user)
        print("注册成功!")
        return user
#!/usr/bin/env python3
"""
银行账户管理系统 - 主程序
"""
import sys
from users.user import UserManager
from accounts.base_account import AccountManager
from transactions.transaction_manager import TransactionManager
from database.db_handler import DatabaseHandler

class BankingSystem:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.user_manager = UserManager(self.db_handler)
        self.account_manager = AccountManager(self.db_handler)
        self.transaction_manager = TransactionManager(self.db_handler)
        self.report_generator = ReportGenerator(self.db_handler)

    def run(self):
        """运行银行系统"""
        print("欢迎使用银行账户管理系统")
        
        # 用户登录/注册
        user = self.user_manager.authenticate_user()
        if not user:
            print("认证失败，退出系统")
            return
            
        while True:
            print("\n请选择操作:")
            print("1. 创建账户")
            print("2. 存款")
            print("3. 取款")
            print("4. 转账")
            print("5. 查看账户信息")
            print("6. 查看交易记录")
            print("7. 生成对账单")  # 新增
            print("8. 生成利息报告")  # 新增
            print("9. 退出")  # 修改
            
            choice = input("请输入选项 (1-9): ")
            
            if choice == '1':
                self.account_manager.create_account(user)
            elif choice == '2':
                self.transaction_manager.deposit(user)
            elif choice == '3':
                self.transaction_manager.withdraw(user)
            elif choice == '4':
                self.transaction_manager.transfer(user)
            elif choice == '5':
                self.account_manager.view_accounts(user)
            elif choice == '6':
                self.transaction_manager.view_transactions(user)
            elif choice == '7':
                self.generate_statement(user)
            elif choice == '8':
                self.generate_interest_report(user)
            elif choice == '9':
                print("感谢使用银行账户管理系统，再见!")
                break
            else:
                print("无效选项，请重新选择")


 # 新增方法
    def generate_statement(self, user):
        account = self.transaction_manager._select_account(user, "请选择要生成对账单的账户")
        if not account:
            return
            
        # 获取日期范围
        try:
            days = int(input("请输入要查询的天数: "))
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            statement = self.report_generator.generate_account_statement(
                account.account_number, start_date, end_date
            )
            print("\n" + statement)
        except ValueError:
            print("请输入有效天数")
            
    def generate_interest_report(self, user):
        report = self.report_generator.generate_interest_report(user)
        print("\n" + report)

if __name__ == "__main__":
    banking_system = BankingSystem()
    banking_system.run()
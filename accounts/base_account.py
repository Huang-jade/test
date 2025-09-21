"""
基础账户类
"""
from abc import ABC, abstractmethod
from datetime import datetime

class Account(ABC):
    def __init__(self, account_number, owner_id, balance=0.0):
        self.account_number = account_number
        self.owner_id = owner_id
        self.balance = balance
        self.created_date = datetime.now()
        self.is_active = True
        
    @abstractmethod
    def get_account_type(self):
        pass
        
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金额必须大于零")
        self.balance += amount
        return self.balance
        
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("取款金额必须大于零")
        if amount > self.balance:
            raise ValueError("余额不足")
        self.balance -= amount
        return self.balance
        
    def __str__(self):
        return (f"账户号: {self.account_number}, "
                f"类型: {self.get_account_type()}, "
                f"余额: {self.balance:.2f}, "
                f"状态: {'活跃' if self.is_active else '冻结'}")

class AccountManager:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        
    # 在create_account方法中添加贷款账户选项
def create_account(self, user):
    print("\n创建账户")
    account_type = input("请输入账户类型 (1: 储蓄账户, 2: 支票账户, 3: 贷款账户): ")
    
    if account_type == '1':
        from accounts.savings_account import SavingsAccount
        account = SavingsAccount.generate_account_number(), user.user_id, 0.0
    elif account_type == '2':
        from accounts.checking_account import CheckingAccount
        account = CheckingAccount.generate_account_number(), user.user_id, 0.0
    elif account_type == '3':
        from accounts.loan_account import LoanAccount
        loan_amount = float(input("请输入贷款金额: "))
        term_months = int(input("请输入贷款期限(月): "))
        account = LoanAccount(LoanAccount.generate_account_number(), user.user_id, 
                             loan_amount, term_months=term_months)
    else:
        print("无效的账户类型")
        return
        
    self.db_handler.save_account(account)
    print(f"账户创建成功! 账户号: {account.account_number}")
        
    def view_accounts(self, user):
        accounts = self.db_handler.get_user_accounts(user.user_id)
        print("\n您的账户:")
        for account in accounts:
            print(account)
"""
支票账户类
"""
from accounts.base_account import Account
import random

class CheckingAccount(Account):
    def __init__(self, account_number, owner_id, balance=0.0, overdraft_limit=500.0):
        super().__init__(account_number, owner_id, balance)
        self.overdraft_limit = overdraft_limit
        
    def get_account_type(self):
        return "支票账户"
        
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("取款金额必须大于零")
        if amount > (self.balance + self.overdraft_limit):
            raise ValueError("超过透支限额")
        self.balance -= amount
        return self.balance
        
    @staticmethod
    def generate_account_number():
        return f"CA{random.randint(10000000, 99999999)}"
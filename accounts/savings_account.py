"""
储蓄账户类
"""
from accounts.base_account import Account
import random

class SavingsAccount(Account):
    def __init__(self, account_number, owner_id, balance=0.0, interest_rate=0.03):
        super().__init__(account_number, owner_id, balance)
        self.interest_rate = interest_rate
        
    def get_account_type(self):
        return "储蓄账户"
        
    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest
        
    @staticmethod
    def generate_account_number():
        return f"SA{random.randint(10000000, 99999999)}"
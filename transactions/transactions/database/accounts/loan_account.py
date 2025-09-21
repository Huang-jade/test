"""
贷款账户类
"""
from accounts.base_account import Account
import random

class LoanAccount(Account):
    def __init__(self, account_number, owner_id, loan_amount, interest_rate=0.05, term_months=12):
        super().__init__(account_number, owner_id, -loan_amount)  # 余额为负表示欠款
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.monthly_payment = self.calculate_monthly_payment()
        
    def get_account_type(self):
        return "贷款账户"
        
    def calculate_monthly_payment(self):
        # 等额本息计算每月还款额
        monthly_rate = self.interest_rate / 12
        return (self.loan_amount * monthly_rate * (1 + monthly_rate)**self.term_months) / \
               ((1 + monthly_rate)**self.term_months - 1)
        
    def make_payment(self, amount):
        if amount <= 0:
            raise ValueError("还款金额必须大于零")
        if amount > abs(self.balance):
            raise ValueError("还款金额超过剩余贷款金额")
            
        self.balance += amount  # 余额为负，加上还款金额
        return abs(self.balance)  # 返回剩余贷款金额
        
    @staticmethod
    def generate_account_number():
        return f"LA{random.randint(10000000, 99999999)}"
        
    def __str__(self):
        return (f"账户号: {self.account_number}, "
                f"类型: {self.get_account_type()}, "
                f"贷款金额: {self.loan_amount:.2f}, "
                f"剩余欠款: {abs(self.balance):.2f}, "
                f"每月还款: {self.monthly_payment:.2f}, "
                f"状态: {'活跃' if self.is_active else '冻结'}")
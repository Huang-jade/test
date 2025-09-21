"""
交易类
"""
from datetime import datetime
from enum import Enum

# 在TransactionType枚举中添加贷款还款类型
class TransactionType(Enum):
    DEPOSIT = "存款"
    WITHDRAWAL = "取款"
    TRANSFER = "转账"
    LOAN_PAYMENT = "贷款还款"

class Transaction:
    def __init__(self, transaction_id, account_number, transaction_type, amount, 
                 timestamp=None, target_account=None, description=""):
        self.transaction_id = transaction_id
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = timestamp or datetime.now()
        self.target_account = target_account
        self.description = description
        
    def __str__(self):
        result = (f"交易ID: {self.transaction_id}, "
                 f"账户: {self.account_number}, "
                 f"类型: {self.transaction_type.value}, "
                 f"金额: {self.amount:.2f}, "
                 f"时间: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                 
        if self.target_account:
            result += f", 目标账户: {self.target_account}"
            
        if self.description:
            result += f", 描述: {self.description}"
            
        return result
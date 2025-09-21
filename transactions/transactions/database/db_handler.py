"""
数据库处理类 - 模拟数据库操作
"""
import json
import os
from users.user import User
from accounts.savings_account import SavingsAccount
from accounts.checking_account import CheckingAccount

class DatabaseHandler:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 初始化数据文件
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.accounts_file = os.path.join(self.data_dir, "accounts.json")
        self.transactions_file = os.path.join(self.data_dir, "transactions.json")
        
        # 确保文件存在
        for file_path in [self.users_file, self.accounts_file, self.transactions_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
                    
    def get_next_user_id(self):
        users = self._load_data(self.users_file)
        return len(users) + 1
        
    def get_next_transaction_id(self):
        transactions = self._load_data(self.transactions_file)
        return len(transactions) + 1
        
    def save_user(self, user):
        users = self._load_data(self.users_file)
        user_data = {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "hashed_password": user.hashed_password
        }
        users.append(user_data)
        self._save_data(self.users_file, users)
        
    def get_user_by_email(self, email):
        users = self._load_data(self.users_file)
        for user_data in users:
            if user_data["email"] == email:
                return User(
                    user_data["user_id"],
                    user_data["name"],
                    user_data["email"],
                    user_data["hashed_password"]
                )
        return None
        
    def save_account(self, account):
        accounts = self._load_data(self.accounts_file)
        account_data = {
            "account_number": account.account_number,
            "owner_id": account.owner_id,
            "balance": account.balance,
            "account_type": account.get_account_type(),
            "created_date": account.created_date.isoformat(),
            "is_active": account.is_active
        }
        
        # 添加特定账户类型的额外属性
        if isinstance(account, SavingsAccount):
            account_data["interest_rate"] = account.interest_rate
        elif isinstance(account, CheckingAccount):
            account_data["overdraft_limit"] = account.overdraft_limit
            
        accounts.append(account_data)
        self._save_data(self.accounts_file, accounts)
        
    def get_user_accounts(self, user_id):
        accounts = self._load_data(self.accounts_file)
        user_accounts = []
        
        for account_data in accounts:
            if account_data["owner_id"] == user_id:
                if account_data["account_type"] == "储蓄账户":
                    account = SavingsAccount(
                        account_data["account_number"],
                        account_data["owner_id"],
                        account_data["balance"]
                    )
                elif account_data["account_type"] == "支票账户":
                    account = CheckingAccount(
                        account_data["account_number"],
                        account_data["owner_id"],
                        account_data["balance"]
                    )
                else:
                    continue
                    
                account.created_date = account_data["created_date"]
                account.is_active = account_data["is_active"]
                user_accounts.append(account)
                
        return user_accounts
        
    def get_account(self, account_number):
        accounts = self._load_data(self.accounts_file)
        for account_data in accounts:
            if account_data["account_number"] == account_number:
                if account_data["account_type"] == "储蓄账户":
                    account = SavingsAccount(
                        account_data["account_number"],
                        account_data["owner_id"],
                        account_data["balance"]
                    )
                elif account_data["account_type"] == "支票账户":
                    account = CheckingAccount(
                        account_data["account_number"],
                        account_data["owner_id"],
                        account_data["balance"]
                    )
                else:
                    return None
                    
                account.created_date = account_data["created_date"]
                account.is_active = account_data["is_active"]
                return account
        return None
        
    def update_account(self, account):
        accounts = self._load_data(self.accounts_file)
        for i, account_data in enumerate(accounts):
            if account_data["account_number"] == account.account_number:
                accounts[i]["balance"] = account.balance
                accounts[i]["is_active"] = account.is_active
                break
        self._save_data(self.accounts_file, accounts)
        
    def save_transaction(self, transaction):
        transactions = self._load_data(self.transactions_file)
        transaction_data = {
            "transaction_id": transaction.transaction_id,
            "account_number": transaction.account_number,
            "transaction_type": transaction.transaction_type.value,
            "amount": transaction.amount,
            "timestamp": transaction.timestamp.isoformat(),
            "target_account": transaction.target_account,
            "description": transaction.description
        }
        transactions.append(transaction_data)
        self._save_data(self.transactions_file, transactions)
        
    def get_account_transactions(self, account_number):
        transactions = self._load_data(self.transactions_file)
        account_transactions = []
        
        for transaction_data in transactions:
            if (transaction_data["account_number"] == account_number or 
                transaction_data["target_account"] == account_number):
                transaction = Transaction(
                    transaction_data["transaction_id"],
                    transaction_data["account_number"],
                    TransactionType(transaction_data["transaction_type"]),
                    transaction_data["amount"],
                    transaction_data["timestamp"],
                    transaction_data["target_account"],
                    transaction_data["description"]
                )
                account_transactions.append(transaction)
                
        return account_transactions
        
    def _load_data(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
            
    def _save_data(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
"""
交易管理类
"""
from transactions.transaction import Transaction, TransactionType

class TransactionManager:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        
    def deposit(self, user):
        print("\n存款操作")
        account = self._select_account(user, "请选择存款账户")
        if not account:
            return
            
        try:
            amount = float(input("请输入存款金额: "))
            account.deposit(amount)
            
            # 记录交易
            transaction = Transaction(
                self.db_handler.get_next_transaction_id(),
                account.account_number,
                TransactionType.DEPOSIT,
                amount
            )
            self.db_handler.save_transaction(transaction)
            self.db_handler.update_account(account)
            
            print(f"存款成功! 当前余额: {account.balance:.2f}")
        except ValueError as e:
            print(f"错误: {e}")
            
    def withdraw(self, user):
        print("\n取款操作")
        account = self._select_account(user, "请选择取款账户")
        if not account:
            return
            
        try:
            amount = float(input("请输入取款金额: "))
            account.withdraw(amount)
            
            # 记录交易
            transaction = Transaction(
                self.db_handler.get_next_transaction_id(),
                account.account_number,
                TransactionType.WITHDRAWAL,
                amount
            )
            self.db_handler.save_transaction(transaction)
            self.db_handler.update_account(account)
            
            print(f"取款成功! 当前余额: {account.balance:.2f}")
        except ValueError as e:
            print(f"错误: {e}")
            
    def transfer(self, user):
        print("\n转账操作")
        from_account = self._select_account(user, "请选择转出账户")
        if not from_account:
            return
            
        to_account_number = input("请输入转入账户号: ")
        to_account = self.db_handler.get_account(to_account_number)
        if not to_account:
            print("转入账户不存在")
            return
            
        try:
            amount = float(input("请输入转账金额: "))
            from_account.withdraw(amount)
            to_account.deposit(amount)
            
            # 记录交易
            transaction = Transaction(
                self.db_handler.get_next_transaction_id(),
                from_account.account_number,
                TransactionType.TRANSFER,
                amount,
                target_account=to_account_number,
                description=f"转账至{to_account_number}"
            )
            self.db_handler.save_transaction(transaction)
            self.db_handler.update_account(from_account)
            self.db_handler.update_account(to_account)
            
            print(f"转账成功! 当前余额: {from_account.balance:.2f}")
        except ValueError as e:
            print(f"错误: {e}")
            
    def view_transactions(self, user):
        account = self._select_account(user, "请选择要查看交易记录的账户")
        if not account:
            return
            
        transactions = self.db_handler.get_account_transactions(account.account_number)
        print(f"\n账户 {account.account_number} 的交易记录:")
        for transaction in transactions:
            print(transaction)
            
    def _select_account(self, user, prompt):
        accounts = self.db_handler.get_user_accounts(user.user_id)
        if not accounts:
            print("您还没有任何账户")
            return None
            
        print(f"\n{prompt}:")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account}")
            
        try:
            choice = int(input("请选择账户 (输入数字): "))
            if 1 <= choice <= len(accounts):
                return accounts[choice - 1]
            else:
                print("无效选择")
                return None
        except ValueError:
            print("请输入有效数字")
            return None
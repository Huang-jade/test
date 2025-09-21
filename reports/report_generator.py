"""
报表生成类
"""
from datetime import datetime, timedelta

class ReportGenerator:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        
    def generate_account_statement(self, account_number, start_date, end_date):
        """生成账户对账单"""
        transactions = self.db_handler.get_account_transactions(account_number)
        account = self.db_handler.get_account(account_number)
        
        # 过滤指定日期范围内的交易
        filtered_transactions = [
            t for t in transactions 
            if start_date <= t.timestamp <= end_date
        ]
        
        # 生成报表
        report = f"账户对账单 - {account_number}\n"
        report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        report += f"时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}\n"
        report += f"当前余额: {account.balance:.2f}\n\n"
        report += "交易明细:\n"
        
        for transaction in filtered_transactions:
            report += f"{transaction}\n"
            
        return report
        
    def generate_interest_report(self, user):
        """生成利息报告"""
        accounts = self.db_handler.get_user_accounts(user.user_id)
        report = f"利息报告 - {user.name}\n"
        report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        total_interest = 0
        
        for account in accounts:
            if hasattr(account, 'interest_rate') and account.balance > 0:
                interest = account.balance * account.interest_rate
                total_interest += interest
                report += (f"账户 {account.account_number}: "
                          f"余额 {account.balance:.2f} * "
                          f"利率 {account.interest_rate*100:.2f}% = "
                          f"利息 {interest:.2f}\n")
                          
        report += f"\n预计年利息总额: {total_interest:.2f}\n"
        return report
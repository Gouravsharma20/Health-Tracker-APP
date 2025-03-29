"""from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()

# Owner Model
class Owner(Base):
    __tablename__ = "owners"

    owner_id = Column(Integer, primary_key=True, index=True)
    owner_name = Column(String(50), nullable=False)
    total_income = Column(Float, default=0.0)
    total_expenses = Column(Float, default=0.0)
    total_tax = Column(Float, default=0.0)  # 18% GST
    net_profit = Column(Float, default=0.0)

    expenses = relationship("Expense", back_populates="owner")

    def update_financials(self, income=0, expense=0, tax=0):
        Update owner's financial records.
        self.total_income += income
        self.total_expenses += expense
        self.total_tax += tax
        self.net_profit = (self.total_income - self.total_expenses - self.total_tax)


# Expense Model
class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    expense_type = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False, default=date.today)

    owner_id = Column(Integer, ForeignKey("owners.owner_id"), nullable=False)
    owner = relationship("Owner", back_populates="expenses")

    def __init__(self, expense_type, amount, owner):
        self.expense_type = expense_type
        self.amount = amount
        self.owner = owner
        self.owner.update_financials(expense=amount)


# Payment Model
class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    final_amount = Column(Float, nullable=False)
    mdr_fee = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)  # 18% GST

    def __init__(self, client_id, amount, payment_method, session):
        self.client_id = client_id
        self.amount = amount
        self.payment_method = payment_method

        self.mdr_fee, self.final_amount = self.calculate_final_amount(amount, payment_method)
        self.tax_amount = self.final_amount * 0.18  # 18% GST

        # Update Owner's Financials
        owner = session.query(Owner).first()
        if owner:
            owner.update_financials(income=self.final_amount, tax=self.tax_amount)

    @staticmethod
    def calculate_final_amount(amount, payment_method):
        # Calculate MDR fee and final amount.
        mdr_rates = {"credit_card": 0.02, "debit_card": 0.015, "upi": 0.01, "cash": 0.0}
        mdr_fee = amount * mdr_rates.get(payment_method, 0.0)
        final_amount = amount - mdr_fee
        return mdr_fee, final_amount """

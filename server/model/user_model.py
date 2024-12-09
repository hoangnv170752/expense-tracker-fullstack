from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from model.utils_model import Base


class User(Base):
    __tablename__ = "kash_users"

    id = Column(Integer, primary_key=True, index=True)
    etTag = Column(Integer, nullable=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, nullable=True)
    birthday = Column(DateTime, nullable=True)
    password = Column(String, nullable=False)
    profile_pic_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    wallets = relationship("UserWallet", back_populates="user")
    expenses = relationship("UserExpense", back_populates="user")
    incomes = relationship("UserIncome", back_populates="user")
    payments = relationship("PaymentHistory", back_populates="user")
    budgets = relationship("UserBudget", back_populates="user")
    notifications = relationship("UserNotification", back_populates="user")
    savings = relationship("SavingsGoal", back_populates="user")


class UserWallet(Base):
    __tablename__ = "kash_user_wallet"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("kash_users.id"), nullable=False)
    wallet_name = Column(String, nullable=False)
    balance = Column(Numeric(12, 2), nullable=False, default=0.0)
    wallet_type = Column(String, nullable=False)  # e.g., 'cash', 'bank', 'crypto'
    currency = Column(String, nullable=False, default="USD")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wallets")


class UserExpense(Base):
    __tablename__ = "kash_expense_user"

    id = Column(Integer, primary_key=True, index=True)
    etTag = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("kash_users.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("kash_user_wallet.id"), nullable=False)
    cat_id = Column(Integer, ForeignKey("kash_categories.id"), nullable=False)
    expense_name = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String, nullable=True)  # e.g., 'credit card', 'cash'
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="expenses")
    wallet = relationship("UserWallet")
    category = relationship("Category")


class UserIncome(Base):
    __tablename__ = "kash_income_user"

    id = Column(Integer, primary_key=True, index=True)
    etTag = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("kash_users.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("kash_user_wallet.id"), nullable=False)
    cat_id = Column(Integer, ForeignKey("kash_categories.id"), nullable=False)
    income_name = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    source = Column(String, nullable=True)  # e.g., 'salary', 'investment'
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="incomes")
    wallet = relationship("UserWallet")
    category = relationship("Category")


class PaymentHistory(Base):
    __tablename__ = "kash_payment_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("kash_users.id"), nullable=False)
    expense_id = Column(Integer, ForeignKey("kash_expense_user.id"), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_amount = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String, nullable=True)
    status = Column(String, nullable=False, default="paid")  # e.g., 'paid', 'due'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")
    expense = relationship("UserExpense")


class UserBudget(Base):
    __tablename__ = "kash_budget"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("kash_users.id"), nullable=False)
    cat_id = Column(Integer, ForeignKey("kash_categories.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("kash_user_wallet.id"), nullable=False)
    budget_amount = Column(Numeric(12, 2), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="budgets")
    wallet = relationship("UserWallet")
    category = relationship("Category")


class UserNotification(Base):
    __tablename__ = "kash_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("kash_users.id"), nullable=False)
    type = Column(String, nullable=False)  # e.g., 'payment reminder', 'budget exceeded'
    message = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="unread")  # e.g., 'read', 'unread'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


class SavingsGoal(Base):
    __tablename__ = "kash_savings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("kash_users.id"), nullable=False)
    goal_name = Column(String, nullable=False)
    target_amount = Column(Numeric(12, 2), nullable=False)
    current_amount = Column(Numeric(12, 2), nullable=False, default=0.0)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="savings")
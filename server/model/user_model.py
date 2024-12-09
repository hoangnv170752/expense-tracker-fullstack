# user_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from model.utils_model import Base

class User(Base):
    __tablename__ = "aslan_users"

    id = Column(Integer, primary_key=True, index=True)
    employeeId = Column(Integer, nullable=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    birthday = Column(DateTime, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    token_usage = relationship("UserTokenUsage", back_populates="user")
    rewards = relationship("Rewards", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")
    alerts = relationship("Alerts", back_populates="user")


class UserTokenUsage(Base):
    __tablename__ = "aslan_user_token_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("aslan_users.id"), nullable=False)
    monthly_token_limit = Column(Integer, nullable=False, default=100)
    tokens_used = Column(Integer, nullable=False, default=0)
    month_start_date = Column(DateTime, default=datetime.utcnow)
    month_end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="token_usage")


class Rewards(Base):
    __tablename__ = "aslan_rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("aslan_users.id"), nullable=False)
    reward_type = Column(String, nullable=False)     # e.g. 'badge', 'coupon'
    reward_description = Column(Text, nullable=True)
    granted_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="rewards")

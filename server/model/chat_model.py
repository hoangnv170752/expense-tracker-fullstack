# chat_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from model.utils_model import get_db_connection
from model.utils_model import Base


class ChatSession(Base):
    __tablename__ = "aslan_chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("aslan_users.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    token_consumed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="chat_sessions")
    chat_history = relationship("ChatHistory", back_populates="session")
    alerts = relationship("Alerts", back_populates="session")


class ChatHistory(Base):
    __tablename__ = "aslan_chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("aslan_chat_sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("aslan_users.id"), nullable=False)
    message_text = Column(Text, nullable=False)
    message_type = Column(String, nullable=False)  
    emotion_label = Column(String, nullable=True)  
    color_flag = Column(String, nullable=True)     
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    session = relationship("ChatSession", back_populates="chat_history")
    user = relationship("User", back_populates="chat_history")
    alerts = relationship("Alerts", back_populates="chat_message")


class Alerts(Base):
    __tablename__ = "aslan_alerts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("aslan_chat_sessions.id"), nullable=False)
    chat_history_id = Column(Integer, ForeignKey("aslan_chat_history.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("aslan_users.id"), nullable=False)
    alert_type = Column(String, nullable=False)   # e.g. 'high_emotion', 'crisis'
    alert_description = Column(Text, nullable=True)
    alert_time = Column(DateTime, default=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="alerts")
    chat_message = relationship("ChatHistory", back_populates="alerts")
    user = relationship("User", back_populates="alerts")

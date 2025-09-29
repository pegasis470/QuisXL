from sqlalchemy import Column, Integer, String, ForeignKey, JSON, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__= 'app_user'
    user_id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String)
    phone_number=Column(String)
    email_id=Column(String)
    organization=Column(String)
    username=Column(String)
    password_hash=Column(String)
    status = Column(String(10), default="Offline")
    auth_token = Column(String, nullable=True)  # New column for auth token
    
class Quiz(Base):
    __tablename__ = "quiz"
    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("app_user.user_id", ondelete="CASCADE"), nullable=False)
    data = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    quiz_name = Column(String(100), nullable=False, default="Untitled Quiz")  # Second column
    owner = relationship("User", backref="quizzes")
    responses = relationship("Response", back_populates="quiz", cascade="all, delete-orphan")

class Response(Base):
    __tablename__ = "response"
    response_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quiz.quiz_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("app_user.user_id", ondelete="CASCADE"), nullable=False)
    response_data = Column(JSON, nullable=False)
    submitted_at = Column(TIMESTAMP, server_default=func.now())
    score = Column(Integer, default=0)  # New column for marks
    name= Column(String)  # Optional column for responder's name
    standard = Column(String)
    quiz = relationship("Quiz", backref="response")
    user = relationship("User", backref="response")  # Relationship to User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Quiz, User
from schemas import QuizCreate, Login
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()
AUTH_KEY=os.getenv("AUTH_KEY_GEN",None)
# Create the FastAPI router
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/make-quiz")
def make_quiz(quiz: QuizCreate , db: Session = Depends(get_db)):
    # Check if user is logged in
    user = db.query(User).filter(User.user_id == quiz.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.status != "Online":
        raise HTTPException(status_code=403, detail="User not logged in")
    # Create a new quiz
    print(quiz)
    new_quiz = Quiz(
        user_id=quiz.user_id,
        quiz_name=quiz.quizname,
        data=[{
            "qus_no": q.qus_no,
            "question": q.qustion,
            "options": [{"A": opt.A, "B": opt.B, "C": opt.C, "D": opt.D} for opt in q.options],
            "answer": q.answer,
            "marks": q.marks
        } for q in quiz.qustions]
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return {"message": "Quiz created successfully", "quiz_id": new_quiz.quiz_id}

@router.get("/get-quizzes/{user_id}")
def get_quizzes(user_id: int, db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).filter(Quiz.user_id == user_id).all()
    if not quizzes:
        raise HTTPException(status_code=404, detail="No quizzes found for this user")
    
    return {"quizzes": [{"quiz_id":quiz.quiz_id,"name":quiz.quiz_name,"data":quiz.data} for quiz in quizzes]} 
@router.get("/get-quiz/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return {"quiz_name": quiz.quiz_name, "data": quiz.data}

@router.delete("/delete-quiz/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    db.delete(quiz)
    db.commit()
    return {"message": "Quiz deleted successfully"} 
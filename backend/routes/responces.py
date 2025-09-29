from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Quiz, User, Response
from schemas import ResponseCreate
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()
AUTH_KEY=os.getenv("AUTH_KEY_GEN",None)
# Create the FastAPI router
router = APIRouter()

@router.post("/quiz")
def collect_response(response:ResponseCreate , db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.quiz_id == response.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    # sort the response data by question number
    response_data = sorted(response.data, key=lambda x: x.qus_no)
    # calculate marks
    marks = 0
    for q in response_data:
        if q.answer == quiz.data[q.qus_no - 1]['answer']:
            marks += quiz.data[q.qus_no - 1]['marks']
    # Create a new response
    new_response = Response(
        quiz_id=response.quiz_id,
        user_id=response.user_id,
        name=response.name,
        response_data=[{
            "qus_no": q.qus_no,
            "answer": q.answer,
        } for q in response_data],
        score=marks
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return {"message": "Response submitted successfully", "response_id": new_response.response_id,"marks": marks}  
@router.get("/responses/{quiz_id}")
def get_responses(quiz_id: int, db: Session = Depends(get_db)):
    responses = db.query(Response).filter(Response.quiz_id == quiz_id).all()
    if not responses:
        raise HTTPException(status_code=404, detail="No responses found for this quiz")
    
    return {"responses": [{"id": response.response_id, "name":response.name,"response_data": response.response_data, "score": response.score} for response in responses]}
@router.get("/response/{response_id}")
def get_response(response_id: int, db: Session = Depends(get_db)):
    response = db.query(Response).filter(Response.response_id == response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    
    return {
        "response_id": response.response_id,
        "quiz_id": response.quiz_id,
        "user_id": response.user_id,
        "name": response.name,
        "standard": response.standard,
        "response_data": response.response_data,
        "score": response.score,
        "submitted_at": response.submitted_at
    }       
@router.get("/get-id")
def get_response_id_by_name(name: str, db: Session = Depends(get_db)):
    response = db.query(Response).filter(Response.name == name).first()
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    
    return {"response_id": response.response_id, "name": response.name}
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import users,admin,responces
from dotenv import load_dotenv
from database import Base,engine
import os
load_dotenv()
app = FastAPI(docs_url=None)


security = HTTPBasic()
USERNAME = os.getenv("SWAGGER_USERNAME")
PASSWORD = os.getenv("SWAGGER_PASSWORD")
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_docs(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="API Docs")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; change this to specific origins for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/user")
app.include_router(admin.router,prefix="/admin")
app.include_router(responces.router, prefix="/response")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
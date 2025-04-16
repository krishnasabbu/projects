from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate, add_pagination
from app.schemas import UserCreate, User, UserUpdate, Token
from app.auth import get_current_user, authenticate_user, create_access_token
from app import crud
from app.logger import setup_logging
import uuid
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException as FastAPIHTTPException

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware for logging and request ID
@app.middleware("http")
async def add_request_id_and_log(request: Request, call_next):
    print(f"request === {request}")
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    setup_logging(request_id)

    # Print basic request info
    print(f"\n🔹 Request Info:")
    print(f"  🧾 Method: {request.method}")
    print(f"  🛣️ URL: {request.url}")
    print(f"  📦 Headers: {dict(request.headers)}")

    # Optional: Log body if it's a POST/PUT and has data
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
        print(f"  🧸 Body: {body.decode('utf-8')}")

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Global exception handler (Controller Advice)
@app.exception_handler(FastAPIHTTPException)
async def global_exception_handler(request: Request, exc: FastAPIHTTPException):
    print(f"HTTP ERROR [{request.state.request_id}]: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "request_id": request.state.request_id,
        },
    )


@app.on_event("startup")
async def startup_event():
    crud.generate_fake_users()


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"from data : {form_data}")
    user_obj = authenticate_user(form_data.username, form_data.password)
    if not user_obj:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user_obj.email)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/users", response_model=User)
def create_user(user: UserCreate):
    return crud.create_user(user)


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, current_user=Depends(get_current_user)):
    print(f"User === {user_id}")
    user = crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users", response_model=Page[User])
def list_all_users(q: str = None, current_user=Depends(get_current_user)):
    print(f"getting it --- {q}")
    return paginate(crud.list_users(q))


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, current_user=Depends(get_current_user)):
    print(f"User === {user_id}")
    updated = crud.update_user(user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@app.delete("/users/{user_id}")
def delete_user(user_id: int, current_user=Depends(get_current_user)):
    deleted = crud.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


add_pagination(app)

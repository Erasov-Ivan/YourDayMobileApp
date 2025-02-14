from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from admin import router as admin_router
from users import router as users_router

app = FastAPI(root_path="/api")
app.include_router(admin_router)
app.include_router(users_router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")

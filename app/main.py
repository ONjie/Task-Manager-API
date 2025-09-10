from fastapi import FastAPI
from app.routes.users import router as users_router
from app.routes.tasks import router as tasks_router
from app.database.database import create_database_and_tables


app = FastAPI()

create_database_and_tables()

app.include_router(users_router)
app.include_router(tasks_router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Task Manager API is running"}
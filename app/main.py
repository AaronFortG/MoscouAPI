from fastapi import FastAPI
from app.routes import user, event, ticket, health

app = FastAPI()

# Include routers
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(event.router, prefix="/events", tags=["Events"])
app.include_router(ticket.router, prefix="/tickets", tags=["Tickets"])
app.include_router(health.router, prefix="/health-check", tags=["Health Check"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

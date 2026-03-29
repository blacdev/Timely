from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, admin, attendance, late, reports, rules

app = FastAPI(title="Timely API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] ,
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(rules.router, prefix="/api/admin", tags=["rules"])
app.include_router(attendance.router, prefix="/api", tags=["attendance"])
app.include_router(late.router, prefix="/api/late", tags=["late"])
app.include_router(reports.router, prefix="/api/admin/reports", tags=["reports"])

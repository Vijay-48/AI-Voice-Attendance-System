from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime

# Import the local storage system
from local_system import LocalAttendanceSystem

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the system
system = LocalAttendanceSystem()

class AttendanceRequest(BaseModel):
    name: str

class StudentRequest(BaseModel):
    name: str
    email: str
    phone: str

class ReportRequest(BaseModel):
    startDate: str
    endDate: str

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.post("/api/mark-attendance")
async def mark_attendance(request: AttendanceRequest):
    success, message = system.mark_attendance(request.name)
    if not success:
        raise HTTPException(status_code=404, detail=message)
    return {"success": True, "message": message}

@app.post("/api/add-student")
async def add_student(request: StudentRequest):
    success, message = system.add_student(request.name, request.email, request.phone)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}

@app.post("/api/attendance-report")
async def get_attendance_report(request: ReportRequest):
    try:
        results = system.get_attendance_report(request.startDate, request.endDate)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
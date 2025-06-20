import datetime
import json
import os
from pathlib import Path

class LocalAttendanceSystem:
    def __init__(self):
        # Create data directory if it doesn't exist
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize storage files
        self.students_file = self.data_dir / "students.json"
        self.attendance_file = self.data_dir / "attendance.json"
        
        # Create files if they don't exist
        self._init_storage()
        
        # Load data
        self.load_data()

    def _init_storage(self):
        if not self.students_file.exists():
            self._save_json(self.students_file, {})
        if not self.attendance_file.exists():
            self._save_json(self.attendance_file, [])

    def _save_json(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def _load_json(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def load_data(self):
        """Load data from JSON files"""
        self.students = self._load_json(self.students_file)
        self.attendance = self._load_json(self.attendance_file)

    def save_data(self):
        """Save data to JSON files"""
        self._save_json(self.students_file, self.students)
        self._save_json(self.attendance_file, self.attendance)

    def generate_student_id(self):
        """Generate a unique student ID"""
        existing_ids = [int(s_id[1:]) for s_id in self.students.values()]
        next_id = max(existing_ids, default=0) + 1
        return f"S{next_id:03d}"

    def add_student(self, name, email, phone):
        """Add a new student"""
        if name.lower() in self.students:
            return False, "Student already exists"
            
        student_id = self.generate_student_id()
        self.students[name.lower()] = student_id
        self.save_data()
        return True, f"Student added successfully! ID: {student_id}"

    def mark_attendance(self, name):
        """Mark attendance for a student"""
        name = name.lower()
        if name not in self.students:
            return False, "Student not found"
            
        attendance_record = {
            "student_id": self.students[name],
            "name": name,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.attendance.append(attendance_record)
        self.save_data()
        return True, f"Attendance marked for {name}"

    def get_attendance_report(self, start_date, end_date):
        """Get attendance report for a date range"""
        start = datetime.datetime.fromisoformat(start_date)
        end = datetime.datetime.fromisoformat(end_date)
        
        # Count attendance for each student in date range
        attendance_count = {}
        for record in self.attendance:
            timestamp = datetime.datetime.fromisoformat(record['timestamp'])
            if start <= timestamp <= end:
                name = record['name']
                attendance_count[name] = attendance_count.get(name, 0) + 1
        
        # Format for report
        report = [{"_id": name, "count": count} 
                 for name, count in attendance_count.items()]
        return sorted(report, key=lambda x: x['count'], reverse=True)
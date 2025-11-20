"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
import sqlite3
from typing import Dict, Any

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

INITIAL_ACTIVITIES: Dict[str, Dict[str, Any]] = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}

DB_PATH = Path(__file__).parent.parent / "activities.db"

def get_connection():
    # Using a new connection per request scope keeps things simple for now
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    first_time = not DB_PATH.exists()
    conn = get_connection()
    cur = conn.cursor()
    # Create tables
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS activities (
            name TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            schedule TEXT NOT NULL,
            max_participants INTEGER NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS participants (
            activity_name TEXT NOT NULL,
            email TEXT NOT NULL,
            PRIMARY KEY(activity_name, email),
            FOREIGN KEY(activity_name) REFERENCES activities(name) ON DELETE CASCADE
        );
        """
    )

    # Seed only if empty (not just first_time because db could exist but be cleared)
    cur.execute("SELECT COUNT(*) FROM activities")
    if cur.fetchone()[0] == 0:
        for name, data in INITIAL_ACTIVITIES.items():
            cur.execute(
                "INSERT INTO activities(name, description, schedule, max_participants) VALUES (?, ?, ?, ?)",
                (name, data["description"], data["schedule"], data["max_participants"]))
            for p in data["participants"]:
                cur.execute(
                    "INSERT INTO participants(activity_name, email) VALUES (?, ?)",
                    (name, p))
    conn.commit()
    conn.close()

init_db()

def build_activity_dict() -> Dict[str, Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, description, schedule, max_participants FROM activities")
    rows = cur.fetchall()
    activities: Dict[str, Dict[str, Any]] = {}
    for (name, description, schedule, max_participants) in rows:
        cur.execute("SELECT email FROM participants WHERE activity_name = ?", (name,))
        participants = [r[0] for r in cur.fetchall()]
        activities[name] = {
            "description": description,
            "schedule": schedule,
            "max_participants": max_participants,
            "participants": participants,
        }
    conn.close()
    return activities


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return build_activity_dict()


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT max_participants FROM activities WHERE name = ?", (activity_name,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Activity not found")
    max_participants = row[0]
    # Check already signed up
    cur.execute("SELECT 1 FROM participants WHERE activity_name = ? AND email = ?", (activity_name, email))
    if cur.fetchone() is not None:
        conn.close()
        raise HTTPException(status_code=400, detail="Student is already signed up")
    # Enforce capacity
    cur.execute("SELECT COUNT(*) FROM participants WHERE activity_name = ?", (activity_name,))
    count = cur.fetchone()[0]
    if count >= max_participants:
        conn.close()
        raise HTTPException(status_code=400, detail="Activity is full")
    cur.execute("INSERT INTO participants(activity_name, email) VALUES (?, ?)", (activity_name, email))
    conn.commit()
    conn.close()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    conn = get_connection()
    cur = conn.cursor()
    # Validate activity exists
    cur.execute("SELECT 1 FROM activities WHERE name = ?", (activity_name,))
    if cur.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Activity not found")
    cur.execute("SELECT 1 FROM participants WHERE activity_name = ? AND email = ?", (activity_name, email))
    if cur.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")
    cur.execute("DELETE FROM participants WHERE activity_name = ? AND email = ?", (activity_name, email))
    conn.commit()
    conn.close()
    return {"message": f"Unregistered {email} from {activity_name}"}

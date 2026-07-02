# Smart Study Planner Agent

## Goal

Build an AI-powered study planning assistant that helps students efficiently organize their study schedule based on available time, subjects, exam dates, and priorities.

The assistant should generate realistic study plans, split work into Pomodoro sessions, adjust schedules dynamically, and answer productivity-related questions.

---

## Features

- Chat interface
- AI planner agent
- Task prioritization
- Study schedule generation
- Pomodoro breakdown
- Memory of previous study sessions
- Daily summary
- Study recommendations

---

## User Flow

User enters:

- Subjects
- Exam dates
- Hours available

↓

Agent creates plan

↓

User marks tasks complete

↓

Agent updates future schedule

---

## Non Goals

- Authentication
- Payments
- OCR
- Email
- Cloud sync
- Multi-user support
- Database
- Notifications

---

## Architecture

Frontend

↓

Planner Agent

↓

Study Skill

↓

Calendar Skill

↓

Memory

↓

Response

---

## Tech Stack

Python

Google ADK

Gemini

FastAPI

Streamlit

MCP

Agent Skills

---

## Success Criteria

The application should:

- generate study plans
- update plans
- answer study questions
- use MCP tools
- demonstrate Agent Skills
- be deployable
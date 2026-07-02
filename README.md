# Smart Study Planner Agent

> An AI-powered study planning assistant built with **Google Agent Development Kit (ADK)**, **FastAPI**, **Streamlit**, and **MCP** to help students generate personalized study schedules, manage progress, and improve exam preparation.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Google ADK](https://img.shields.io/badge/Google-ADK-orange)
![MCP](https://img.shields.io/badge/MCP-Integrated-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

# Overview

Preparing for multiple exams often requires balancing limited study time across several subjects while ensuring high-priority exams receive sufficient attention.

The **Smart Study Planner Agent** automates this process using an AI-powered agent architecture. Users provide their subjects, exam dates, and available study hours, and the application generates a structured study plan broken into Pomodoro sessions while tracking study history and allowing plans to be updated over time.

This project demonstrates modern AI agent engineering concepts including:

- Google Agent Development Kit (ADK)
- Agent Skills
- Model Context Protocol (MCP)
- FastAPI backend
- Streamlit frontend
- Session memory
- Input validation
- Modular architecture

---

# Features

## AI Study Planner

- Generates personalized study schedules
- Prioritizes subjects with earlier exams
- Allocates available study hours efficiently

---

## Pomodoro Planning

Automatically breaks study sessions into:

- 25 minute focus sessions
- Short breaks
- Daily study schedule

---

## Memory

Keeps track of

- Completed study sessions
- Previous study plans
- Study history

---

## FastAPI Backend

REST API endpoints for:

- Generate Study Plan
- Update Study Plan
- Chat
- History

---

## Streamlit Frontend

Simple interactive dashboard allowing users to:

- Enter subjects
- Add exam dates
- Specify available study hours
- Generate study schedules
- View recommendations

---

## MCP Integration

Demonstrates Model Context Protocol by exposing tool-like functionality for:

- Schedule generation
- Plan updates
- Daily summaries
- Study validation

---

## Google ADK

Implements the main planner as a Google ADK Agent while integrating reusable planning skills.

---

# Architecture

```text
                 Streamlit Frontend
                         │
                         ▼
                  FastAPI Backend
                         │
                         ▼
          Google ADK StudyPlannerAgent
              │         │         │
              ▼         ▼         ▼
        StudySkill Calendar MemorySkill
                         │
                         ▼
                    MCP Tool Layer
```

---

# Project Structure

```text
study-planner-agent/

├── app/
│   └── main.py
│
├── agents/
│   └── planner.py
│
├── frontend/
│   └── app.py
│
├── skills/
│   ├── study.py
│   ├── calendar.py
│   └── memory.py
│
├── mcp/
│   └── mcp_client.py
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# Technology Stack

### Backend

- Python 3.11
- FastAPI
- Uvicorn

### Frontend

- Streamlit

### AI

- Google Agent Development Kit (ADK)
- Google GenAI SDK

### Agent Concepts

- Agent Skills
- MCP
- Memory
- Modular Agents

### Testing

- unittest

---

# Application Workflow

1. User enters study information.
2. Planner Agent validates inputs.
3. Calendar Skill allocates study sessions.
4. Study Skill creates Pomodoro blocks.
5. Memory Skill stores previous plans.
6. MCP layer provides tool functionality.
7. FastAPI returns the generated plan.
8. Streamlit displays the schedule.

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Health Check |
| POST | `/plan/generate` | Generate Study Plan |
| POST | `/plan/update` | Update Existing Plan |
| GET | `/history` | Retrieve Study History |
| DELETE | `/history` | Clear Study History |
| POST | `/chat` | Chat with Planner |

---

# Running the Project

## Clone Repository

```bash
git clone https://github.com/Sohail-Rasul/study-planner-agent.git
cd study-planner-agent
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start Backend

```bash
uvicorn app.main:app --reload
```

FastAPI Documentation:

```
http://127.0.0.1:8000/docs
```

---

## Start Frontend

```bash
streamlit run frontend/app.py
```

---

# Security

The application includes:

- Input validation
- Invalid date detection
- Invalid study hour detection
- Safe request handling
- Modular architecture

No API keys are stored inside the repository.

---

# Testing

Run all tests using:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

# Future Improvements

- Google Calendar integration
- Email reminders
- Authentication
- Cloud deployment
- Multi-user support
- LLM-powered study recommendations
- Adaptive scheduling using user performance

---
# Architecture Overview

The Smart Study Planner Agent follows a modular agent architecture built around the Google Agent Development Kit (ADK). The system separates user interaction, business logic, reusable skills, memory, and external tools into independent components, making the application easier to maintain and extend.

The Streamlit frontend provides an intuitive interface where users enter their subjects, exam dates, and available study hours. These requests are sent to a FastAPI backend, which validates the input before forwarding it to the main StudyPlannerAgent.

The StudyPlannerAgent serves as the orchestration layer of the application. Rather than performing every task itself, it delegates work to specialized skills:

StudySkill generates Pomodoro-based study sessions.
CalendarSkill distributes study sessions across the available days before each exam.
MemorySkill stores previous study plans and completed study sessions to preserve context during runtime.
MCP Tool Layer exposes reusable planning utilities and demonstrates Model Context Protocol integration.

After collecting results from each component, the planner combines them into a structured study plan, which is returned through FastAPI and displayed in the Streamlit interface.

This modular architecture allows new skills and tools to be added with minimal changes to the core planner, making the system scalable and easy to extend.


--- 

# Course Concepts Demonstrated

 Google ADK

 Agent Skills

 MCP

 FastAPI

 Streamlit

 Memory

 Modular Agent Architecture

---

# Acknowledgements

Built as part of the

**5-Day AI Agents: Intensive Vibe Coding Course with Google**

Hosted on Kaggle.

---

# License

This project is licensed under the MIT License.
# XP-Pilot 🧑‍✈️🤖

**XP-Pilot** is an autonomous, event-driven development ecosystem designed to bridge the gap between silent coding errors and professional growth. It functions as a **"Human-in-the-Loop" (HITL) orchestration layer** that monitors your development environment in real-time and provides AI-powered interventions — catching bugs before they cost you, and turning every error into a learning moment.

---

## 🧠 What Is XP-Pilot?

Most developers work in isolation from their mistakes. Errors get suppressed, ignored, or discovered too late. XP-Pilot changes that by acting as an intelligent co-pilot sitting alongside your development process — watching for anomalies, reasoning about them with AI, and surfacing actionable guidance right when you need it.

> *It's not just a debugger. It's a growth engine.*

---

## ✨ Key Features

- 🔍 **Real-Time Environment Monitoring** — Continuously watches your dev environment for errors, exceptions, and anomalies as they happen
- 🤖 **AI-Powered Interventions** — Uses an intelligent agent to analyze issues and suggest or apply fixes automatically
- 🧑‍💼 **Human-in-the-Loop (HITL)** — Keeps you in control with smart prompts before taking action, so you learn, not just fix
- 🐛 **Buggy Code Analysis** — Detects and reasons about problematic code patterns using an AI agent pipeline
- 🛠️ **Extensible Tool System** — Modular `tools.py` architecture makes it easy to add custom intervention capabilities
- 🐳 **Docker-Ready** — Containerized for consistent, reproducible environments across machines
- 🖥️ **Full-Stack Dashboard** — React/TypeScript frontend (`my-app`) for visualizing monitoring state and AI interventions

---

## 🗂️ Project Structure



XP-Pilot/
├── my-app/             # React + TypeScript frontend dashboard
├── pycache/        # Python cache
├── agent.py            # Core AI agent — reasoning & intervention logic
├── buggy_code.py       # Test harness with intentional bugs for agent evaluation
├── main.py             # Application entry point & event loop
├── server.py           # Backend server — bridges frontend and agent
├── tools.py            # Modular toolkit used by the AI agent
├── Dockerfile          # Container configuration
└── .env                # Environment variables & API keys





---

## 🔄 How It Works

Development Environment
│
│ (errors / events)
▼
main.py  ──────────────────────────────────┐
│                                       │
▼                                       ▼
agent.py                               server.py
(AI Reasoning)                        (API Layer)
│                                       │
▼                                       ▼
tools.py                              my-app (UI)
(Actions)                        (Dashboard / HITL)
│
▼
Human Confirmation
│
▼
Fix Applied / Lesson Surfaced




---

## 🛠️ Tech Stack

| Layer       | Technology                    |
|-------------|-------------------------------|
| Backend     | Python                        |
| AI Agent    | LLM-powered (Claude / OpenAI) |
| Frontend    | TypeScript + React + CSS      |
| Infra       | Docker                        |
| Comms       | REST API via `server.py`      |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker (optional but recommended)

### Option A — Run with Docker

```bash
git clone https://github.com/soorajzap/XP-Pilot.git
cd XP-Pilot

# Configure your environment
cp .env .env.local
# Edit .env with your API keys

# Build and run
docker build -t xp-pilot .
docker run --env-file .env.local -p 8000:8000 xp-pilot
```

### Option B — Run Locally

```bash
git clone https://github.com/soorajzap/XP-Pilot.git
cd XP-Pilot

# Backend setup
pip install -r requirements.txt
cp .env .env.local   # Add your API keys

# Start the backend
python main.py

# Frontend setup (separate terminal)
cd my-app
npm install
npm start
```

---

## ⚙️ Configuration

Edit `.env` with your credentials:

```env
ANTHROPIC_API_KEY=your_key_here
# Add any other service keys required by tools.py
```

---

## 🧪 Testing the Agent

`buggy_code.py` contains intentional errors for testing the agent's detection and reasoning capabilities:

```bash
python buggy_code.py
```

Watch how XP-Pilot's agent identifies, reasons about, and surfaces interventions in real time.

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/smarter-interventions`)
3. Commit your changes (`git commit -m 'Add new intervention tool'`)
4. Push to the branch (`git push origin feature/smarter-interventions`)
5. Open a Pull Request

---

## 📄 License

This project is open source. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Sooraj** — [@soorajzap](https://github.com/soorajzap)

---

> *XP-Pilot — Because every bug is a lesson waiting to be learned.*

# StadiumAI — Local Run

This workspace contains a FastAPI backend and a Vite React frontend.

Quick start (two terminals):

Backend

```powershell
cd D:\Chhavi\stadium-ai\backend
python -m venv .venv   # optional
.\.venv\Scripts\Activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend

```powershell
cd D:\Chhavi\stadium-ai\frontend
npm install
npm run dev
```

Notes

- If the OpenRouter API returns `402 Payment Required`, the backend will fall back to a local heuristic for crowd analysis.
- Configure `backend/.env` to set `OPENROUTER_API_KEY` if you want real LLM responses.

Hackathon MVP demo

1. Start backend and frontend (see above).
2. In another terminal run the demo surge script to simulate a crowd surge:

```powershell
cd D:\Chhavi\stadium-ai\demo
python simulate_surge.py
```

3. In the staff UI (`http://localhost:5173`) open "Live Planner" and click "Fetch Plan" — execute suggested actions to observe simulated incidents and planner responses.

Notes: the MVP uses a rule-based planner (`backend/app/planner.py`) and on-edge heuristics for safe fallback. This is intentionally lightweight and demo-friendly for a hackathon MVP.

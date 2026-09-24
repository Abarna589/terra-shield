# TERRA-SHIELD

AI-powered landslide early-warning and risk-monitoring prototype for the
North Eastern Region (NER) — built for SIH26001.

## What it does

TERRA-SHIELD pulls live weather data, calculates a landslide risk score,
visualises it on a GIS map, raises alerts when risk crosses a threshold,
and lets citizens/field officers submit geo-tagged hazard reports —
closing the loop between monitoring and ground-truth verification.

Monitor → Analyse → Predict → Warn → Enable preventive action

## Architecture

React (TypeScript) frontend
        │  HTTP/JSON
        ▼
FastAPI backend
        │
        ├── Open-Meteo API      → live rainfall, soil moisture, temperature
        ├── Risk engine         → rule-based score (see Model below)
        ├── Alert store         → in-memory, triggers on HIGH/CRITICAL
        └── Reports store       → in-memory, citizen-submitted hazard reports
        │
        ▼
Leaflet map (OpenStreetMap tiles) — colored risk zone overlay

## Tech stack

- Frontend: React + TypeScript (Vite), react-leaflet
- Backend: FastAPI (Python), httpx for external API calls
- Weather data: Open-Meteo (free, no API key required)
- Maps: Leaflet + OpenStreetMap tiles

## Running locally

Backend:
    cd backend
    .\.venv\Scripts\Activate.ps1
    fastapi dev main.py

Frontend (separate terminal):
    cd frontend
    npm run dev

Open http://localhost:5173

## API endpoints

GET  /api/v1/health    — service status
GET  /api/v1/weather   — live rainfall / soil moisture / temperature
GET  /api/v1/risk      — computed risk score, level, confidence
GET  /api/v1/alerts    — alerts triggered by HIGH/CRITICAL risk
GET  /api/v1/reports   — submitted field reports
POST /api/v1/reports   — submit a new field report

## Current risk model — honesty note

The current risk score is a **transparent, rule-based baseline**
(rainfall_24h weighted 0.6 + soil_moisture weighted 0.4), not a trained
ML model. It was chosen deliberately for the prototype stage: it's fast
to build, fully explainable, and gives the rest of the system (map,
alerts, reports) a real signal to react to. The architecture is built so
this function can be swapped for a trained model (e.g. LightGBM/XGBoost
on rainfall, soil moisture, slope, elevation, historical landslide data)
without changing any other part of the system.

## Known limitations (by design, for prototype scope)

- Alerts and reports are stored in memory — they reset if the backend
  restarts. A production version would use PostgreSQL + PostGIS.
- Single demo location (Kohima, Nagaland) rather than full NER coverage.
- No offline mode yet — planned as the next milestone.
- No SMS/multilingual delivery yet — alerts currently render on-dashboard.

## Roadmap

1. Trained ML risk model (replacing the rule-based baseline)
2. PostgreSQL + PostGIS for persistent storage and multi-location support
3. Multilingual, priority-based SMS/push alerts
4. Offline maps + mesh/Bluetooth comms for low-connectivity areas
5. Photo/video upload on field reports, feeding back into model retraining
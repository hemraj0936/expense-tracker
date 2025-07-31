#!/bin/bash

# Start FastAPI backend
uvicorn backend.server:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend
streamlit run frontend/app.py --server.port 10000 --server.address 0.0.0.0

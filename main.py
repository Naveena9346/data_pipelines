"""
DataForge Enterprise Data Pipelines Platform — Entry Point
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from backend.main import app

if __name__ == "__main__":
    import uvicorn
    print("Launching DataForge Enterprise Platform backend on http://127.0.0.1:8000...")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

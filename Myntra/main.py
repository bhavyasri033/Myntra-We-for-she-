"""
Myntra Regional Fashion ML Intelligence Service - FastAPI Gateway Entrypoint
AI Backend Intelligence Service powering Myntra's Regional Fashion Recommendation feature.
"""

import uvicorn
from fastapi import FastAPI
from ml_intelligence.api.router import ml_router

app = FastAPI(
    title="Myntra Regional Fashion ML Intelligence Service",
    description="AI Backend Intelligence Service powering Myntra's Regional Fashion Recommendation feature.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount ML Intelligence Router (Developer 2 Gateway Integration)
app.include_router(ml_router)


@app.get("/")
def root():
    """Root endpoint redirecting to health check & documentation."""
    return {
        "service": "Myntra Regional Fashion ML Intelligence Service",
        "status": "ONLINE",
        "docs": "/docs",
        "health": "/api/v1/ml/health"
    }


if __name__ == "__main__":
    print("[INIT] Starting Myntra Regional Fashion ML Intelligence Service on http://localhost:8000 ...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

"""
ML Connector Bridge - Python to TypeScript bridge for ML operations
Enables unconstrained feature extraction and emergent pattern discovery
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import numpy as np
import json
from pathlib import Path
import logging
from datetime import datetime

# Local imports (to be created)
from emergent_intelligence import EmergentIntelligence

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SOLAR EMERGENCE ML Bridge", version="1.0.0")

# Enable CORS for TypeScript frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize emergent intelligence system
intelligence = EmergentIntelligence()

class VideoProcessRequest(BaseModel):
    """Request model for video processing"""
    video_path: str
    video_number: int
    extract_everything: bool = True
    store_raw: bool = True
    discover_patterns: bool = True

class DiscoveryResponse(BaseModel):
    """Response model for discovered patterns"""
    video_number: int
    features_extracted: int
    patterns_discovered: List[Dict[str, Any]]
    correlations_found: List[Dict[str, Any]]
    unknown_signals: List[Dict[str, Any]]
    intelligence_updated: bool
    checkpoint_saved: bool

@app.post("/process_video", response_model=DiscoveryResponse)
async def process_video(request: VideoProcessRequest):
    """
    Process a video with unconstrained extraction
    Extract everything, judge nothing, discover patterns
    """
    try:
        logger.info(f"Processing video {request.video_number}: {request.video_path}")
        
        # Extract everything without filtering
        features = await intelligence.extract_everything(
            video_path=request.video_path,
            constrained=False,
            filter_features=False
        )
        
        # Store raw features without judgment
        if request.store_raw:
            await intelligence.store_raw_features(
                video_number=request.video_number,
                features=features
            )
        
        # Discover patterns without prejudice
        discoveries = await intelligence.discover_patterns(
            features=features,
            video_number=request.video_number,
            use_previous_intelligence=True
        )
        
        # Update sequential intelligence
        intelligence_updated = await intelligence.update_intelligence(
            discoveries=discoveries,
            video_number=request.video_number
        )
        
        # Save checkpoint after each video
        checkpoint_saved = await intelligence.save_checkpoint(
            video_number=request.video_number
        )
        
        return DiscoveryResponse(
            video_number=request.video_number,
            features_extracted=len(features),
            patterns_discovered=discoveries.get("patterns", []),
            correlations_found=discoveries.get("correlations", []),
            unknown_signals=discoveries.get("unknown", []),
            intelligence_updated=intelligence_updated,
            checkpoint_saved=checkpoint_saved
        )
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/intelligence/state")
async def get_intelligence_state():
    """Get current state of emergent intelligence"""
    try:
        state = await intelligence.get_current_state()
        return {
            "videos_processed": state.get("videos_processed", 0),
            "total_patterns": state.get("total_patterns", 0),
            "total_correlations": state.get("total_correlations", 0),
            "unknown_space_used": state.get("unknown_space_used", 0),
            "last_checkpoint": state.get("last_checkpoint", None),
            "intelligence_metrics": state.get("metrics", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/discoveries/recent")
async def get_recent_discoveries(limit: int = 10):
    """Get recent pattern discoveries"""
    try:
        discoveries = await intelligence.get_recent_discoveries(limit=limit)
        return {
            "count": len(discoveries),
            "discoveries": discoveries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/intelligence/checkpoint")
async def create_checkpoint():
    """Manually create an intelligence checkpoint"""
    try:
        checkpoint_path = await intelligence.create_checkpoint()
        return {
            "success": True,
            "checkpoint_path": str(checkpoint_path),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patterns/evolution")
async def get_pattern_evolution():
    """Track how patterns evolve over sequential processing"""
    try:
        evolution = await intelligence.get_pattern_evolution()
        return {
            "evolution_timeline": evolution.get("timeline", []),
            "pattern_strength_over_time": evolution.get("strength", []),
            "emergence_events": evolution.get("emergence_events", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "unconstrained_discovery",
        "ml_bridge": "active",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
Python-Go Bridge for EH²SMAS Swarm Coordination
Connects BMAD Python agents to Go Genkit coordination system
"""

import asyncio
import json
import requests
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentLevel(Enum):
    L1_MICRO_AGENTS = "L1_MICRO_AGENTS"
    L2_DEPARTMENT_MGR = "L2_DEPARTMENT_MGR"
    L3_DIVISION_CHIEF = "L3_DIVISION_CHIEF"
    L4_EXECUTIVE = "L4_EXECUTIVE"
    L5_CEO = "L5_CEO"

@dataclass
class SwarmCoordinationRequest:
    video_id: str
    phase: str
    agent_level: AgentLevel
    agent_id: str
    message: Dict[str, Any]
    correlation_id: str
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

@dataclass
class SwarmCoordinationResponse:
    status: str
    response_data: Dict[str, Any]
    next_actions: List[str]
    agent_assignments: Dict[str, str]
    correlation_id: str
    timestamp: float

class EHSMASBridge:
    """Bridge between Python BMAD agents and Go Genkit coordination"""
    
    def __init__(self, go_coordinator_url: str = "http://localhost:8080"):
        self.go_coordinator_url = go_coordinator_url
        self.active_correlations = {}
        self.agent_state_cache = {}
        
    async def coordinate_agent(self, request: SwarmCoordinationRequest) -> SwarmCoordinationResponse:
        """Send agent coordination request to Go coordinator"""
        try:
            logger.info(f"🌌 Coordinating {request.agent_id} at level {request.agent_level.value}")
            
            # Convert request to JSON
            request_data = {
                "video_id": request.video_id,
                "phase": request.phase,
                "agent_level": request.agent_level.value,
                "agent_id": request.agent_id,
                "message": request.message,
                "correlation_id": request.correlation_id,
                "timestamp": request.timestamp
            }
            
            # Send to Go coordinator
            response = requests.post(
                f"{self.go_coordinator_url}/coordinate",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                response_data = response.json()
                return SwarmCoordinationResponse(
                    status=response_data["status"],
                    response_data=response_data["response_data"],
                    next_actions=response_data["next_actions"],
                    agent_assignments=response_data["agent_assignments"],
                    correlation_id=response_data["correlation_id"],
                    timestamp=response_data["timestamp"]
                )
            else:
                logger.error(f"Go coordinator error: {response.status_code}")
                raise Exception(f"Coordination failed: {response.text}")
                
        except Exception as e:
            logger.error(f"Bridge coordination error: {e}")
            # Return fallback response
            return SwarmCoordinationResponse(
                status="ERROR",
                response_data={"error": str(e)},
                next_actions=[],
                agent_assignments={},
                correlation_id=request.correlation_id,
                timestamp=time.time()
            )
    
    async def track_consensus(self) -> Dict[str, Any]:
        """Get consensus status from Go coordinator"""
        try:
            response = requests.get(f"{self.go_coordinator_url}/consensus", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Consensus tracking failed: {response.status_code}")
                return {"error": "consensus_tracking_failed"}
        except Exception as e:
            logger.error(f"Consensus tracking error: {e}")
            return {"error": str(e)}
    
    async def check_coordinator_health(self) -> bool:
        """Check if Go coordinator is healthy"""
        try:
            response = requests.get(f"{self.go_coordinator_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

class EHSMASAgentCoordinator:
    """High-level coordinator for EH²SMAS agents using Go bridge"""
    
    def __init__(self):
        self.bridge = EHSMASBridge()
        self.current_video_id = None
        self.active_phase = None
        self.agent_registry = {}
        
    async def register_agent(self, agent_id: str, agent_level: AgentLevel, capabilities: List[str]):
        """Register an agent with the coordination system"""
        self.agent_registry[agent_id] = {
            "level": agent_level,
            "capabilities": capabilities,
            "status": "REGISTERED",
            "last_activity": time.time()
        }
        logger.info(f"📝 Registered agent {agent_id} at level {agent_level.value}")
    
    async def start_video_processing(self, video_id: str):
        """Begin coordinated processing of a single video"""
        self.current_video_id = video_id
        self.active_phase = "VIDEO_INTAKE"
        logger.info(f"🎬 Starting EH²SMAS processing for video {video_id}")
        
        # Coordinate video ingestion
        await self.coordinate_phase("VIDEO_INTAKE", ["VideoIngestionSpecialist"])
    
    async def coordinate_phase(self, phase: str, participating_agents: List[str]):
        """Coordinate a specific phase across multiple agents"""
        self.active_phase = phase
        logger.info(f"⚡ Coordinating phase {phase} with {len(participating_agents)} agents")
        
        coordination_tasks = []
        correlation_id = f"{self.current_video_id}_{phase}_{int(time.time())}"
        
        for agent_id in participating_agents:
            if agent_id in self.agent_registry:
                agent_info = self.agent_registry[agent_id]
                
                request = SwarmCoordinationRequest(
                    video_id=self.current_video_id,
                    phase=phase,
                    agent_level=agent_info["level"],
                    agent_id=agent_id,
                    message={"phase_data": phase, "capabilities": agent_info["capabilities"]},
                    correlation_id=correlation_id
                )
                
                task = self.bridge.coordinate_agent(request)
                coordination_tasks.append(task)
        
        # Execute coordination in parallel for same video
        if coordination_tasks:
            responses = await asyncio.gather(*coordination_tasks, return_exceptions=True)
            
            # Process responses
            successful_responses = []
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    logger.error(f"Agent {participating_agents[i]} coordination failed: {response}")
                else:
                    successful_responses.append(response)
                    logger.info(f"✅ Agent {participating_agents[i]} coordinated: {response.status}")
            
            return successful_responses
        
        return []
    
    async def run_full_video_analysis(self, video_id: str):
        """Run complete EH²SMAS analysis on single video"""
        logger.info(f"🌌 Running full EH²SMAS analysis on video {video_id}")
        
        # Phase 1: Video Intake
        await self.start_video_processing(video_id)
        
        # Phase 2: Horizontal Analysis (L1 + L2)
        micro_agents = [aid for aid, info in self.agent_registry.items() 
                       if info["level"] == AgentLevel.L1_MICRO_AGENTS]
        await self.coordinate_phase("HORIZONTAL_ANALYSIS", micro_agents)
        
        department_agents = [aid for aid, info in self.agent_registry.items() 
                           if info["level"] == AgentLevel.L2_DEPARTMENT_MGR]
        await self.coordinate_phase("DEPARTMENT_SYNTHESIS", department_agents)
        
        # Phase 3: Vertical Synthesis (L3 + L4)
        division_agents = [aid for aid, info in self.agent_registry.items() 
                         if info["level"] == AgentLevel.L3_DIVISION_CHIEF]
        await self.coordinate_phase("VERTICAL_SYNTHESIS", division_agents)
        
        executive_agents = [aid for aid, info in self.agent_registry.items() 
                          if info["level"] == AgentLevel.L4_EXECUTIVE]
        await self.coordinate_phase("EXECUTIVE_INTEGRATION", executive_agents)
        
        # Phase 4: Quality Assurance & Consensus
        await self.coordinate_phase("QUALITY_ASSURANCE", ["PatternValidationAgent", "ConsensusOrchestrator"])
        
        # Phase 5: CEO Coordination & Intelligence Accumulation
        ceo_agents = [aid for aid, info in self.agent_registry.items() 
                     if info["level"] == AgentLevel.L5_CEO]
        await self.coordinate_phase("SEQUENTIAL_LEARNING_UPDATE", ceo_agents)
        
        # Check final consensus
        consensus_status = await self.bridge.track_consensus()
        logger.info(f"🎯 Video {video_id} consensus status: {consensus_status}")
        
        return consensus_status

# Example usage and agent registration
async def setup_ehsmas_agents():
    """Setup example EH²SMAS agents for coordination"""
    coordinator = EHSMASAgentCoordinator()
    
    # Register L1 Micro-Agents (examples)
    await coordinator.register_agent("landmark_left_eyebrow_1", AgentLevel.L1_MICRO_AGENTS, ["facial_landmark_detection"])
    await coordinator.register_agent("landmark_right_mouth_corner", AgentLevel.L1_MICRO_AGENTS, ["facial_landmark_detection"])
    await coordinator.register_agent("AU1_InnerBrowRaiser", AgentLevel.L1_MICRO_AGENTS, ["action_unit_detection"])
    await coordinator.register_agent("AU12_LipCornerPuller", AgentLevel.L1_MICRO_AGENTS, ["action_unit_detection"])
    await coordinator.register_agent("audio_F0_contour", AgentLevel.L1_MICRO_AGENTS, ["audio_feature_extraction"])
    
    # Register L2 Department Managers
    await coordinator.register_agent("FacialExpressionDepartment", AgentLevel.L2_DEPARTMENT_MGR, ["facial_synthesis"])
    await coordinator.register_agent("MicroExpressionDepartment", AgentLevel.L2_DEPARTMENT_MGR, ["au_synthesis"])
    await coordinator.register_agent("AudioAnalysisDepartment", AgentLevel.L2_DEPARTMENT_MGR, ["audio_synthesis"])
    
    # Register L3 Division Chiefs
    await coordinator.register_agent("NonverbalIntelligenceDivision", AgentLevel.L3_DIVISION_CHIEF, ["visual_integration"])
    await coordinator.register_agent("VerbalIntelligenceDivision", AgentLevel.L3_DIVISION_CHIEF, ["audio_integration"])
    
    # Register L4 Executives
    await coordinator.register_agent("CrossModalIntegrationExecutive", AgentLevel.L4_EXECUTIVE, ["behavioral_signature_creation"])
    
    # Register L5 CEO
    await coordinator.register_agent("SequentialLearningOrchestrator", AgentLevel.L5_CEO, ["sequential_intelligence_evolution"])
    
    return coordinator

# Integration with BMAD framework
class BMADEHSMASIntegration:
    """Integration layer between BMAD agents and EH²SMAS coordination"""
    
    def __init__(self):
        self.coordinator = None
        
    async def initialize(self):
        """Initialize EH²SMAS coordination system"""
        self.coordinator = await setup_ehsmas_agents()
        
        # Check Go coordinator health
        if await self.coordinator.bridge.check_coordinator_health():
            logger.info("✅ Go coordinator is healthy and ready")
        else:
            logger.warning("⚠️ Go coordinator not available - using fallback mode")
    
    async def process_video_with_ehsmas(self, video_path: str, video_id: str):
        """Process a video using EH²SMAS coordination"""
        if self.coordinator:
            return await self.coordinator.run_full_video_analysis(video_id)
        else:
            logger.error("❌ EH²SMAS coordinator not initialized")
            return {"error": "coordinator_not_initialized"}

# Example main function
async def main():
    """Example of running EH²SMAS coordination"""
    integration = BMADEHSMASIntegration()
    await integration.initialize()
    
    # Process a video
    result = await integration.process_video_with_ehsmas("video_001.mp4", "video_001")
    print("🎯 EH²SMAS Processing Result:", json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
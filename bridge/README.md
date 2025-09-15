# EH²SMAS Go Bridge with Genkit

## Overview

This bridge connects the Python BMAD agents to a Go-based coordination system using Google's Genkit framework for enhanced observability and performance in managing 511+ agents across the holarchical hierarchy.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Python BMAD   │───▶│   Go Genkit      │───▶│  Genkit Dev UI  │
│     Agents      │    │   Coordinator    │    │   (Monitoring)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                       │                       │
        │              ┌────────▼────────┐             │
        │              │ EH²SMAS State   │             │
        └──────────────▶│    Tracker      │◀────────────┘
                       └─────────────────┘
```

## Setup Instructions

### 1. Prerequisites
```bash
# Install Go (if not already installed)
brew install go

# Verify Go installation
go version  # Should be 1.22+
```

### 2. Initialize Go Module
```bash
cd bridge/go-agent-coordinator
go mod init github.com/Bodhi1111/solar-emergence/bridge/go-agent-coordinator
```

### 3. Install Dependencies
```bash
# Install Genkit dependencies
go get github.com/firebase/genkit/go/genkit

# Install additional dependencies for HTTP server
go mod tidy
```

### 4. Start Go Coordinator
```bash
# Start the Go coordination server
go run swarm_coordinator.go

# Server will start on http://localhost:8080
```

### 5. Setup Genkit Developer UI
```bash
# Install Genkit CLI (one-time setup)
npm install -g genkit-cli

# Start Genkit developer UI for monitoring
genkit dev

# Browse to http://localhost:4000 for swarm monitoring
```

## Agent Coordination Flows

### L1: Micro-Agents (511+ agents)
- **468 Facial Landmark Agents**: Individual coordinate tracking
- **43 Action Unit Agents**: FACS micro-expression detection  
- **Audio Feature Agents**: Spectral, prosodic, temporal analysis

### L2: Department Managers (4 agents)
- **Facial Expression Department**: Synthesizes landmark agents
- **Micro-Expression Department**: Coordinates action unit agents
- **Audio Analysis Department**: Integrates audio feature agents
- **Temporal Dynamics Department**: Manages timing agents

### L3: Division Chiefs (3 agents)
- **Nonverbal Intelligence Division**: Visual behavior synthesis
- **Verbal Intelligence Division**: Audio behavior synthesis
- **Temporal Intelligence Division**: Timing pattern synthesis

### L4: Executives (2 agents)
- **Cross-Modal Integration Executive**: Behavioral signature creation
- **Pattern Validation Executive**: Quality assurance

### L5: CEO (1 agent)
- **Sequential Learning Orchestrator**: Intelligence evolution across videos

## API Endpoints

### POST /coordinate
Coordinate agent actions across the hierarchy.

**Request:**
```json
{
  "video_id": "video_001",
  "phase": "HORIZONTAL_ANALYSIS", 
  "agent_level": "L1_MICRO_AGENTS",
  "agent_id": "landmark_left_eyebrow_1",
  "message": {"landmark_data": [0.234, 0.567]},
  "correlation_id": "video_001_phase_1",
  "timestamp": 1704067200
}
```

**Response:**
```json
{
  "status": "COORDINATED",
  "response_data": {
    "agent_level": "L1_MICRO_SPECIALIST",
    "coordination_mode": "PARALLEL_ON_SAME_VIDEO"
  },
  "next_actions": ["EXTRACT_FACIAL_LANDMARK"],
  "agent_assignments": {"facial_department": "AGGREGATE_LANDMARKS"},
  "correlation_id": "video_001_phase_1",
  "timestamp": 1704067201
}
```

### GET /consensus
Track consensus status across all hierarchy levels.

**Response:**
```json
{
  "consensus_by_level": {
    "L1_micro_agents": 0.85,
    "L2_department_mgrs": 0.92,
    "L3_division_chiefs": 0.88,
    "L4_executives": 0.95
  },
  "overall_consensus": 0.90,
  "consensus_threshold_met": true
}
```

### GET /health
Check coordinator health status.

**Response:**
```json
{
  "status": "HEALTHY",
  "architecture": "EH²SMAS",
  "active_agents": 536,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Python Integration

### Basic Usage
```python
from bridge.python_go_bridge import EHSMASBridge, SwarmCoordinationRequest, AgentLevel

# Initialize bridge
bridge = EHSMASBridge()

# Coordinate an agent
request = SwarmCoordinationRequest(
    video_id="video_001",
    phase="HORIZONTAL_ANALYSIS",
    agent_level=AgentLevel.L1_MICRO_AGENTS,
    agent_id="landmark_left_eyebrow_1", 
    message={"landmark_coordinates": [0.234, 0.567]},
    correlation_id="video_001_1704067200"
)

response = await bridge.coordinate_agent(request)
print(f"Coordination status: {response.status}")
```

### Full Video Processing
```python
from bridge.python_go_bridge import BMADEHSMASIntegration

# Initialize integration
integration = BMADEHSMASIntegration()
await integration.initialize()

# Process video with full EH²SMAS coordination
result = await integration.process_video_with_ehsmas("video_001.mp4", "video_001")
```

## Monitoring & Observability

### Genkit Developer UI
- **Flow Visualization**: See agent coordination flows in real-time
- **Trace Analysis**: Track individual agent interactions
- **Performance Metrics**: Monitor consensus building and response times
- **Error Tracking**: Debug coordination failures

### Key Metrics
- **Active Agents**: Number of agents currently processing
- **Consensus Levels**: Agreement scores across hierarchy levels
- **Processing Performance**: Time per coordination cycle
- **Error Rates**: Failed coordination attempts

## Integration with BMAD

The Go coordinator integrates seamlessly with your existing BMAD framework:

1. **Agent Registration**: Python agents register with Go coordinator
2. **Phase Coordination**: BMAD orchestrates phases, Go coordinates agents
3. **State Synchronization**: Shared state between Python and Go systems
4. **Consensus Building**: Go manages multi-level consensus protocols
5. **Sequential Learning**: Go tracks intelligence evolution across videos

## Development Workflow

### 1. Add New Agent Type
```go
// In swarm_coordinator.go
func coordinateNewAgentType(ctx context.Context, input *SwarmCoordinationRequest, response *SwarmCoordinationResponse) (*SwarmCoordinationResponse, error) {
    // Add coordination logic for new agent type
    return response, nil
}
```

### 2. Register in Python
```python
# In python_go_bridge.py
await coordinator.register_agent("new_agent_id", AgentLevel.L1_MICRO_AGENTS, ["new_capability"])
```

### 3. Test Coordination
```bash
# Start Go coordinator
go run swarm_coordinator.go

# Run Python integration test
python bridge/python_go_bridge.py
```

### 4. Monitor in Genkit UI
```bash
# Start monitoring
genkit dev

# Browse to http://localhost:4000
# View coordination flows and traces
```

## Performance Optimization

### For Mac M2 Max
- **Concurrent Goroutines**: Up to 10 cores for agent coordination
- **Memory Efficiency**: Optimized for 64GB unified memory
- **Local Processing**: No external API calls or cloud dependencies
- **HTTP Keep-Alive**: Persistent connections for Python bridge

### Scaling Considerations
- **Agent Batching**: Process agents in optimal batch sizes
- **Consensus Caching**: Cache consensus calculations where possible
- **State Compression**: Efficient state representation
- **Connection Pooling**: Reuse HTTP connections

## Troubleshooting

### Common Issues

**Go coordinator not starting:**
```bash
# Check Go installation
go version

# Verify dependencies
go mod tidy

# Run with verbose logging
go run -v swarm_coordinator.go
```

**Python bridge connection failed:**
```python
# Check coordinator health
healthy = await bridge.check_coordinator_health()
print(f"Coordinator healthy: {healthy}")

# Use fallback mode if needed
if not healthy:
    logger.warning("Using fallback coordination mode")
```

**Genkit UI not accessible:**
```bash
# Restart Genkit dev server
genkit dev --port 4000

# Check for port conflicts
lsof -i :4000
```

This bridge provides robust, observable coordination for your EH²SMAS architecture while maintaining the performance and local-only constraints of Solar Emergence.
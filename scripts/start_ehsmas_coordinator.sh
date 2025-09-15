#!/bin/bash

# Start EH²SMAS Go Coordinator with Genkit Monitoring
# SINGULAR SEQUENTIAL PROCESSING ONLY - One video at a time with 511+ agent coordination

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🌌 Starting EH²SMAS Go Coordinator with Genkit Monitoring${NC}"
echo -e "${BLUE}======================================================================${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Go is installed
check_go_installation() {
    print_info "Checking Go installation..."
    
    if ! command -v go &> /dev/null; then
        print_error "Go is not installed. Installing via Homebrew..."
        brew install go
        print_status "Go installed successfully"
    else
        GO_VERSION=$(go version | cut -d' ' -f3)
        print_status "Go is installed: $GO_VERSION"
    fi
}

# Check if Genkit CLI is installed
check_genkit_installation() {
    print_info "Checking Genkit CLI installation..."
    
    if ! command -v genkit &> /dev/null; then
        print_warning "Genkit CLI not found. Installing..."
        npm install -g genkit-cli
        print_status "Genkit CLI installed successfully"
    else
        print_status "Genkit CLI is available"
    fi
}

# Setup Go module if needed
setup_go_module() {
    print_info "Setting up Go module for EH²SMAS coordinator..."
    
    cd bridge/go-agent-coordinator
    
    if [ ! -f "go.mod" ]; then
        print_info "Initializing Go module..."
        go mod init github.com/Bodhi1111/solar-emergence/bridge/go-agent-coordinator
    fi
    
    print_info "Installing Go dependencies..."
    go get github.com/firebase/genkit/go/genkit
    go mod tidy
    
    print_status "Go module setup complete"
    cd ../..
}

# Start Go coordinator in background
start_go_coordinator() {
    print_info "Starting EH²SMAS Go Coordinator..."
    
    cd bridge/go-agent-coordinator
    
    # Kill any existing coordinator process
    pkill -f "swarm_coordinator" || true
    
    # Start coordinator in background
    nohup go run swarm_coordinator.go > ../../logs/go_coordinator.log 2>&1 &
    GO_PID=$!
    
    echo $GO_PID > ../../logs/go_coordinator.pid
    
    print_status "Go Coordinator started (PID: $GO_PID)"
    print_info "Logs available at: logs/go_coordinator.log"
    
    cd ../..
}

# Wait for coordinator to be ready
wait_for_coordinator() {
    print_info "Waiting for Go Coordinator to be ready..."
    
    for i in {1..30}; do
        if curl -s http://localhost:8080/health > /dev/null 2>&1; then
            print_status "Go Coordinator is ready and healthy"
            return 0
        fi
        echo -n "."
        sleep 1
    done
    
    print_error "Go Coordinator failed to start within 30 seconds"
    return 1
}

# Start Genkit developer UI
start_genkit_ui() {
    print_info "Starting Genkit Developer UI for swarm monitoring..."
    
    cd bridge/go-agent-coordinator
    
    # Kill any existing Genkit UI process
    pkill -f "genkit dev" || true
    
    # Start Genkit UI in background
    nohup genkit dev --port 4000 > ../../logs/genkit_ui.log 2>&1 &
    GENKIT_PID=$!
    
    echo $GENKIT_PID > ../../logs/genkit_ui.pid
    
    print_status "Genkit Developer UI started (PID: $GENKIT_PID)"
    print_info "UI available at: http://localhost:4000"
    print_info "Logs available at: logs/genkit_ui.log"
    
    cd ../..
}

# Test the coordinator
test_coordinator() {
    print_info "Testing EH²SMAS coordinator functionality..."
    
    # Test health endpoint
    HEALTH_RESPONSE=$(curl -s http://localhost:8080/health)
    if echo "$HEALTH_RESPONSE" | grep -q "HEALTHY"; then
        print_status "Health check passed"
    else
        print_error "Health check failed"
        return 1
    fi
    
    # Test consensus endpoint
    CONSENSUS_RESPONSE=$(curl -s http://localhost:8080/consensus)
    if echo "$CONSENSUS_RESPONSE" | grep -q "consensus_by_level"; then
        print_status "Consensus tracking operational"
    else
        print_error "Consensus tracking failed"
        return 1
    fi
    
    print_status "All coordinator tests passed"
}

# Display status and URLs
display_status() {
    echo
    echo -e "${PURPLE}🎯 EH²SMAS Go Coordinator Status${NC}"
    echo -e "${BLUE}================================${NC}"
    echo
    echo -e "${GREEN}✅ Go Coordinator:${NC} http://localhost:8080"
    echo -e "${GREEN}✅ Genkit Dev UI:${NC}  http://localhost:4000"
    echo
    echo -e "${BLUE}📊 Available Endpoints:${NC}"
    echo -e "   POST /coordinate  - Agent coordination"
    echo -e "   GET  /consensus   - Consensus tracking"
    echo -e "   GET  /health      - Health status"
    echo
    echo -e "${BLUE}📁 Log Files:${NC}"
    echo -e "   logs/go_coordinator.log - Go coordinator logs"
    echo -e "   logs/genkit_ui.log     - Genkit UI logs"
    echo
    echo -e "${YELLOW}🔧 Process Management:${NC}"
    echo -e "   Stop coordinator: ./scripts/stop_ehsmas_coordinator.sh"
    echo -e "   View logs: tail -f logs/go_coordinator.log"
    echo
}

# Create logs directory if it doesn't exist
mkdir -p logs

# Main execution
main() {
    check_go_installation
    check_genkit_installation
    setup_go_module
    start_go_coordinator
    
    if wait_for_coordinator; then
        start_genkit_ui
        
        # Brief wait for Genkit UI to start
        sleep 3
        
        if test_coordinator; then
            display_status
            
            echo -e "${GREEN}🚀 EH²SMAS Go Coordinator with Genkit monitoring is ready!${NC}"
            echo -e "${BLUE}Process 511+ agents across holarchical hierarchy with full observability${NC}"
        else
            print_error "Coordinator tests failed"
            exit 1
        fi
    else
        print_error "Failed to start coordinator"
        exit 1
    fi
}

# Trap to cleanup on exit
cleanup() {
    print_info "Cleaning up background processes..."
    if [ -f logs/go_coordinator.pid ]; then
        kill $(cat logs/go_coordinator.pid) 2>/dev/null || true
        rm -f logs/go_coordinator.pid
    fi
    if [ -f logs/genkit_ui.pid ]; then
        kill $(cat logs/genkit_ui.pid) 2>/dev/null || true
        rm -f logs/genkit_ui.pid
    fi
}

trap cleanup EXIT

main "$@"
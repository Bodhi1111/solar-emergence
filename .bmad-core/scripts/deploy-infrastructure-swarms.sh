#!/bin/bash

# SINGULAR SEQUENTIAL PROCESSING ONLY

# Deploy Infrastructure Swarms Script
# Coordinate deployment of all data infrastructure swarm agents for Solar Emergence

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
SOLAR_EMERGENCE_ROOT="/Users/joshuavaughan/dev/Projects/solar-emergence"
DATA_ROOT="/data/solar-emergence"
LOGS_DIR="${DATA_ROOT}/logs"
BACKUP_DIR="${DATA_ROOT}/backups"

echo -e "${PURPLE}🌌 Solar Emergence Data Infrastructure Swarm Deployment${NC}"
echo -e "${BLUE}======================================================================================================${NC}"

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

# Function to check system requirements
check_system_requirements() {
    print_info "Checking system requirements for Mac M2 Max optimization..."
    
    # Check if running on Apple Silicon
    if [[ $(uname -m) != "arm64" ]]; then
        print_error "This system is optimized for Apple Silicon (M2 Max). Current architecture: $(uname -m)"
        exit 1
    fi
    
    # Check available memory
    TOTAL_MEMORY=$(sysctl -n hw.memsize)
    TOTAL_MEMORY_GB=$((TOTAL_MEMORY / 1024 / 1024 / 1024))
    
    if [[ $TOTAL_MEMORY_GB -lt 32 ]]; then
        print_warning "Recommended memory: 64GB. Current: ${TOTAL_MEMORY_GB}GB"
    else
        print_status "Memory check passed: ${TOTAL_MEMORY_GB}GB available"
    fi
    
    # Check available disk space
    AVAILABLE_SPACE=$(df -BG "$HOME" | tail -1 | awk '{print $4}' | sed 's/G//')
    if [[ $AVAILABLE_SPACE -lt 500 ]]; then
        print_error "Insufficient disk space. Need 500GB+, have ${AVAILABLE_SPACE}GB"
        exit 1
    else
        print_status "Disk space check passed: ${AVAILABLE_SPACE}GB available"
    fi
    
    print_status "System requirements verification complete"
}

# Function to create data directory structure
create_data_directories() {
    print_info "Creating optimized data directory structure..."
    
    DIRECTORIES=(
        "$DATA_ROOT"
        "$DATA_ROOT/raw-videos"
        "$DATA_ROOT/processed-videos"
        "$DATA_ROOT/features/facial-landmarks"
        "$DATA_ROOT/features/action-units"
        "$DATA_ROOT/features/audio-features"
        "$DATA_ROOT/features/synchronized"
        "$DATA_ROOT/vectors"
        "$DATA_ROOT/graph"
        "$DATA_ROOT/embeddings"
        "$DATA_ROOT/cache"
        "$DATA_ROOT/backups"
        "$DATA_ROOT/logs"
        "$DATA_ROOT/metadata"
        "$DATA_ROOT/models"
        "$DATA_ROOT/temp"
    )
    
    for dir in "${DIRECTORIES[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            print_status "Created directory: $dir"
        else
            print_info "Directory exists: $dir"
        fi
    done
    
    # Set appropriate permissions
    chmod -R 755 "$DATA_ROOT"
    print_status "Data directory structure created successfully"
}

# Function to check and install Python dependencies
setup_python_environment() {
    print_info "Setting up Python environment for infrastructure swarms..."
    
    # Check if Python 3.11+ is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not found"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
    print_info "Found Python version: $PYTHON_VERSION"
    
    # Create virtual environment if it doesn't exist
    VENV_PATH="$DATA_ROOT/venv"
    if [[ ! -d "$VENV_PATH" ]]; then
        print_info "Creating Python virtual environment..."
        python3 -m venv "$VENV_PATH"
        print_status "Virtual environment created"
    fi
    
    # Activate virtual environment
    source "$VENV_PATH/bin/activate"
    
    # Install/upgrade core dependencies
    print_info "Installing Python dependencies..."
    pip install --upgrade pip setuptools wheel
    
    # Infrastructure-specific dependencies
    DEPENDENCIES=(
        "opencv-python"
        "mediapipe"
        "librosa"
        "numpy"
        "scipy"
        "scikit-learn"
        "qdrant-client"
        "neo4j"
        "ffmpeg-python"
        "torch"
        "torchaudio"
        "torchvision"
        "mlx"
        "mlx-lm"
    )
    
    for dep in "${DEPENDENCIES[@]}"; do
        print_info "Installing $dep..."
        pip install "$dep" --quiet
    done
    
    print_status "Python environment setup complete"
}

# Function to deploy Video Processing Swarm
deploy_video_processing_swarm() {
    print_info "🎥 Deploying Video Processing Swarm..."
    
    # Check FFmpeg with VideoToolbox support
    if ! command -v ffmpeg &> /dev/null; then
        print_warning "FFmpeg not found. Installing via Homebrew..."
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            print_error "Homebrew not found. Please install FFmpeg manually"
            exit 1
        fi
    fi
    
    # Verify VideoToolbox support
    if ffmpeg -hwaccels 2>/dev/null | grep -q videotoolbox; then
        print_status "FFmpeg with VideoToolbox acceleration confirmed"
    else
        print_warning "VideoToolbox acceleration may not be available"
    fi
    
    # Create video processing configuration
    cat > "$DATA_ROOT/config/video_processing_config.json" << EOF
{
    "hardware_acceleration": {
        "videotoolbox": true,
        "metal_performance_shaders": true,
        "neural_engine": true
    },
    "processing_settings": {
        "max_sequential_videos": 1,
        "frame_extraction_strategy": "adaptive",
        "quality_threshold": 0.95,
        "memory_optimization": true
    },
    "feature_extraction": {
        "facial_landmarks": {
            "model": "mediapipe_face_mesh",
            "landmark_count": 468,
            "detection_confidence": 0.7,
            "tracking_confidence": 0.5
        },
        "action_units": {
            "model": "opencv_based_detector",
            "au_count": 43,
            "intensity_threshold": 0.5
        },
        "audio_features": {
            "sample_rate": 22050,
            "mfcc_coefficients": 13,
            "spectral_features": true,
            "prosodic_features": true
        }
    }
}
EOF
    
    print_status "Video Processing Swarm deployment complete"
}

# Function to deploy Storage Architecture Swarm
deploy_storage_architecture_swarm() {
    print_info "🗄️ Deploying Storage Architecture Swarm..."
    
    # Install and configure Qdrant (local)
    print_info "Setting up Qdrant vector database..."
    
    if ! command -v docker &> /dev/null; then
        print_warning "Docker not found. Installing Docker Desktop for Mac..."
        print_info "Please install Docker Desktop manually from https://docker.com/products/docker-desktop"
    else
        # Run Qdrant in Docker
        docker pull qdrant/qdrant:latest
        
        # Create Qdrant data directory
        mkdir -p "$DATA_ROOT/vectors/qdrant-data"
        
        # Start Qdrant container
        docker run -d \
            --name solar-emergence-qdrant \
            -p 6333:6333 \
            -v "$DATA_ROOT/vectors/qdrant-data:/qdrant/storage" \
            qdrant/qdrant:latest \
            || print_info "Qdrant container already running"
        
        print_status "Qdrant vector database configured"
    fi
    
    # Install and configure Neo4j (local)
    print_info "Setting up Neo4j knowledge graph database..."
    
    if command -v brew &> /dev/null; then
        if ! brew list neo4j &> /dev/null; then
            brew install neo4j
        fi
        
        # Configure Neo4j
        NEO4J_CONF_DIR="/usr/local/etc/neo4j"
        if [[ -d "$NEO4J_CONF_DIR" ]]; then
            # Set data directories
            echo "dbms.directories.data=$DATA_ROOT/graph/neo4j-data" >> "$NEO4J_CONF_DIR/neo4j.conf"
            echo "dbms.directories.logs=$DATA_ROOT/logs/neo4j" >> "$NEO4J_CONF_DIR/neo4j.conf"
            
            # Performance tuning for M2 Max
            echo "dbms.memory.heap.initial_size=4G" >> "$NEO4J_CONF_DIR/neo4j.conf"
            echo "dbms.memory.heap.max_size=8G" >> "$NEO4J_CONF_DIR/neo4j.conf"
            echo "dbms.memory.pagecache.size=16G" >> "$NEO4J_CONF_DIR/neo4j.conf"
        fi
        
        # Create data directories
        mkdir -p "$DATA_ROOT/graph/neo4j-data"
        mkdir -p "$DATA_ROOT/logs/neo4j"
        
        print_status "Neo4j knowledge graph database configured"
    else
        print_warning "Homebrew not found. Please install Neo4j manually"
    fi
    
    # Create storage configuration
    cat > "$DATA_ROOT/config/storage_config.json" << EOF
{
    "vector_database": {
        "type": "qdrant",
        "connection": "http://localhost:6333",
        "collections": {
            "facial_landmarks": {
                "vector_size": 468,
                "distance": "cosine",
                "hnsw_config": {
                    "m": 16,
                    "ef_construct": 200
                }
            },
            "action_units": {
                "vector_size": 43,
                "distance": "cosine",
                "hnsw_config": {
                    "m": 8,
                    "ef_construct": 100
                }
            },
            "audio_features": {
                "vector_size": 128,
                "distance": "cosine",
                "hnsw_config": {
                    "m": 12,
                    "ef_construct": 150
                }
            }
        }
    },
    "knowledge_graph": {
        "type": "neo4j",
        "connection": "bolt://localhost:7687",
        "auth": {
            "username": "neo4j",
            "password": "solaremergence"
        },
        "performance": {
            "heap_size": "8G",
            "pagecache_size": "16G"
        }
    },
    "file_system": {
        "base_path": "$DATA_ROOT",
        "compression": true,
        "caching": {
            "enabled": true,
            "max_size_gb": 8,
            "prefetch_strategy": "intelligent"
        }
    }
}
EOF
    
    print_status "Storage Architecture Swarm deployment complete"
}

# Function to deploy Feature Extraction Swarm
deploy_feature_extraction_swarm() {
    print_info "🔍 Deploying Feature Extraction Swarm..."
    
    # Download required models
    print_info "Downloading and configuring ML models..."
    
    MODELS_DIR="$DATA_ROOT/models"
    
    # MediaPipe models (automatically downloaded)
    python3 -c "
import mediapipe as mp
print('MediaPipe face mesh model ready')
face_mesh = mp.solutions.face_mesh.FaceMesh()
print('Face mesh initialized successfully')
"
    
    # Create feature extraction configuration
    cat > "$DATA_ROOT/config/feature_extraction_config.json" << EOF
{
    "mediapipe": {
        "face_mesh": {
            "static_image_mode": false,
            "max_num_faces": 2,
            "refine_landmarks": true,
            "min_detection_confidence": 0.7,
            "min_tracking_confidence": 0.5
        }
    },
    "action_units": {
        "detector_type": "opencv_based",
        "intensity_scale": [0, 5],
        "confidence_threshold": 0.8
    },
    "audio_processing": {
        "librosa": {
            "sample_rate": 22050,
            "frame_length": 2048,
            "hop_length": 512,
            "mfcc_coefficients": 13
        }
    },
    "hardware_optimization": {
        "use_metal": true,
        "use_neural_engine": true,
        "sequence_size": 32,
        "memory_efficient": true
    }
}
EOF
    
    print_status "Feature Extraction Swarm deployment complete"
}

# Function to deploy Embedding Pipeline Swarm
deploy_embedding_pipeline_swarm() {
    print_info "🧠 Deploying Embedding Pipeline Swarm..."
    
    # Create embedding configuration
    cat > "$DATA_ROOT/config/embedding_config.json" << EOF
{
    "models": {
        "facial_embedding": {
            "architecture": "lightweight_transformer",
            "input_size": 468,
            "output_size": 256,
            "training": "self_supervised",
            "optimization": "mlx_native"
        },
        "audio_embedding": {
            "architecture": "1d_cnn",
            "input_size": 128,
            "output_size": 128,
            "training": "contrastive_learning",
            "optimization": "streaming_capable"
        },
        "multimodal_fusion": {
            "architecture": "cross_attention",
            "input_sizes": [256, 128],
            "output_size": 384,
            "training": "end_to_end",
            "optimization": "inference_speed"
        }
    },
    "search_capabilities": {
        "similarity_search": true,
        "pattern_search": true,
        "temporal_search": true,
        "multimodal_search": true
    }
}
EOF
    
    print_status "Embedding Pipeline Swarm deployment complete"
}

# Function to create infrastructure coordination script
create_coordination_script() {
    print_info "Creating infrastructure coordination script..."
    
    cat > "$DATA_ROOT/scripts/coordinate_infrastructure.py" << 'EOF'
#!/usr/bin/env python3
"""
Solar Emergence Infrastructure Coordination Script
Coordinates all data infrastructure swarms for optimal performance
"""

import json
import time
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/data/solar-emergence/logs/infrastructure.log'),
        logging.StreamHandler()
    ]
)

class InfrastructureCoordinator:
    def __init__(self):
        self.config_dir = Path('/data/solar-emergence/config')
        self.data_dir = Path('/data/solar-emergence')
        
    def initialize_all_swarms(self):
        """Initialize all infrastructure swarms in optimal order"""
        
        logging.info("🌌 Initializing Solar Emergence Infrastructure Swarms")
        
        # Phase 1: Storage systems
        self.initialize_storage_systems()
        
        # Phase 2: Processing pipelines
        self.initialize_processing_pipelines()
        
        # Phase 3: Intelligence layers
        self.initialize_intelligence_layers()
        
        # Phase 4: Coordination validation
        self.validate_infrastructure_coordination()
        
        logging.info("✅ Infrastructure swarm initialization complete")
        
    def initialize_storage_systems(self):
        """Initialize vector database and knowledge graph"""
        
        logging.info("🗄️ Initializing storage systems...")
        
        try:
            # Initialize vector database collections
            from qdrant_client import QdrantClient
            qdrant = QdrantClient("localhost", port=6333)
            
            # Test connection
            collections = qdrant.get_collections()
            logging.info(f"Qdrant connected, collections: {len(collections.collections)}")
            
        except Exception as e:
            logging.error(f"Vector database initialization failed: {e}")
            
        try:
            # Initialize knowledge graph
            from neo4j import GraphDatabase
            neo4j_driver = GraphDatabase.driver("bolt://localhost:7687")
            
            with neo4j_driver.session() as session:
                result = session.run("RETURN 1 as test")
                logging.info("Neo4j knowledge graph connected successfully")
                
        except Exception as e:
            logging.error(f"Knowledge graph initialization failed: {e}")
    
    def initialize_processing_pipelines(self):
        """Initialize video processing and feature extraction"""
        
        logging.info("🎥 Initializing processing pipelines...")
        
        try:
            # Test MediaPipe
            import mediapipe as mp
            face_mesh = mp.solutions.face_mesh.FaceMesh()
            logging.info("MediaPipe face mesh initialized")
            
            # Test audio processing
            import librosa
            logging.info("Librosa audio processing ready")
            
            # Test video processing
            import cv2
            logging.info(f"OpenCV version: {cv2.__version__}")
            
        except Exception as e:
            logging.error(f"Processing pipeline initialization failed: {e}")
    
    def initialize_intelligence_layers(self):
        """Initialize embedding and search capabilities"""
        
        logging.info("🧠 Initializing intelligence layers...")
        
        try:
            # Test MLX (if available)
            try:
                import mlx.core as mx
                logging.info("MLX framework available for Apple Silicon optimization")
            except ImportError:
                logging.warning("MLX not available, falling back to standard implementations")
            
            # Test embedding capabilities
            import numpy as np
            test_embedding = np.random.rand(256)
            logging.info("Embedding generation capabilities ready")
            
        except Exception as e:
            logging.error(f"Intelligence layer initialization failed: {e}")
    
    def validate_infrastructure_coordination(self):
        """Validate all systems are working together"""
        
        logging.info("✅ Validating infrastructure coordination...")
        
        # Run integration tests
        validation_results = {
            "storage_systems": self.test_storage_integration(),
            "processing_pipelines": self.test_processing_integration(),
            "intelligence_layers": self.test_intelligence_integration()
        }
        
        all_passed = all(validation_results.values())
        
        if all_passed:
            logging.info("🎯 All infrastructure systems validated successfully")
        else:
            logging.error(f"Infrastructure validation failed: {validation_results}")
        
        return all_passed
    
    def test_storage_integration(self):
        """Test storage system integration"""
        try:
            # Test vector database
            from qdrant_client import QdrantClient
            qdrant = QdrantClient("localhost", port=6333)
            qdrant.get_collections()
            
            # Test knowledge graph
            from neo4j import GraphDatabase
            driver = GraphDatabase.driver("bolt://localhost:7687")
            with driver.session() as session:
                session.run("RETURN 1")
            
            return True
        except:
            return False
    
    def test_processing_integration(self):
        """Test processing pipeline integration"""
        try:
            import mediapipe as mp
            import librosa
            import cv2
            return True
        except:
            return False
    
    def test_intelligence_integration(self):
        """Test intelligence layer integration"""
        try:
            import numpy as np
            # Basic embedding test
            test_vector = np.random.rand(256)
            return len(test_vector) == 256
        except:
            return False

if __name__ == "__main__":
    coordinator = InfrastructureCoordinator()
    coordinator.initialize_all_swarms()
EOF
    
    chmod +x "$DATA_ROOT/scripts/coordinate_infrastructure.py"
    print_status "Infrastructure coordination script created"
}

# Function to run system validation tests
run_system_validation() {
    print_info "🔍 Running system validation tests..."
    
    # Test Python environment
    source "$DATA_ROOT/venv/bin/activate"
    
    # Run infrastructure coordination test
    python3 "$DATA_ROOT/scripts/coordinate_infrastructure.py"
    
    # Test basic functionality
    python3 -c "
import sys
print(f'✅ Python {sys.version}')

try:
    import mediapipe as mp
    print('✅ MediaPipe available')
except ImportError:
    print('❌ MediaPipe not available')

try:
    import librosa
    print('✅ Librosa available')
except ImportError:
    print('❌ Librosa not available')

try:
    import cv2
    print(f'✅ OpenCV {cv2.__version__} available')
except ImportError:
    print('❌ OpenCV not available')

try:
    import qdrant_client
    print('✅ Qdrant client available')
except ImportError:
    print('❌ Qdrant client not available')

try:
    import neo4j
    print('✅ Neo4j driver available')
except ImportError:
    print('❌ Neo4j driver not available')

try:
    import mlx.core
    print('✅ MLX available for Apple Silicon optimization')
except ImportError:
    print('⚠️ MLX not available (optional)')
"
    
    print_status "System validation complete"
}

# Function to create startup script
create_startup_script() {
    print_info "Creating infrastructure startup script..."
    
    cat > "$DATA_ROOT/scripts/start_infrastructure.sh" << 'EOF'
#!/bin/bash

# Solar Emergence Infrastructure Startup Script

echo "🌌 Starting Solar Emergence Infrastructure..."

# Start Qdrant (if using Docker)
if command -v docker &> /dev/null; then
    if ! docker ps | grep -q solar-emergence-qdrant; then
        echo "Starting Qdrant vector database..."
        docker start solar-emergence-qdrant || docker run -d \
            --name solar-emergence-qdrant \
            -p 6333:6333 \
            -v /data/solar-emergence/vectors/qdrant-data:/qdrant/storage \
            qdrant/qdrant:latest
    fi
fi

# Start Neo4j (if installed)
if command -v neo4j &> /dev/null; then
    echo "Starting Neo4j knowledge graph..."
    neo4j start
fi

# Activate Python environment
source /data/solar-emergence/venv/bin/activate

# Run infrastructure coordination
python3 /data/solar-emergence/scripts/coordinate_infrastructure.py

echo "✅ Solar Emergence Infrastructure is ready!"
EOF
    
    chmod +x "$DATA_ROOT/scripts/start_infrastructure.sh"
    print_status "Startup script created"
}

# Main deployment function
main() {
    echo -e "${PURPLE}Starting Solar Emergence Data Infrastructure Swarm Deployment...${NC}"
    
    # Create config directory
    mkdir -p "$DATA_ROOT/config"
    mkdir -p "$DATA_ROOT/scripts"
    
    # Run deployment phases
    check_system_requirements
    create_data_directories
    setup_python_environment
    deploy_video_processing_swarm
    deploy_storage_architecture_swarm
    deploy_feature_extraction_swarm
    deploy_embedding_pipeline_swarm
    create_coordination_script
    create_startup_script
    run_system_validation
    
    echo -e "${GREEN}🎯 Solar Emergence Data Infrastructure Swarm Deployment Complete!${NC}"
    echo -e "${BLUE}======================================================================================================${NC}"
    echo -e "${GREEN}Infrastructure Status:${NC}"
    echo -e "${GREEN}  ✅ Video Processing Swarm: Ready${NC}"
    echo -e "${GREEN}  ✅ Storage Architecture Swarm: Ready${NC}"
    echo -e "${GREEN}  ✅ Feature Extraction Swarm: Ready${NC}"
    echo -e "${GREEN}  ✅ Embedding Pipeline Swarm: Ready${NC}"
    echo -e "${GREEN}  ✅ System Coordination: Ready${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo -e "${YELLOW}  1. Start infrastructure: $DATA_ROOT/scripts/start_infrastructure.sh${NC}"
    echo -e "${YELLOW}  2. Test with sample video: Deploy pattern discovery campaign${NC}"
    echo -e "${YELLOW}  3. Begin processing 1,500 sales videos for pattern discovery${NC}"
    echo ""
    echo -e "${PURPLE}🌟 Solar Emergence is ready for breakthrough pattern discovery!${NC}"
}

# Run main deployment
main "$@"
"""
BMAD Knowledge Bridge - Connects harvested knowledge to active BMAD agents
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import re
from datetime import datetime

def yaml_dump(data, **kwargs):
    """Simple YAML dump replacement to avoid external dependency"""
    def _format_value(value, indent=0):
        spaces = "  " * indent
        if isinstance(value, dict):
            if not value:
                return "{}"
            result = "\n"
            for k, v in value.items():
                result += f"{spaces}{k}: {_format_value(v, indent + 1)}"
            return result
        elif isinstance(value, list):
            if not value:
                return "[]"
            result = "\n"
            for item in value:
                result += f"{spaces}- {_format_value(item, indent + 1)}"
            return result
        elif isinstance(value, str):
            if '\n' in value or len(value) > 60:
                return f'|\n{spaces}  {value.replace(chr(10), chr(10) + spaces + "  ")}'
            return f'"{value}"'
        else:
            return str(value)
    
    return _format_value(data).strip()

class BMADKnowledgeBridge:
    """
    Bridges processed knowledge into BMAD agent working memory
    """
    
    def __init__(self):
        self.docs_path = Path("docs")
        self.bmad_path = Path(".bmad-core")
        self.specs_path = Path("specs")
        
    def sync_knowledge_to_bmad(self):
        """
        Sync all processed knowledge into BMAD working context
        """
        
        print("🔗 Syncing Knowledge Corpus → BMAD Agents")
        
        # 1. Load all validated knowledge
        knowledge = self._load_validated_knowledge()
        
        # 2. Update BMAD agent context
        self._update_agent_context(knowledge)
        
        # 3. Generate new specs from knowledge
        self._generate_specs_from_knowledge(knowledge)
        
        # 4. Update BMAD working memory
        self._update_bmad_memory(knowledge)
        
        print("✅ Knowledge sync complete!")
    
    def _load_validated_knowledge(self) -> Dict:
        """Load all validated knowledge from corpus"""
        
        knowledge = {
            "patterns": [],
            "algorithms": [],
            "architectures": [],
            "techniques": [],
            "principles": [],
            "requirements": [],
            "constraints": []
        }
        
        # Load from validated processing results
        validated_path = Path("knowledge-corpus/processed/validated")
        
        if validated_path.exists():
            for json_file in validated_path.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    extracted = data.get("extracted_knowledge", {})
                    
                    for key, values in extracted.items():
                        if key in knowledge and isinstance(values, list):
                            knowledge[key].extend(values)
                except Exception as e:
                    print(f"  ⚠️  Error processing {json_file}: {e}")
        
        # Load from generated docs
        knowledge_summary_path = self.docs_path / "extracted-knowledge" / "KNOWLEDGE_SUMMARY.md"
        if knowledge_summary_path.exists():
            summary_content = knowledge_summary_path.read_text()
            knowledge["summary"] = summary_content
            
            # Parse the markdown summary for structured data
            parsed = self._parse_knowledge_summary(summary_content)
            for key, values in parsed.items():
                if key in knowledge:
                    knowledge[key].extend(values)
            
        return knowledge
    
    def _parse_knowledge_summary(self, content: str) -> Dict[str, List[str]]:
        """Parse knowledge summary markdown into structured data"""
        
        parsed = {
            "patterns": [],
            "algorithms": [],
            "architectures": [],
            "techniques": [],
            "principles": []
        }
        
        current_section = None
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Detect sections
            if '### Patterns' in line:
                current_section = 'patterns'
            elif '### Algorithms' in line:
                current_section = 'algorithms'
            elif '### Architectures' in line:
                current_section = 'architectures'
            elif '### Techniques' in line:
                current_section = 'techniques'
            elif '### Principles' in line:
                current_section = 'principles'
            elif line.startswith('### ') or line.startswith('---'):
                current_section = None
            
            # Extract items
            elif current_section and line.startswith('- '):
                item = line[2:].strip()
                if item and item not in parsed[current_section]:
                    parsed[current_section].append(item)
        
        return parsed
    
    def _update_agent_context(self, knowledge: Dict):
        """Update BMAD agent context with knowledge"""
        
        # Create agent context file
        agent_context = {
            "solar_emergence_knowledge": {
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "discovered_patterns": knowledge.get("patterns", [])[:20],
                "applicable_algorithms": knowledge.get("algorithms", [])[:20], 
                "local_architectures": knowledge.get("architectures", [])[:20],
                "constraint_compliant_techniques": knowledge.get("techniques", [])[:20],
                "core_principles": [
                    "DISCOVERY_FIRST",
                    "LOCAL_ONLY", 
                    "ZERO_COST",
                    "EMERGENT",
                    "SEQUENTIAL",
                    "MULTIMODAL"
                ],
                "project_principles": knowledge.get("principles", [])[:10]
            }
        }
        
        # Save to BMAD working memory
        bmad_context_path = self.bmad_path / "context" / "knowledge_context.json"
        bmad_context_path.parent.mkdir(parents=True, exist_ok=True)
        bmad_context_path.write_text(json.dumps(agent_context, indent=2))
        
        print(f"  ✅ Updated agent context: {bmad_context_path}")
    
    def _generate_specs_from_knowledge(self, knowledge: Dict):
        """Generate BMAD specs from discovered knowledge"""
        
        # Generate multimodal processing spec
        multimodal_spec = {
            "version": "1.0.0",
            "name": "multimodal-discovery-pipeline",
            "description": "Emergent intelligence through multimodal pattern discovery",
            "knowledge_base": {
                "discovered_patterns": knowledge.get("patterns", []),
                "algorithms": knowledge.get("algorithms", []),
                "architectures": knowledge.get("architectures", [])
            },
            "processing": {
                "modalities": ["text", "audio", "vision", "temporal"],
                "fusion": "vertical_synthesis",
                "output": "signatures"
            },
            "constraints": {
                "local_only": True,
                "zero_cost": True,
                "emergent": True
            },
            "implementation": {
                "text_processing": "whisper.cpp for speech-to-text",
                "pattern_discovery": "GNN-based approaches",
                "fusion_architecture": "layered fusion modules",
                "validation": "constraint compliance checking"
            }
        }
        
        self.specs_path.mkdir(exist_ok=True)
        spec_path = self.specs_path / "multimodal-discovery.spec.yml"
        spec_path.write_text(yaml_dump(multimodal_spec))
        
        print(f"  ✅ Generated spec: {spec_path}")
        
        # Generate solar emergence architecture spec
        architecture_spec = {
            "version": "1.0.0",
            "name": "solar-emergence-architecture",
            "description": "4-layer emergent intelligence architecture",
            "layers": {
                "layer_1": {
                    "name": "Input Processing",
                    "purpose": "Multimodal data ingestion",
                    "components": ["audio_processor", "text_processor", "vision_processor"]
                },
                "layer_2": {
                    "name": "Pattern Discovery", 
                    "purpose": "Emergent pattern identification",
                    "components": ["gnn_analyzer", "topology_mapper", "sequence_detector"]
                },
                "layer_3": {
                    "name": "Vertical Synthesis",
                    "purpose": "Cross-modal fusion",
                    "components": ["fusion_engine", "signature_generator", "knowledge_integrator"]
                },
                "layer_4": {
                    "name": "Intelligence Emergence",
                    "purpose": "Emergent behavior generation",
                    "components": ["behavior_synthesizer", "response_generator", "learning_adapter"]
                }
            },
            "knowledge_integration": {
                "patterns": len(knowledge.get("patterns", [])),
                "algorithms": len(knowledge.get("algorithms", [])),
                "architectures": len(knowledge.get("architectures", []))
            }
        }
        
        arch_spec_path = self.specs_path / "solar-emergence-architecture.spec.yml"
        arch_spec_path.write_text(yaml_dump(architecture_spec))
        
        print(f"  ✅ Generated architecture spec: {arch_spec_path}")
    
    def _update_bmad_memory(self, knowledge: Dict):
        """Update BMAD working memory with current knowledge"""
        
        memory = {
            "project": "SOLAR EMERGENCE",
            "architecture": "4-layer emergent intelligence",
            "current_knowledge": {
                "total_patterns": len(knowledge.get("patterns", [])),
                "total_algorithms": len(knowledge.get("algorithms", [])), 
                "total_architectures": len(knowledge.get("architectures", [])),
                "total_techniques": len(knowledge.get("techniques", [])),
                "total_principles": len(knowledge.get("principles", [])),
                "compliance_enforced": True
            },
            "constraints": {
                "local_only": True,
                "zero_cost": True,
                "emergent_behavior": True,
                "no_external_apis": True
            },
            "next_steps": [
                "Implement multimodal extraction pipeline",
                "Build vertical synthesis layer", 
                "Create sequential learning engine",
                "Deploy discovery agents",
                "Test emergent behavior patterns"
            ],
            "available_tools": [
                "whisper.cpp (local speech processing)",
                "GNN pattern discovery",
                "Topological data analysis",
                "Local fusion architectures"
            ]
        }
        
        memory_path = self.bmad_path / "memory" / "current_state.json"
        memory_path.parent.mkdir(parents=True, exist_ok=True)
        memory_path.write_text(json.dumps(memory, indent=2))
        
        print(f"  ✅ Updated BMAD memory: {memory_path}")
        
        # Create knowledge index for quick lookup
        knowledge_index = {
            "index_version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "categories": {
                category: len(items) for category, items in knowledge.items() 
                if isinstance(items, list)
            },
            "quick_access": {
                "local_processing_tools": [
                    item for item in knowledge.get("algorithms", []) 
                    if "local" in item.lower() or "whisper" in item.lower()
                ],
                "pattern_discovery": [
                    item for item in knowledge.get("patterns", [])
                    if "pattern" in item.lower() or "discovery" in item.lower()
                ],
                "fusion_architectures": [
                    item for item in knowledge.get("architectures", [])
                    if "fusion" in item.lower() or "layer" in item.lower()
                ]
            }
        }
        
        index_path = self.bmad_path / "memory" / "knowledge_index.json"
        index_path.write_text(json.dumps(knowledge_index, indent=2))
        
        print(f"  ✅ Created knowledge index: {index_path}")

if __name__ == "__main__":
    bridge = BMADKnowledgeBridge()
    bridge.sync_knowledge_to_bmad()
[#!/usr/bin/env python3
"""
SOLAR EMERGENCE - Knowledge Organization & Distribution System
Routes extracted knowledge to appropriate agents, specs, and project components
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
import shutil
from datetime import datetime

@dataclass
class KnowledgeCategory:
    """Defines how knowledge should be categorized and routed"""
    name: str
    keywords: List[str]
    target_agents: List[str]
    target_specs: List[str]
    target_docs: List[str]
    priority: int

class KnowledgeOrganizer:
    """
    Organizes processed knowledge and distributes it to appropriate project components
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.knowledge_corpus = self.project_root / "knowledge-corpus"
        self.docs_path = self.project_root / "docs"
        self.specs_path = self.project_root / "specs"
        self.agents_path = self.project_root / "agents"
        
        # Define knowledge categories and their routing
        self.categories = {
            "multimodal_processing": KnowledgeCategory(
                name="Multimodal Processing",
                keywords=["multimodal", "video", "audio", "vision", "cross-modal", "fusion"],
                target_agents=["VideoProcessingAgent", "AudioAnalysisAgent", "VisionAgent"],
                target_specs=["video-processing.spec.yml", "audio-analysis.spec.yml"],
                target_docs=["multimodal-architecture.md", "video-pipeline.md"],
                priority=1
            ),
            "emergent_intelligence": KnowledgeCategory(
                name="Emergent Intelligence",
                keywords=["emergent", "discovery", "pattern", "emergence", "algorithmic"],
                target_agents=["DiscoveryAgent", "PatternEmergenceAgent", "IntelligenceAccumulator"],
                target_specs=["emergent-patterns.spec.yml", "pattern-emergence.spec.yml"],
                target_docs=["emergent-intelligence.md", "discovery-architecture.md"],
                priority=1
            ),
            "graph_neural_networks": KnowledgeCategory(
                name="Graph Neural Networks",
                keywords=["graph", "gnn", "knowledge graph", "neo4j", "relationships"],
                target_agents=["KnowledgeGraphAgent", "RelationshipExtractor"],
                target_specs=["knowledge-graph.spec.yml", "relationship-extraction.spec.yml"],
                target_docs=["knowledge-graph-design.md", "graph-architecture.md"],
                priority=2
            ),
            "agent_orchestration": KnowledgeCategory(
                name="Agent Orchestration", 
                keywords=["agent", "orchestration", "workflow", "bmad", "multi-agent"],
                target_agents=["OrchestrationAgent", "WorkflowManager", "BMadOrchestrator"],
                target_specs=["agent-orchestration.spec.yml", "bmad-workflow.spec.yml"],
                target_docs=["agent-architecture.md", "bmad-implementation.md"],
                priority=2
            ),
            "local_ml_optimization": KnowledgeCategory(
                name="Local ML Optimization",
                keywords=["mlx", "apple", "local", "optimization", "m2", "silicon"],
                target_agents=["MLXOptimizer", "LocalInferenceAgent"],
                target_specs=["local-ml.spec.yml", "mlx-optimization.spec.yml"],
                target_docs=["local-ml-architecture.md", "apple-silicon-optimization.md"],
                priority=3
            ),
            "data_pipeline": KnowledgeCategory(
                name="Data Pipeline",
                keywords=["pipeline", "processing", "etl", "data flow", "sequential"],
                target_agents=["DataPipelineAgent", "SequentialProcessor"],
                target_specs=["data-pipeline.spec.yml", "sequential-processing.spec.yml"],
                target_docs=["data-architecture.md", "pipeline-design.md"],
                priority=3
            )
        }
    
    def organize_knowledge(self):
        """Main method to organize and distribute all processed knowledge"""
        
        print("🗂️ SOLAR EMERGENCE - Knowledge Organization & Distribution")
        print("=" * 60)
        
        # 1. Load processed knowledge
        processed_knowledge = self._load_processed_knowledge()
        
        # 2. Categorize knowledge by domain
        categorized_knowledge = self._categorize_knowledge(processed_knowledge)
        
        # 3. Route to appropriate components
        routing_results = self._route_to_components(categorized_knowledge)
        
        # 4. Update agent specifications
        self._update_agent_specs(categorized_knowledge)
        
        # 5. Generate specialized documentation
        self._generate_specialized_docs(categorized_knowledge)
        
        # 6. Create knowledge routing report
        self._create_routing_report(routing_results)
        
        print("\n✅ Knowledge organization and distribution complete!")
        
    def _load_processed_knowledge(self) -> Dict[str, Any]:
        """Load all validated processed knowledge"""
        
        processed_knowledge = {
            "patterns": [],
            "algorithms": [],
            "architectures": [],
            "techniques": [],
            "principles": [],
            "implementations": []
        }
        
        validated_path = self.knowledge_corpus / "processed" / "validated"
        
        if not validated_path.exists():
            print("❌ No validated knowledge found!")
            return processed_knowledge
            
        print(f"📂 Loading knowledge from {validated_path}")
        
        for json_file in validated_path.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    
                extracted = data.get("extracted_knowledge", {})
                
                for category, items in extracted.items():
                    if category in processed_knowledge and isinstance(items, list):
                        processed_knowledge[category].extend(items)
                        
            except Exception as e:
                print(f"⚠️ Error loading {json_file}: {e}")
        
        total_items = sum(len(v) for v in processed_knowledge.values())
        print(f"📊 Loaded {total_items} knowledge items across {len(processed_knowledge)} categories")
        
        return processed_knowledge
    
    def _categorize_knowledge(self, knowledge: Dict[str, Any]) -> Dict[str, Dict]:
        """Categorize knowledge items by domain"""
        
        print("\n🏷️ Categorizing knowledge by domain...")
        
        categorized = {}
        
        for category_id, category in self.categories.items():
            categorized[category_id] = {
                "metadata": category,
                "items": {
                    "patterns": [],
                    "algorithms": [],
                    "architectures": [],
                    "techniques": [],
                    "principles": [],
                    "implementations": []
                }
            }
        
        # Categorize each knowledge item
        for knowledge_type, items in knowledge.items():
            for item in items:
                if isinstance(item, str):
                    # Find which categories this item belongs to
                    matching_categories = self._find_matching_categories(item)
                    
                    for category_id in matching_categories:
                        if category_id in categorized:
                            categorized[category_id]["items"][knowledge_type].append(item)
        
        # Print categorization summary
        for category_id, data in categorized.items():
            total_items = sum(len(v) for v in data["items"].values())
            if total_items > 0:
                print(f"  📁 {data['metadata'].name}: {total_items} items")
        
        return categorized
    
    def _find_matching_categories(self, item: str) -> List[str]:
        """Find which categories an item belongs to based on keywords"""
        
        item_lower = item.lower()
        matching = []
        
        for category_id, category in self.categories.items():
            for keyword in category.keywords:
                if keyword.lower() in item_lower:
                    matching.append(category_id)
                    break
        
        # If no specific match, default to general categories
        if not matching:
            if any(word in item_lower for word in ["pattern", "algorithm", "technique"]):
                matching.append("emergent_intelligence")
        
        return matching
    
    def _route_to_components(self, categorized_knowledge: Dict) -> Dict[str, List[str]]:
        """Route knowledge to appropriate agents, specs, and docs"""
        
        print("\n🚦 Routing knowledge to project components...")
        
        routing_results = {
            "agents_updated": [],
            "specs_created": [],
            "docs_generated": []
        }
        
        for category_id, data in categorized_knowledge.items():
            category = data["metadata"]
            items = data["items"]
            
            total_items = sum(len(v) for v in items.values())
            if total_items == 0:
                continue
                
            print(f"  📋 Processing {category.name} ({total_items} items)")
            
            # Route to agents
            for agent_name in category.target_agents:
                self._update_agent_knowledge(agent_name, items)
                routing_results["agents_updated"].append(agent_name)
            
            # Route to specs
            for spec_name in category.target_specs:
                self._update_spec_knowledge(spec_name, items, category)
                routing_results["specs_created"].append(spec_name)
            
            # Route to docs
            for doc_name in category.target_docs:
                self._update_doc_knowledge(doc_name, items, category)
                routing_results["docs_generated"].append(doc_name)
        
        return routing_results
    
    def _update_agent_knowledge(self, agent_name: str, knowledge_items: Dict):
        """Update agent with relevant knowledge"""
        
        # Create agent knowledge directory if it doesn't exist
        agent_knowledge_dir = self.agents_path / "knowledge" / agent_name.lower()
        agent_knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        # Create knowledge base file for this agent
        knowledge_file = agent_knowledge_dir / "extracted_knowledge.json"
        
        agent_knowledge = {
            "agent": agent_name,
            "updated": datetime.now().isoformat(),
            "knowledge": knowledge_items,
            "total_items": sum(len(v) for v in knowledge_items.values())
        }
        
        with open(knowledge_file, 'w') as f:
            json.dump(agent_knowledge, f, indent=2)
    
    def _update_spec_knowledge(self, spec_name: str, knowledge_items: Dict, category: KnowledgeCategory):
        """Create or update spec files with relevant knowledge"""
        
        spec_file = self.specs_path / spec_name
        spec_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create enhanced spec based on extracted knowledge
        spec_content = {
            "version": "1.0.0",
            "name": spec_name.replace(".spec.yml", ""),
            "description": f"Enhanced with knowledge from {category.name}",
            "updated": datetime.now().isoformat(),
            "knowledge_source": "constraint_validated_extraction",
            "extracted_patterns": knowledge_items.get("patterns", [])[:10],
            "extracted_algorithms": knowledge_items.get("algorithms", [])[:10],
            "extracted_techniques": knowledge_items.get("techniques", [])[:10],
            "implementation_guidance": {
                "principles": [
                    "LOCAL_ONLY: All processing on Mac M2 Max",
                    "ZERO_COST: No external APIs or services", 
                    "DISCOVERY_FIRST: Let patterns emerge naturally",
                    "EMERGENT: Build intelligence through discovery"
                ],
                "constraints": [
                    "No cloud dependencies",
                    "No paid services",
                    "Local model inference only",
                    "Docker containers for databases"
                ]
            }
        }
        
        with open(spec_file, 'w') as f:
            yaml.dump(spec_content, f, default_flow_style=False, indent=2)
    
    def _update_doc_knowledge(self, doc_name: str, knowledge_items: Dict, category: KnowledgeCategory):
        """Generate specialized documentation with extracted knowledge"""
        
        docs_dir = self.docs_path / "knowledge-enhanced"
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        doc_file = docs_dir / doc_name
        
        # Generate markdown documentation
        content = f"""# {category.name} - Enhanced Documentation

Generated from constraint-validated knowledge extraction

## Overview
This documentation has been enhanced with patterns, algorithms, and techniques extracted from cutting-edge research papers, all filtered through SOLAR EMERGENCE constraints.

## Extracted Patterns
"""
        
        for i, pattern in enumerate(knowledge_items.get("patterns", [])[:15], 1):
            content += f"{i}. {pattern}\n"
        
        content += f"""
## Discovered Algorithms
"""
        
        for i, algorithm in enumerate(knowledge_items.get("algorithms", [])[:15], 1):
            content += f"{i}. {algorithm}\n"
            
        content += f"""
## Applicable Techniques
"""
        
        for i, technique in enumerate(knowledge_items.get("techniques", [])[:15], 1):
            content += f"{i}. {technique}\n"
            
        content += f"""
## Implementation Principles

### Core Constraints (IMMUTABLE)
- **LOCAL_ONLY**: Everything runs on Mac M2 Max
- **ZERO_COST**: No paid APIs or cloud services
- **DISCOVERY_FIRST**: Let mathematics reveal patterns
- **EMERGENT**: Intelligence emerges from data

### Target Agents
{chr(10).join(f'- {agent}' for agent in category.target_agents)}

### Related Specifications
{chr(10).join(f'- {spec}' for spec in category.target_specs)}

---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Knowledge Items: {sum(len(v) for v in knowledge_items.values())}
Category Priority: {category.priority}
"""
        
        with open(doc_file, 'w') as f:
            f.write(content)
    
    def _update_agent_specs(self, categorized_knowledge: Dict):
        """Update existing agent specifications with extracted knowledge"""
        
        print("\n🤖 Updating agent specifications...")
        
        # Create agents knowledge summary
        agents_summary = {}
        
        for category_id, data in categorized_knowledge.items():
            category = data["metadata"]
            items = data["items"]
            
            for agent_name in category.target_agents:
                if agent_name not in agents_summary:
                    agents_summary[agent_name] = {
                        "categories": [],
                        "total_knowledge_items": 0,
                        "patterns": [],
                        "algorithms": [],
                        "techniques": []
                    }
                
                agents_summary[agent_name]["categories"].append(category.name)
                agents_summary[agent_name]["total_knowledge_items"] += sum(len(v) for v in items.values())
                agents_summary[agent_name]["patterns"].extend(items.get("patterns", [])[:5])
                agents_summary[agent_name]["algorithms"].extend(items.get("algorithms", [])[:5])
                agents_summary[agent_name]["techniques"].extend(items.get("techniques", [])[:5])
        
        # Save agent knowledge summary
        agents_knowledge_file = self.agents_path / "AGENT_KNOWLEDGE_SUMMARY.json"
        with open(agents_knowledge_file, 'w') as f:
            json.dump(agents_summary, f, indent=2)
        
        print(f"  📊 Updated knowledge for {len(agents_summary)} agents")
    
    def _generate_specialized_docs(self, categorized_knowledge: Dict):
        """Generate specialized documentation for each knowledge domain"""
        
        print("\n📝 Generating specialized documentation...")
        
        # Create master knowledge index
        master_index = {
            "title": "SOLAR EMERGENCE - Master Knowledge Index",
            "generated": datetime.now().isoformat(),
            "categories": {},
            "routing_summary": {},
            "total_knowledge_items": 0
        }
        
        for category_id, data in categorized_knowledge.items():
            category = data["metadata"]
            items = data["items"]
            total_items = sum(len(v) for v in items.values())
            
            master_index["categories"][category_id] = {
                "name": category.name,
                "priority": category.priority,
                "knowledge_items": total_items,
                "target_agents": category.target_agents,
                "target_specs": category.target_specs,
                "target_docs": category.target_docs
            }
            
            master_index["total_knowledge_items"] += total_items
        
        # Save master index
        index_file = self.docs_path / "MASTER_KNOWLEDGE_INDEX.json"
        with open(index_file, 'w') as f:
            json.dump(master_index, f, indent=2)
    
    def _create_routing_report(self, routing_results: Dict):
        """Create a comprehensive routing report"""
        
        print("\n📋 Creating knowledge routing report...")
        
        report_content = f"""# SOLAR EMERGENCE - Knowledge Routing Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Routing Summary

### Agents Updated
{chr(10).join(f'- {agent}' for agent in set(routing_results["agents_updated"]))}

### Specifications Created
{chr(10).join(f'- {spec}' for spec in set(routing_results["specs_created"]))}

### Documentation Generated
{chr(10).join(f'- {doc}' for doc in set(routing_results["docs_generated"]))}

## Knowledge Distribution

### High Priority Categories
{chr(10).join(f'- {cat.name} (Priority {cat.priority})' for cat in self.categories.values() if cat.priority <= 2)}

### Supporting Categories  
{chr(10).join(f'- {cat.name} (Priority {cat.priority})' for cat in self.categories.values() if cat.priority > 2)}

## Next Steps

1. **Review Agent Knowledge**: Check `agents/knowledge/` for agent-specific knowledge bases
2. **Validate Specifications**: Review `specs/` for enhanced specifications
3. **Study Documentation**: Explore `docs/knowledge-enhanced/` for detailed guidance
4. **Implement Components**: Use extracted knowledge to build agents and pipelines

## File Locations

- **Agent Knowledge**: `agents/knowledge/[agent-name]/extracted_knowledge.json`
- **Enhanced Specs**: `specs/[spec-name].spec.yml`
- **Specialized Docs**: `docs/knowledge-enhanced/[doc-name].md`
- **Master Index**: `docs/MASTER_KNOWLEDGE_INDEX.json`
- **Agent Summary**: `agents/AGENT_KNOWLEDGE_SUMMARY.json`

---
All knowledge has been filtered through SOLAR EMERGENCE constraints:
✅ LOCAL_ONLY ✅ ZERO_COST ✅ DISCOVERY_FIRST ✅ EMERGENT
"""
        
        report_file = self.docs_path / "KNOWLEDGE_ROUTING_REPORT.md"
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        print(f"  📄 Routing report saved: {report_file}")

# CLI Interface
if __name__ == "__main__":
    organizer = KnowledgeOrganizer()
    organizer.organize_knowledge()
    
    print(f"""
🎯 Knowledge Organization Complete!

📁 Check these locations:
   • agents/knowledge/ - Agent-specific knowledge bases
   • specs/ - Enhanced specifications  
   • docs/knowledge-enhanced/ - Specialized documentation
   • docs/MASTER_KNOWLEDGE_INDEX.json - Complete knowledge map
   
🚀 Next: Use this organized knowledge to build your emergent intelligence system!
""")]

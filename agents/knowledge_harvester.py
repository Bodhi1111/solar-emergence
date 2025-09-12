"""
SOLAR EMERGENCE - Knowledge Processing Pipeline
Processes corpus through constraints into project artifacts
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from constraint_enforcer import ConstraintEnforcer, ProjectConstraints

class KnowledgeProcessingPipeline:
    """
    Pipeline that processes raw knowledge corpus into project artifacts
    while maintaining strict constraint compliance
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.corpus_path = self.project_root / "knowledge-corpus"
        self.docs_path = self.project_root / "docs"
        
        # Initialize constraint enforcer
        self.enforcer = ConstraintEnforcer()
        
        # Processing stats
        self.stats = {
            "files_processed": 0,
            "violations_found": 0,
            "translations_made": 0,
            "knowledge_extracted": 0,
            "compliance_scores": []
        }
    
    def process_corpus(self):
        """Process entire knowledge corpus through constraints"""
        
        print("🚀 SOLAR EMERGENCE - Knowledge Harvester")
        print("=" * 50)
        print("Processing knowledge corpus with constraint enforcement...")
        print()
        
        # Ensure output directories exist
        self._setup_output_directories()
        
        # Process each file in raw-inputs
        raw_inputs = self.corpus_path / "raw-inputs"
        
        if not raw_inputs.exists():
            print("❌ No raw-inputs directory found!")
            print(f"Create: {raw_inputs}")
            print("Then add documents to process.")
            return
        
        # Find all files to process
        files_to_process = []
        for pattern in ["**/*.md", "**/*.txt", "**/*.json", "**/*.yml"]:
            files_to_process.extend(raw_inputs.glob(pattern))
        
        if not files_to_process:
            print("📝 No files found in raw-inputs/")
            print("Add documents to knowledge-corpus/raw-inputs/ and try again.")
            return
        
        print(f"📂 Found {len(files_to_process)} files to process")
        print()
        
        # Process each file
        processed_knowledge = {}
        
        for file_path in files_to_process:
            result = self._process_file(file_path)
            if result:
                processed_knowledge[str(file_path.name)] = result
        
        # Generate project artifacts from processed knowledge
        if processed_knowledge:
            self._generate_artifacts(processed_knowledge)
        
        # Print summary
        self._print_summary()
    
    def _setup_output_directories(self):
        """Setup output directories"""
        dirs = [
            self.corpus_path / "processed" / "validated",
            self.corpus_path / "processed" / "rejected",
            self.docs_path / "planning",
            self.docs_path / "architecture", 
            self.docs_path / "extracted-knowledge"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single file through constraints"""
        
        print(f"📄 Processing: {file_path.name}")
        
        try:
            content = file_path.read_text(errors='ignore')
            
            # Process through constraint enforcer
            result = self.enforcer.enforce_constraints(
                content=content,
                source=str(file_path.relative_to(self.corpus_path))
            )
            
            # Calculate compliance score
            violations_count = len(result['scan_result']['violations'])
            content_length = len(content.split())
            compliance_score = max(0, 1 - (violations_count * 0.1))  # Simple scoring
            
            # Extract knowledge from content
            extracted_knowledge = self._extract_knowledge(content)
            
            processed_result = {
                'original_source': result['original_source'],
                'violations_found': [v['type'] for v in result['scan_result']['violations']],
                'translations_made': [v['alternative'] for v in result['scan_result']['violations']],
                'compliance_score': compliance_score,
                'extracted_knowledge': extracted_knowledge,
                'processing_metadata': result
            }
            
            # Update stats
            self.stats["files_processed"] += 1
            self.stats["violations_found"] += violations_count
            self.stats["translations_made"] += len(result['scan_result']['violations'])
            self.stats["compliance_scores"].append(compliance_score)
            
            # Save processed result
            if compliance_score > 0.3:  # Reasonable compliance threshold
                # Good compliance - save to validated
                output_path = self.corpus_path / "processed" / "validated" / f"{file_path.stem}_processed.json"
                output_path.write_text(json.dumps(processed_result, indent=2))
                print(f"  ✅ Validated (compliance: {compliance_score:.2f})")
                
                # Show translations made
                if processed_result["translations_made"]:
                    print(f"  🔄 Translations: {', '.join(processed_result['translations_made'][:3])}")
                    if len(processed_result['translations_made']) > 3:
                        print(f"      ... and {len(processed_result['translations_made']) - 3} more")
                
                return processed_result
                
            else:
                # Poor compliance - save to rejected
                output_path = self.corpus_path / "processed" / "rejected" / f"{file_path.stem}_rejected.json"
                output_path.write_text(json.dumps(processed_result, indent=2))
                print(f"  ❌ Rejected (compliance: {compliance_score:.2f})")
                print(f"      Violations: {processed_result['violations_found']}")
                
        except Exception as e:
            print(f"  ⚠️ Error processing: {e}")
            
        return None
    
    def _extract_knowledge(self, content: str) -> Dict[str, List[str]]:
        """Extract categorized knowledge from content"""
        
        import re
        
        knowledge = {
            "patterns": [],
            "algorithms": [],
            "architectures": [],
            "techniques": [],
            "principles": []
        }
        
        # Simple pattern extraction (can be enhanced with NLP)
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for patterns
            if any(word in line.lower() for word in ['pattern', 'emerge', 'discover', 'reveal']):
                knowledge['patterns'].append(line[:100])
            
            # Look for algorithms
            if any(word in line.lower() for word in ['algorithm', 'process', 'method', 'approach']):
                knowledge['algorithms'].append(line[:100])
            
            # Look for architectures
            if any(word in line.lower() for word in ['architecture', 'system', 'structure', 'component']):
                knowledge['architectures'].append(line[:100])
            
            # Look for techniques
            if any(word in line.lower() for word in ['technique', 'strategy', 'implementation']):
                knowledge['techniques'].append(line[:100])
            
            # Look for principles
            if any(word in line.lower() for word in ['principle', 'rule', 'guideline', 'constraint']):
                knowledge['principles'].append(line[:100])
        
        # Remove duplicates and empty entries
        for category in knowledge:
            knowledge[category] = list(set(filter(None, knowledge[category])))
        
        return knowledge
    
    def _generate_artifacts(self, processed_knowledge: Dict):
        """Generate clean project artifacts from validated knowledge"""
        
        print("\n📝 Generating Project Artifacts...")
        
        # Aggregate all validated knowledge
        aggregated = {
            "patterns": [],
            "algorithms": [],
            "architectures": [],
            "techniques": [],
            "principles": []
        }
        
        for filename, result in processed_knowledge.items():
            extracted = result.get("extracted_knowledge", {})
            for key, values in extracted.items():
                if key in aggregated and isinstance(values, list):
                    aggregated[key].extend(values)
        
        # Generate SOLAR EMERGENCE planning documents
        self._generate_planning_docs(aggregated, processed_knowledge)
        
        # Generate extracted knowledge summary
        self._generate_knowledge_summary(aggregated)
        
        # Update project documentation
        self._update_project_docs(aggregated)
    
    def _generate_planning_docs(self, knowledge: Dict, processed_knowledge: Dict):
        """Generate SOLAR EMERGENCE planning documents"""
        
        constraints = ProjectConstraints()
        
        charter = f"""# SOLAR EMERGENCE - Enhanced Project Charter
# Generated from Constraint-Validated Knowledge Corpus

## Core Principles (IMMUTABLE)
{chr(10).join(f'- {p}' for p in constraints.core_principles)}

## Technical Constraints (NON-NEGOTIABLE)
- **Hardware**: {constraints.technical_requirements['hardware']}
- **APIs**: {constraints.technical_requirements['apis']}
- **Storage**: {constraints.technical_requirements['storage']}
- **ML Models**: {constraints.technical_requirements['ml_models']}
- **Cost**: {constraints.technical_requirements['cost']}

## Emergent Patterns Discovered
{chr(10).join(f'- {p}' for p in knowledge.get('patterns', [])[:15])}

## Discovery-Based Algorithms  
{chr(10).join(f'- {a}' for a in knowledge.get('algorithms', [])[:15])}

## Local Architecture Components
{chr(10).join(f'- {a}' for a in knowledge.get('architectures', [])[:15])}

## Applicable Techniques (Constraint-Compliant)
{chr(10).join(f'- {t}' for t in knowledge.get('techniques', [])[:15])}

---
## Processing Summary
- Files Processed: {len(processed_knowledge)}
- Constraint Violations Prevented: {self.stats['violations_found']}
- Local Translations Applied: {self.stats['translations_made']}
- Average Compliance Score: {(sum(self.stats['compliance_scores']) / len(self.stats['compliance_scores'])) if self.stats['compliance_scores'] else 0:.2f}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Constraint Enforcement: ACTIVE ✅
"""
        
        output_path = self.docs_path / "planning" / "ENHANCED_PROJECT_CHARTER.md"
        output_path.write_text(charter)
        print(f"  ✅ Generated: docs/planning/ENHANCED_PROJECT_CHARTER.md")
    
    def _generate_knowledge_summary(self, knowledge: Dict):
        """Generate summary of extracted knowledge"""
        
        summary = f"""# Extracted Knowledge Summary

## Knowledge Categories
"""
        
        for category, items in knowledge.items():
            if items:
                summary += f"\n### {category.title()} ({len(items)} items)\n"
                for item in items[:10]:  # Top 10 items per category
                    summary += f"- {item}\n"
                if len(items) > 10:
                    summary += f"... and {len(items) - 10} more\n"
        
        summary += f"""
---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Knowledge Items: {sum(len(v) for v in knowledge.values())}
"""
        
        output_path = self.docs_path / "extracted-knowledge" / "KNOWLEDGE_SUMMARY.md"
        output_path.write_text(summary)
        print(f"  ✅ Generated: docs/extracted-knowledge/KNOWLEDGE_SUMMARY.md")
    
    def _update_project_docs(self, knowledge: Dict):
        """Update existing project documentation with extracted knowledge"""
        
        # Create requirements update based on extracted knowledge
        requirements_update = f"""# Requirements Enhancement from Knowledge Corpus

## Emergent Intelligence Requirements
Based on constraint-validated knowledge extraction:

### Functional Requirements
{chr(10).join(f'- FR{i:03d}: {p}' for i, p in enumerate(knowledge.get('patterns', [])[:10], 1))}

### Discovery Requirements  
{chr(10).join(f'- DR{i:03d}: {a}' for i, a in enumerate(knowledge.get('algorithms', [])[:10], 1))}

### Architecture Requirements
{chr(10).join(f'- AR{i:03d}: {arch}' for i, arch in enumerate(knowledge.get('architectures', [])[:10], 1))}

---
All requirements maintain compliance with SOLAR EMERGENCE constraints:
- LOCAL_ONLY, ZERO_COST, DISCOVERY_FIRST, EMERGENT
"""
        
        output_path = self.docs_path / "planning" / "REQUIREMENTS_ENHANCEMENT.md"  
        output_path.write_text(requirements_update)
        print(f"  ✅ Generated: docs/planning/REQUIREMENTS_ENHANCEMENT.md")
    
    def _print_summary(self):
        """Print processing summary"""
        
        print("\n" + "=" * 50)
        print("📊 KNOWLEDGE HARVESTING SUMMARY")
        print("=" * 50)
        print(f"Files Processed: {self.stats['files_processed']}")
        print(f"Constraint Violations Found & Corrected: {self.stats['violations_found']}")  
        print(f"Local Translations Applied: {self.stats['translations_made']}")
        
        if self.stats['compliance_scores']:
            avg_compliance = sum(self.stats['compliance_scores']) / len(self.stats['compliance_scores'])
            print(f"Average Compliance Score: {avg_compliance:.2f}/1.00")
        
        print(f"\n✅ Knowledge corpus processed with SOLAR EMERGENCE constraints enforced!")
        print(f"📁 Enhanced artifacts saved to: docs/")
        print(f"🚫 Quarantined processing in: knowledge-corpus/")
        print(f"\n🎯 Your project remains TRUE to its core principles:")
        print("   LOCAL_ONLY • ZERO_COST • DISCOVERY_FIRST • EMERGENT")

# CLI Interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test with sample content
        print("🧪 Running Knowledge Harvester Test...")
        
        # Create test file
        test_dir = Path("knowledge-corpus/raw-inputs/examples")
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_content = """# Test Document
        
This system demonstrates emergent pattern discovery algorithms.
It uses local architecture for processing video data.
The technique reveals hidden insights through mathematical analysis.
Unfortunately, it currently uses OpenAI API for processing.
Cloud storage is required for scalability.
"""
        
        test_file = test_dir / "test_doc.md"
        test_file.write_text(test_content)
        print(f"📝 Created test file: {test_file}")
    
    # Run the pipeline
    pipeline = KnowledgeProcessingPipeline()
    pipeline.process_corpus()

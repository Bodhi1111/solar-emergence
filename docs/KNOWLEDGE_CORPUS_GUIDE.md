# Knowledge Corpus Feeding & Processing Guide

## Overview

The SOLAR EMERGENCE knowledge corpus uses a constraint-enforced pipeline to process raw knowledge into project-compliant artifacts. This ensures all knowledge aligns with LOCAL_ONLY, ZERO_COST, and EMERGENT principles.

## 📥 Feeding Knowledge to the Corpus

### Quick Commands

```bash
# Feed a single file
python3 scripts/feed_knowledge.py --file /path/to/document.pdf --category papers

# Feed from URL
python3 scripts/feed_knowledge.py --url https://example.com/paper.pdf --category papers

# Feed entire directory
python3 scripts/feed_knowledge.py --directory /path/to/docs --category documentation

# Feed GitHub repository
python3 scripts/feed_knowledge.py --github https://github.com/owner/repo

# Feed raw text
python3 scripts/feed_knowledge.py --text "Your knowledge content" --filename "knowledge.md"

# List current corpus contents
python3 scripts/feed_knowledge.py --list

# Feed and immediately process
python3 scripts/feed_knowledge.py --file document.pdf --process
```

## 📂 Knowledge Categories

### `documentation/`
- `.md` files (documentation)
- `.py`, `.js`, `.ts` files (source code)
- Configuration files
- API documentation

### `papers/`
- `.pdf` research papers
- `.tex` LaTeX files
- `.bib` bibliography files
- Academic content

### `examples/`
- Code examples
- Tutorials
- Sample implementations
- Reference materials

### `repositories/`
- Complete GitHub repositories
- Open source projects
- Code libraries

## 🔄 Processing the Knowledge Corpus

### Step 1: Feed Knowledge (Choose Method)

**Method A: Direct File Addition**
```bash
# Copy files directly
cp your_research_paper.pdf knowledge-corpus/raw-inputs/papers/
cp your_code_examples.py knowledge-corpus/raw-inputs/documentation/
```

**Method B: Using the Feed Script**
```bash
# Add AI/ML research paper
python3 scripts/feed_knowledge.py --url "https://arxiv.org/pdf/2023.12345.pdf" --category papers

# Add local documentation
python3 scripts/feed_knowledge.py --file "~/Documents/ml_guide.md" --category documentation

# Clone relevant repository
python3 scripts/feed_knowledge.py --github "https://github.com/openai/whisper"
```

### Step 2: Process Through Constraint Pipeline

```bash
# Run the knowledge harvester (processes raw content)
python3 agents/knowledge_harvester.py

# Bridge processed knowledge to BMAD agents
python3 agents/bmad_knowledge_bridge.py

# Or run both together
npm run sync-knowledge
```

### Step 3: Monitor Processing

```bash
# Check processing results
ls knowledge-corpus/processed/validated/

# View knowledge summary
cat docs/extracted-knowledge/KNOWLEDGE_SUMMARY.md

# Check BMAD integration
cat .bmad-core/context/knowledge_context.json
```

## 🔍 What Happens During Processing

### 1. Constraint Enforcement
- **LOCAL_ONLY Check**: Removes references to cloud APIs
- **ZERO_COST Check**: Flags paid services, suggests free alternatives
- **EMERGENT Check**: Ensures focus on discovery vs. predefined patterns

### 2. Knowledge Extraction
- Identifies patterns, algorithms, architectures
- Extracts techniques and principles
- Preserves constraint-compliant information

### 3. Compliance Scoring
- Only knowledge with >0.3 compliance score passes through
- Violations are logged and alternatives suggested
- Clean artifacts generated in `docs/`

### 4. BMAD Integration
- Processed knowledge feeds into agent working memory
- 106+ knowledge items available to agents
- Pattern discovery enhanced by corpus knowledge

## 📊 Monitoring the Pipeline

### Check Pipeline Status
```bash
# View processing statistics
tail logs/knowledge_processing.log

# Check validation results
ls knowledge-corpus/processed/validated/

# Monitor BMAD integration
npm run knowledge-stats
```

### View Extracted Knowledge
```bash
# Knowledge summary
cat docs/extracted-knowledge/KNOWLEDGE_SUMMARY.md

# BMAD agent context
cat .bmad-core/context/knowledge_context.json

# Discovery specifications
ls specs/discovery/
```

## 🎯 Best Practices

### What to Feed
✅ **Good Sources**:
- Open source ML/AI repositories
- ArXiv papers on pattern discovery
- Local processing documentation
- Constraint-compliant tools and libraries
- Emergent intelligence research

❌ **Avoid**:
- Paid API documentation
- Cloud-only solutions
- Proprietary service manuals
- Non-emergent, rule-based approaches

### Processing Tips

1. **Feed incrementally** - Process new knowledge regularly
2. **Review violations** - Check constraint enforcement logs
3. **Monitor compliance** - Ensure knowledge aligns with principles
4. **Test integration** - Verify BMAD agents can access new knowledge

## 🚀 Example Workflows

### Workflow 1: Research Paper Integration
```bash
# 1. Download paper
python3 scripts/feed_knowledge.py --url "https://arxiv.org/pdf/2024.12345.pdf" --category papers

# 2. Process immediately
python3 agents/knowledge_harvester.py

# 3. Integrate with BMAD
python3 agents/bmad_knowledge_bridge.py

# 4. Check results
cat docs/extracted-knowledge/KNOWLEDGE_SUMMARY.md
```

### Workflow 2: Repository Integration
```bash
# 1. Clone relevant repository
python3 scripts/feed_knowledge.py --github "https://github.com/microsoft/DeepSpeed"

# 2. Process and filter
npm run sync-knowledge

# 3. Review compliance
grep -i "violation" logs/knowledge_processing.log

# 4. Check agent integration
npm run knowledge-stats
```

### Workflow 3: Bulk Documentation
```bash
# 1. Add documentation directory
python3 scripts/feed_knowledge.py --directory "~/Downloads/ml_docs/" --category documentation

# 2. List what was added
python3 scripts/feed_knowledge.py --list

# 3. Process everything
npm run sync-knowledge

# 4. Monitor results
tail -f logs/knowledge_processing.log
```

## 🔧 Troubleshooting

### Common Issues

**"No knowledge extracted"**
- Check if files are in supported formats (.md, .py, .pdf, .html)
- Verify content isn't filtered out by CONTENT_FILTER.md rules

**"Low compliance score"**
- Review constraint violations in processing logs
- Content may reference too many cloud/paid services
- Consider manual editing for local alternatives

**"BMAD integration failed"**
- Ensure bridge script completed successfully
- Check `.bmad-core/context/` directory permissions
- Verify JSON format validity

### Debug Commands
```bash
# Check raw inputs
ls -la knowledge-corpus/raw-inputs/

# Check processing logs
tail -n 50 logs/knowledge_processing.log

# Check constraint violations
grep "VIOLATION" logs/constraint_enforcement.log

# Test BMAD integration
node -e "const {KnowledgeLoader} = require('./.bmad-core/utils/knowledge-loader.js'); console.log(new KnowledgeLoader().getKnowledgeStats());"
```

## 📈 Monitoring Success

### Key Metrics
- **Files processed**: Total knowledge items processed
- **Compliance rate**: Percentage passing constraint checks
- **Knowledge extraction**: Number of patterns/algorithms/techniques found
- **BMAD integration**: Agent access to processed knowledge

### Success Indicators
- ✅ Knowledge summary updates in `docs/extracted-knowledge/`
- ✅ BMAD agents have access to new patterns
- ✅ Compliance scores >0.3 for processed content
- ✅ No constraint violations in processing logs

The knowledge corpus is now ready to continuously learn and enhance your SOLAR EMERGENCE project with constraint-compliant intelligence!
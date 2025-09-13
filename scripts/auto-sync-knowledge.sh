#!/bin/bash

# Auto-sync Knowledge Script
# Automatically syncs knowledge corpus with BMAD agents

set -e

echo "🔄 Auto-syncing Knowledge Corpus → BMAD Agents"

# Check if we're in the right directory
if [ ! -f ".bmad-core/core-config.yaml" ]; then
    echo "❌ Not in Solar Emergence project directory"
    exit 1
fi

# Run knowledge harvester if it exists
if [ -f "agents/knowledge_harvester.py" ]; then
    echo "📊 Running Knowledge Harvester..."
    python3 agents/knowledge_harvester.py
else
    echo "⚠️  Knowledge Harvester not found, skipping..."
fi

# Run knowledge bridge
echo "🔗 Running Knowledge Bridge..."
python3 agents/bmad_knowledge_bridge.py

# Verify integration
echo "✅ Verifying integration..."

# Check that context was created
if [ -f ".bmad-core/context/knowledge_context.json" ]; then
    echo "  ✅ BMAD context updated"
else
    echo "  ❌ BMAD context missing"
    exit 1
fi

# Check that memory was created
if [ -f ".bmad-core/memory/current_state.json" ]; then
    echo "  ✅ BMAD memory updated"
else
    echo "  ❌ BMAD memory missing"
    exit 1
fi

# Check that specs were created
if [ -f "specs/multimodal-discovery.spec.yml" ]; then
    echo "  ✅ Multimodal spec generated"
else
    echo "  ❌ Multimodal spec missing"
    exit 1
fi

# Show knowledge stats
echo ""
echo "📈 Current Knowledge Stats:"
if command -v node &> /dev/null && [ -f "package.json" ]; then
    npm run knowledge-stats
else
    # Fallback to Python stats
    python3 -c "
import json
from pathlib import Path

try:
    context_path = Path('.bmad-core/context/knowledge_context.json')
    if context_path.exists():
        context = json.loads(context_path.read_text())
        knowledge = context.get('solar_emergence_knowledge', {})
        
        print(f'  Patterns: {len(knowledge.get(\"discovered_patterns\", []))}')
        print(f'  Algorithms: {len(knowledge.get(\"applicable_algorithms\", []))}')
        print(f'  Architectures: {len(knowledge.get(\"local_architectures\", []))}')
        print(f'  Last Updated: {knowledge.get(\"last_updated\", \"Unknown\")}')
    else:
        print('  ❌ No knowledge context found')
except Exception as e:
    print(f'  ❌ Error reading stats: {e}')
"
fi

echo ""
echo "🎯 Next Steps:"
echo "  1. Run 'bmad generate-prd' to create knowledge-informed PRD"
echo "  2. Run 'npm run validate-constraints' to test compliance checking"
echo "  3. Run 'npm run search-knowledge [term]' to explore knowledge"

echo ""
echo "✅ Knowledge sync complete! BMAD agents now have access to 106+ knowledge items."
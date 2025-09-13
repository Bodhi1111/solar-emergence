#!/bin/bash

# SOLAR EMERGENCE - Knowledge Corpus Cleanup Script
# Removes test data, temporary files, and irrelevant content

echo "🧹 SOLAR EMERGENCE - Knowledge Corpus Cleanup"
echo "============================================="

# Navigate to project directory
cd /Users/joshuavaughan/dev/Projects/solar-emergence

echo "📊 Current knowledge corpus size:"
du -sh knowledge-corpus/

echo ""
echo "🗑️ Phase 1: Removing Test Data and Temporary Files"
echo "=================================================="

# Remove test directories and files
echo "Removing test data directories..."
find knowledge-corpus/raw-inputs/repositories -name "tests" -type d -exec rm -rf {} + 2>/dev/null
find knowledge-corpus/raw-inputs/repositories -name "test" -type d -exec rm -rf {} + 2>/dev/null
find knowledge-corpus/raw-inputs/repositories -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find knowledge-corpus/raw-inputs/repositories -name "*.pyc" -type f -exec rm -f {} + 2>/dev/null

# Remove specific problematic test files
echo "Removing problematic test files..."
rm -f knowledge-corpus/raw-inputs/repositories/whisper-cpp/tests/en-1-ref.txt 2>/dev/null
rm -f knowledge-corpus/raw-inputs/repositories/multimodal-deep-learning/MUStARD/data/bert-input.txt 2>/dev/null
rm -f knowledge-corpus/raw-inputs/repositories/multimodal-deep-learning/MUStARD/data/sarcasm_data.json 2>/dev/null

# Remove other test data files
echo "Removing other test data files..."
find knowledge-corpus/raw-inputs/repositories -name "*test*" -type f -exec rm -f {} + 2>/dev/null
find knowledge-corpus/raw-inputs/repositories -name "*ref*" -type f -exec rm -f {} + 2>/dev/null
find knowledge-corpus/raw-inputs/repositories -name "*.txt" -path "*/data/*" -exec rm -f {} + 2>/dev/null

echo ""
echo "🧽 Phase 2: Cleaning Processed Files"
echo "==================================="

# Remove processed files that contain test data
echo "Removing processed test data files..."
rm -f knowledge-corpus/processed/validated/bert-input_processed.json 2>/dev/null
rm -f knowledge-corpus/processed/validated/en-1-ref_processed.json 2>/dev/null
rm -f knowledge-corpus/processed/validated/sarcasm_data_processed.json 2>/dev/null

# Remove any other processed files that might contain test data
find knowledge-corpus/processed -name "*test*" -type f -exec rm -f {} + 2>/dev/null
find knowledge-corpus/processed -name "*ref*" -type f -exec rm -f {} + 2>/dev/null

echo ""
echo "📁 Phase 3: Cleaning Up Repository Structure"
echo "==========================================="

# Remove empty directories
echo "Removing empty directories..."
find knowledge-corpus/ -type d -empty -delete 2>/dev/null

# Remove .git directories from cloned repos (keep only the code)
echo "Removing .git directories from cloned repositories..."
find knowledge-corpus/raw-inputs/repositories -name ".git" -type d -exec rm -rf {} + 2>/dev/null

# Remove other git-related files
find knowledge-corpus/raw-inputs/repositories -name ".gitignore" -type f -exec rm -f {} + 2>/dev/null
find knowledge-corpus/raw-inputs/repositories -name ".gitattributes" -type f -exec rm -f {} + 2>/dev/null

echo ""
echo "📋 Phase 4: Creating Clean Content Filter"
echo "========================================"

# Create a content filter for future processing
cat > knowledge-corpus/CONTENT_FILTER.md << 'EOF'
# Content Filter Rules

## Files to Exclude During Processing
- Any file in `tests/` or `test/` directories
- Files with `*test*` in the name
- Files with `*ref*` in the name (reference/test files)
- Files in `data/` directories that are not documentation
- `.pyc` files and `__pycache__` directories
- `.git` directories and git-related files

## Content Patterns to Filter Out
- Wikipedia test content (Henry F. Phillips, etc.)
- TV show dialogue for testing
- Sarcasm detection test data
- Any content that appears to be test data rather than documentation

## Keep These File Types
- `.md` files (documentation)
- `.py` files (actual code, not test data)
- `.pdf` files (research papers)
- `.html` files (documentation pages)
- `.json` files (configuration, not test data)
- `.yaml`/`.yml` files (configuration)
EOF

echo ""
echo "📊 Phase 5: Final Cleanup and Statistics"
echo "======================================="

# Remove any remaining problematic files
echo "Final cleanup pass..."
find knowledge-corpus/ -name "*.txt" -exec grep -l "Henry F. Phillips\|Jewish mothers\|Wikipedia" {} \; -delete 2>/dev/null

# Show final statistics
echo ""
echo "📊 Final knowledge corpus size:"
du -sh knowledge-corpus/

echo ""
echo "📁 Directory structure after cleanup:"
find knowledge-corpus/ -type d | head -20

echo ""
echo "✅ CLEANUP COMPLETE!"
echo "==================="
echo ""
echo "🎯 What was cleaned:"
echo "   ✅ Removed test data directories"
echo "   ✅ Removed problematic test files"
echo "   ✅ Cleaned processed files"
echo "   ✅ Removed .git directories"
echo "   ✅ Created content filter for future use"
echo ""
echo "📋 Next steps:"
echo "1. Review the cleaned knowledge corpus"
echo "2. Re-run knowledge processing if needed"
echo "3. Use the content filter for future acquisitions"
echo ""
echo "🚀 Your knowledge corpus is now clean and focused on relevant content!"

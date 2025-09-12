# Knowledge Corpus - QUARANTINE ZONE

This directory is for dumping raw knowledge that will be processed.

## ⚠️ IMPORTANT
- This content is NOT part of the codebase
- Everything here is filtered through constraints
- Only validated, compliant knowledge makes it to /docs

## Constraints Enforced
1. LOCAL_ONLY - No cloud services
2. ZERO_COST - No paid APIs
3. DISCOVERY_FIRST - No predetermined patterns
4. EMERGENT - Patterns must emerge from data

## Usage
1. Dump any articles/docs into `raw-inputs/`
2. Run: `python agents/knowledge_harvester.py`
3. Clean artifacts appear in `/docs/`

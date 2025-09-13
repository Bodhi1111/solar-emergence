# Implementation Plan: SOLAR EMERGENCE - Multimodal Discovery Engine

**Branch**: `001-multimodal-discovery-engine` | **Date**: 2025-09-12 | **Spec**: [/specs/solar-emergence-core-feature.spec.md]
**Input**: Feature specification from `/specs/solar-emergence-core-feature.spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → ✅ Spec loaded: Multimodal Sales Intelligence Discovery
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Project Type: Single (local processing engine)
   → Structure Decision: Option 1 (single project)
3. Evaluate Constitution Check section below
   → ✅ LOCAL_ONLY compliance verified
   → ✅ ZERO_COST compliance verified
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → Research local ML frameworks, multimodal processing
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, CLAUDE.md
6. Re-evaluate Constitution Check section
   → Verify all implementations remain constraint-compliant
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach
8. STOP - Ready for /tasks command
```

## Summary
Building a multimodal discovery engine for estate planning sales meetings that processes video recordings locally to discover emergent behavioral patterns correlating with sales outcomes, using 100% local processing on Mac M2 Max hardware with zero external dependencies.

## Technical Context
**Language/Version**: Python 3.11 + TypeScript (BMAD agents)  
**Primary Dependencies**: MLX Framework, OpenCV, MediaPipe, FFmpeg, Whisper.cpp  
**Storage**: PostgreSQL + pgvector, Neo4j (graph), Qdrant (vectors)  
**Testing**: pytest (Python), jest (TypeScript)  
**Target Platform**: Mac M2 Max (32GB RAM)  
**Project Type**: single - local processing engine  
**Performance Goals**: Process 1hr video in <10min, real-time feature extraction  
**Constraints**: LOCAL_ONLY processing, ZERO_COST (no APIs), 32GB RAM limit  
**Scale/Scope**: 1,500+ video corpus, 468 facial landmarks per frame

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 1 (multimodal processing engine)
- Using framework directly? ✅ (MLX, OpenCV without wrappers)
- Single data model? ✅ (unified signature representation)
- Avoiding patterns? ✅ (direct processing, no abstraction layers)

**Architecture**:
- EVERY feature as library? ✅ (modular processing libraries)
- Libraries listed:
  - `extraction_lib`: Multimodal feature extraction
  - `synthesis_lib`: Vertical signature synthesis
  - `discovery_lib`: Pattern discovery and correlation
  - `learning_lib`: Sequential intelligence accumulation
- CLI per library: 
  - `solar-extract --video [path] --format json`
  - `solar-synthesize --features [path] --output signatures`
  - `solar-discover --signatures [path] --correlations`
  - `solar-learn --corpus [path] --update-model`
- Library docs: llms.txt format planned? ✅

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? ✅
- Git commits show tests before implementation? ✅
- Order: Contract→Integration→E2E→Unit strictly followed? ✅
- Real dependencies used? ✅ (actual video files, real DBs)
- Integration tests for: new libraries, contract changes, shared schemas? ✅
- FORBIDDEN: Implementation before test ✅ (understood)

**Observability**:
- Structured logging included? ✅ (JSON logs)
- Frontend logs → backend? N/A (local processing only)
- Error context sufficient? ✅ (frame numbers, processing stage)

**Versioning**:
- Version number assigned? ✅ (1.0.0)
- BUILD increments on every change? ✅
- Breaking changes handled? ✅ (signature format versioning)

## Project Structure

### Documentation (this feature)
```
specs/001-multimodal-discovery/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (SELECTED - local processing engine)
src/
├── models/
│   ├── meeting.py       # Meeting recording metadata
│   ├── signature.py     # Multimodal signature representation
│   ├── pattern.py       # Discovered behavioral patterns
│   └── correlation.py   # Statistical correlations
├── services/
│   ├── extraction/      # Feature extraction services
│   ├── synthesis/       # Signature synthesis services
│   ├── discovery/       # Pattern discovery services
│   └── learning/        # Sequential learning services
├── cli/
│   ├── solar_extract.py
│   ├── solar_synthesize.py
│   ├── solar_discover.py
│   └── solar_learn.py
└── lib/
    ├── mlx_utils.py     # MLX framework utilities
    ├── cv_processing.py # OpenCV/MediaPipe integration
    └── db_connectors.py # PostgreSQL/Neo4j/Qdrant

tests/
├── contract/
│   ├── test_extraction_contract.py
│   ├── test_synthesis_contract.py
│   └── test_discovery_contract.py
├── integration/
│   ├── test_video_pipeline.py
│   ├── test_signature_generation.py
│   └── test_pattern_discovery.py
└── unit/
    ├── test_facial_landmarks.py
    ├── test_audio_prosody.py
    └── test_correlation_math.py
```

**Structure Decision**: Option 1 (Single project) - appropriate for local processing engine

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context**:
   - MLX Framework best practices for multimodal processing
   - Whisper.cpp integration with Python
   - MediaPipe optimization for 468 facial landmarks
   - pgvector performance tuning for signature storage
   - Neo4j schema design for behavioral patterns

2. **Generate and dispatch research agents**:
   ```
   Task: "Research MLX Framework for local multimodal processing"
   Task: "Find best practices for Whisper.cpp Python integration"
   Task: "Research MediaPipe optimization for real-time landmark extraction"
   Task: "Investigate pgvector indexing strategies for 1500+ videos"
   Task: "Research Neo4j schema evolution for emergent patterns"
   ```

3. **Consolidate findings** in `research.md`:
   - Decision: MLX for all AI processing (local M2 optimization)
   - Rationale: Native Apple Silicon support, zero API dependency
   - Alternatives considered: PyTorch (less M2 optimized), TensorFlow (heavier)

**Output**: research.md with all technical decisions documented

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Meeting: recording_path, duration, participants, outcome
   - Signature: multimodal_features, timestamp, meeting_id
   - Pattern: correlation_strength, feature_combination, occurrence_count
   - Intelligence: accumulated_patterns, prediction_accuracy, corpus_size

2. **Generate API contracts** from functional requirements:
   - POST /extract: Video → Features contract
   - POST /synthesize: Features → Signature contract
   - POST /discover: Signatures → Patterns contract
   - POST /learn: Patterns → Intelligence contract
   - Output OpenAPI schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - test_extraction_contract.py: Video input validation
   - test_synthesis_contract.py: Signature format validation
   - test_discovery_contract.py: Pattern structure validation
   - Tests must fail initially (no implementation)

4. **Extract test scenarios** from user stories:
   - Process first video end-to-end
   - Generate signature from multimodal features
   - Discover pattern across 10 videos
   - Predict outcome from learned patterns

5. **Update CLAUDE.md incrementally**:
   - Add MLX, Whisper.cpp, MediaPipe to tech context
   - Document local-only constraint enforcement
   - Include multimodal processing patterns

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, CLAUDE.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs:
  - Each contract → contract test task [P]
  - Each entity → model creation task [P]
  - Each processing stage → implementation task
  - Integration tests for full pipeline

**Ordering Strategy**:
- TDD order: Tests before implementation
- Processing order: Extract → Synthesize → Discover → Learn
- Parallel tasks for independent components [P]

**Estimated Output**: 30-35 numbered tasks covering:
- Model implementations (4 tasks)
- Contract tests (4 tasks)
- Feature extraction (6 tasks)
- Signature synthesis (4 tasks)
- Pattern discovery (5 tasks)
- Sequential learning (4 tasks)
- Integration tests (3-5 tasks)

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*No violations - fully compliant with all constitutional principles*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - approach described)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (none)

**Constraint Compliance**:
- [x] LOCAL_ONLY: All processing on Mac M2 Max
- [x] ZERO_COST: No paid APIs or services
- [x] EMERGENT: Pattern discovery not predefined
- [x] DISCOVERY_FIRST: Mathematics drives insights
- [x] SEQUENTIAL: Each video builds intelligence
- [x] MULTIMODAL: All signals processed equally

---
*Based on Constitution v2.1.1 and SOLAR EMERGENCE principles*
# Spec-Kit Integration Guide for BMAD Agents

## Overview
This guide explains how BMAD agents can use the spec-kit functionality for Spec-Driven Development (SDD) in the Solar Emergence project.

## Available Spec-Kit Commands

### 1. **@BMad specify** - Create Feature Specifications
**Usage**: `@BMad specify "feature description"`

**What it does**:
- Creates a new feature branch
- Initializes specification file using `templates/spec-template.md`
- Sets up directory structure for the feature
- Reports completion with branch name and spec file path

**Example**:
```
@BMad specify "implement multimodal pattern discovery pipeline"
```

### 2. **@BMad plan** - Create Implementation Plans
**Usage**: `@BMad plan "implementation details"`

**What it does**:
- Reads feature specification from the current branch
- Loads constitution requirements from `memory/constitution.md`
- Executes implementation plan template (`templates/plan-template.md`)
- Generates artifacts in phases:
  - Phase 0: `research.md`
  - Phase 1: `data-model.md`, `contracts/`, `quickstart.md`
  - Phase 2: `tasks.md`

**Example**:
```
@BMad plan "implement local-only Whisper.cpp integration with constraint validation"
```

### 3. **@BMad tasks** - Generate Task Breakdown
**Usage**: `@BMad tasks "task details"`

**What it does**:
- Creates detailed task breakdown from implementation plan
- Uses `templates/tasks-template.md`
- Generates actionable tasks with dependencies
- Incorporates constraint compliance requirements

## Spec-Kit Integration Points

### Constitution Compliance
All spec-kit operations automatically reference:
- **Constitution**: `memory/constitution.md`
- **Constraints**: LOCAL_ONLY, ZERO_COST, EMERGENT_FOCUS
- **Validation**: Automatic constraint checking in all generated artifacts

### Knowledge Integration
Spec-kit operations have access to:
- **106+ Knowledge Items** from validated corpus
- **Pattern Discovery Techniques** (GNN, TDA, UMAP)
- **Local Processing Algorithms** (Whisper.cpp, etc.)
- **Architecture Patterns** from Solar Emergence system

### Template System
All specifications use standardized templates:
- `templates/spec-template.md` - Feature specifications
- `templates/plan-template.md` - Implementation plans
- `templates/tasks-template.md` - Task breakdowns
- `templates/agent-file-template.md` - Agent documentation

## Agent Workflow Integration

### Phase 1: Specification Creation
1. Agent receives feature request
2. Uses `@BMad specify` to create specification
3. Incorporates knowledge from corpus
4. Ensures constraint compliance

### Phase 2: Implementation Planning
1. Agent reads generated specification
2. Uses `@BMad plan` to create implementation plan
3. Leverages knowledge corpus for technical decisions
4. Validates against constitution requirements

### Phase 3: Task Generation
1. Agent processes implementation plan
2. Uses `@BMad tasks` to create actionable tasks
3. Incorporates constraint validation
4. Generates dependency mapping

## Available Scripts

### Core Scripts
- `scripts/create-new-feature.sh` - Feature creation
- `scripts/setup-plan.sh` - Plan setup
- `scripts/check-task-prerequisites.sh` - Prerequisites checking
- `scripts/get-feature-paths.sh` - Path resolution

### Utility Scripts
- `scripts/common.sh` - Common functions
- `scripts/update-agent-context.sh` - Context updates

## Knowledge Bridge Integration

### Automatic Knowledge Access
The spec-kit automatically integrates with:
- **Knowledge Context**: `.bmad-core/context/knowledge_context.json`
- **Knowledge Loader**: `.bmad-core/utils/knowledge-loader.js`
- **Memory System**: `.bmad-core/memory/`

### Constraint Validation
All generated artifacts are automatically validated against:
- **LOCAL_ONLY**: No external API dependencies
- **ZERO_COST**: No paid service requirements
- **EMERGENT_FOCUS**: Aligned with emergence principles

## Usage Examples

### Example 1: Creating a New Feature
```bash
# Agent workflow
@BMad specify "implement real-time audio pattern recognition"

# Results in:
# - New branch: feature/audio-pattern-recognition
# - Spec file: specs/audio-pattern-recognition/spec.md
# - Ready for planning phase
```

### Example 2: Planning Implementation
```bash
# Agent workflow
@BMad plan "use Whisper.cpp for local audio processing with GNN pattern discovery"

# Results in:
# - research.md with audio processing research
# - data-model.md with data structures
# - contracts/ with API definitions
# - quickstart.md with setup instructions
# - tasks.md with implementation tasks
```

### Example 3: Task Generation
```bash
# Agent workflow
@BMad tasks "implement constraint-compliant audio processing pipeline"

# Results in:
# - Detailed task breakdown
# - Dependency mapping
# - Constraint validation
# - Implementation timeline
```

## Best Practices

### For Agents
1. **Always use spec-kit commands** for feature development
2. **Reference constitution** in all specifications
3. **Leverage knowledge corpus** for technical decisions
4. **Validate constraints** at each phase
5. **Use absolute paths** for all file operations

### For Specifications
1. **Follow template structure** exactly
2. **Include constraint compliance** sections
3. **Reference knowledge corpus** items
4. **Document local-only requirements**
5. **Specify zero-cost implementations**

## Troubleshooting

### Common Issues
- **Path issues**: Always use absolute paths from repo root
- **Template loading**: Ensure templates exist in `templates/`
- **Script execution**: Check script permissions and paths
- **Constraint violations**: Review constitution requirements

### Debug Commands
```bash
# Check spec-kit status
npm run knowledge-stats

# Validate constraints
npm run validate-constraints

# Sync knowledge
npm run sync-knowledge

# View project status
npm run project-status
```

## Integration Status
- ✅ **Spec-kit commands** configured in BMad
- ✅ **Templates** available and loaded
- ✅ **Scripts** executable and functional
- ✅ **Knowledge integration** active
- ✅ **Constraint validation** enabled
- ✅ **Constitution compliance** enforced

Your agents now have full access to the spec-kit functionality for Spec-Driven Development! 🚀

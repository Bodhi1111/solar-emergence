# Spec-Kit & BMad Framework Integration Guide

## Overview

This project integrates GitHub's Spec-Kit methodology with the BMad framework core to provide a comprehensive spec-driven development environment:

- **Spec-Kit**: Provides structured `/specify`, `/plan`, `/tasks` commands and templates
- **BMad Framework**: Provides core agents, workflows, and development processes via `.bmad-core/`

## Available Commands

### Spec-Kit Commands (via Claude Code)
- `/specify` - Create feature specifications using spec-driven methodology
- `/plan` - Generate technical implementation plans 
- `/tasks` - Break down plans into executable tasks

### BMad Commands (existing)
- `/BMad` prefixed commands for various agents and workflows
- Full agent ecosystem for development tasks

## Workflow Integration

### 1. Feature Specification Phase
**Use**: `/specify "feature description"`
**Process**: 
1. Creates feature branch via `scripts/create-new-feature.sh`
2. Generates specification in `specs/###-feature-name/spec.md`
3. Uses `templates/spec-template.md` structure
4. Focuses on WHAT and WHY, not HOW

**BMad Integration**: Spec-kit specs align with BMad's requirements gathering approach

### 2. Planning Phase  
**Use**: `/plan`
**Process**:
1. Loads feature spec from previous phase
2. Creates technical implementation plan
3. Generates `research.md`, `data-model.md`, `quickstart.md`
4. Creates contracts and failing tests
5. Updates agent context files (CLAUDE.md, etc.)

**BMad Integration**: Plans feed into BMad's architecture and development workflows

### 3. Task Generation Phase
**Use**: `/tasks` 
**Process**:
1. Loads plan from previous phase
2. Generates ordered, executable tasks
3. Creates `tasks.md` with TDD-ordered implementation steps

**BMad Integration**: Tasks can be executed using BMad agents and workflows

## Template Relationships

### Spec-Kit Templates (now in `/templates/`)
- `spec-template.md` - Feature specification template
- `plan-template.md` - Implementation planning template  
- `tasks-template.md` - Task breakdown template

### BMad Templates (in `.bmad-core/templates/`)
- Various BMad-specific templates and configurations
- Agent definitions and workflows

**Note**: Root-level spec-kit templates are the primary templates for feature development.

## Directory Structure

```
solar-emergence/
├── .bmad-core/                    # BMad framework core
│   ├── agents/                    # BMad agent definitions
│   ├── tasks/                     # BMad task templates
│   ├── templates/                 # BMad templates
│   └── workflows/                 # BMad workflows
├── .claude/commands/              # All slash commands
│   ├── specify.md                 # Spec-kit /specify command
│   ├── plan.md                    # Spec-kit /plan command
│   ├── tasks.md                   # Spec-kit /tasks command
│   └── BMad/                      # BMad agent commands
├── specs/                         # Generated feature specs
│   └── ###-feature-name/          # Per-feature directories
│       ├── spec.md                # Feature specification
│       ├── plan.md                # Implementation plan
│       ├── research.md            # Technical research
│       ├── data-model.md          # Data models
│       ├── quickstart.md          # Usage examples
│       ├── contracts/             # API contracts
│       └── tasks.md               # Executable tasks
├── scripts/                       # Spec-kit utilities
│   └── create-new-feature.sh      # Feature branch creation
├── templates/                     # Spec-kit templates
└── memory/                        # Spec-kit memory/constitution
```

## BMad Agent Enhancement

Your BMad agents can now leverage spec-kit in these ways:

### 1. Specification Review
BMad agents can review spec-kit generated specifications for completeness and quality using BMad's quality gates.

### 2. Plan Validation  
Architectural agents can validate spec-kit plans against BMad's constitution and coding standards.

### 3. Task Execution
Development agents can execute spec-kit generated tasks using BMad's TDD and quality processes.

### 4. Framework Integration
BMad agents can integrate spec-kit outputs with BMad core processes and standards.

## Usage Recommendations

### For New Features
1. Start with `/specify` to create specification
2. Use `/plan` to generate implementation plan  
3. Use `/tasks` to create executable task list
4. Execute tasks using BMad agents and workflows

### For BMad Agents
- Reference spec-kit generated docs when working on features
- Use spec-kit structure for consistent documentation
- Integrate spec-kit outputs with BMad core processes
- Leverage BMad agent ecosystem for complex orchestration

### For Hybrid Workflows
- Use spec-kit for structured feature development
- Use BMad for complex agent orchestration
- Combine both for comprehensive development coverage

## Key Benefits

1. **Structured Process**: Spec-kit provides clear specification-to-implementation pipeline
2. **Agent Integration**: BMad agents can consume and enhance spec-kit outputs
3. **Consistency**: Both frameworks emphasize testing, documentation, and quality
4. **Flexibility**: Choose appropriate tool for each development phase
5. **Scalability**: Spec-kit handles feature lifecycle, BMad handles complex orchestration

## Next Steps

1. Try the integration with a sample feature using `/specify`
2. Configure BMad agents to reference spec-kit generated documentation
3. Create custom workflows that bridge both frameworks
4. Establish quality gates that leverage both systems
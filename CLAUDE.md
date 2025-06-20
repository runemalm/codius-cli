# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
- `pipenv install --dev` - Install all dependencies including dev packages
- `pipenv shell` - Activate the virtual environment
- `pipenv run python src/main.py` - Run the CLI application

### Testing
- `pipenv run pytest` - Run all tests
- `pipenv run pytest src/tests/unit/` - Run unit tests
- `pipenv run pytest -v` - Run tests with verbose output

### Dependencies
- `pipenv install <package>` - Add new production dependency
- `pipenv install <package> --dev` - Add new development dependency
- `pipenv graph` - Show dependency tree
- `pipenv check` - Check for security vulnerabilities

## Architecture Overview

This is a **Domain-Driven Design (DDD) CLI assistant** built with **LangGraph** that helps users model and generate C# code using the OpenDDD.NET framework. The codebase follows clean architecture principles with distinct layers.

### Core Architecture Patterns

**LangGraph Workflow**: The main processing flow is implemented as a directed graph with conditional routing:
- `DistillIntent` → `PlanChanges` → `GenerateCode` → `Preview` → `ApplyChanges`/`Abort`
- Each node represents a discrete processing step with state transitions
- Routers handle conditional branching based on intent clarity and user approval

**Session-based State Management**: 
- Sessions maintain conversation history and domain context across interactions
- State includes intent, domain summary, generated files, and user approval status
- History can be compacted while preserving domain context in the session state

**Code Scanner for C# Analysis**:
- Scans existing C# codebases to identify DDD building blocks (AggregateRoot, Entity, ValueObject, etc.)
- Recognizes OpenDDD.NET patterns across Domain, Application, and Infrastructure layers
- Used to understand existing domain models before making changes

### Key Components

**Domain Layer** (`src/domain/`):
- `Session`: Core entity managing conversation state and history
- `State`: Holds current modeling context (intent, domain summary, plans)
- `History`: Message history with compaction capabilities
- Services for session management and configuration

**Graph Layer** (`src/graph/`):
- `GraphState`: TypedDict defining state schema passed between nodes
- Nodes implement individual processing steps (intent distillation, planning, code generation, etc.)
- Routers handle conditional logic for workflow branching

**Infrastructure Layer** (`src/infrastructure/`):
- LLM service integration (OpenAI)
- Code scanner for analyzing existing C# codebases
- Repository pattern for session persistence
- Logging service configuration

**UI Layer** (`src/ui/`):
- Rich console-based interface with panels and syntax highlighting
- Slash commands for session management (`/clear`, `/compact`, `/new`, etc.)
- Prompt toolkit integration for command completion

### Domain-Specific Context

The assistant specializes in **tactical DDD patterns** for C# using OpenDDD.NET:
- Aggregate roots, entities, value objects, domain events
- Repository interfaces, domain services, ports/adapters
- Application commands, actions, event listeners
- Infrastructure services and adapters

When working with code generation, the system analyzes existing patterns in the target codebase and generates code following the established conventions and OpenDDD.NET framework patterns.
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![Author: David Runemalm](https://img.shields.io/badge/Author-David%20Runemalm-blue)](https://www.davidrunemalm.com)
[![Master workflow](https://github.com/runemalm/openddd-cli/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/openddd-cli/actions/workflows/master.yml)
[![PyPI version](https://badge.fury.io/py/openddd-cli.svg)](https://pypi.org/project/openddd-cli/)
![Downloads](https://pepy.tech/badge/openddd-cli)
![No dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

# OpenDDD.NET Coding Assistant

> ✨ AI-powered CLI for evolving OpenDDD.NET projects — like Codex or Claude, but made for DDD in ASP.NET Core.

The **OpenDDD.NET Coding Assistant** is a developer-first CLI tool that understands **Domain-Driven Design** and the conventions of the [OpenDDD.NET](https://github.com/runemalm/OpenDDD.NET) framework. It helps you generate and evolve aggregates, value objects, services, listeners, and more — all from natural language instructions.

Built with a LangGraph agent under the hood, it reasons about your modeling request, plans changes, shows previews, and applies those changes to your source code.

---

## 🚀 Quickstart

### 1. Install

```bash
pip install openddd-cli
```

> Requires Python 3.11+. Ensure you have an OpenDDD.NET-based solution available.

---

### 2. Initialize Project

```bash
openddd
```

On first run, it will create `.openddd/config.yaml` with settings like this:

```yaml
llm:
  provider: openai
  openai:
    model: gpt-4o
    api_key: sk-... # Set your OpenAI key or use OPENAI_API_KEY env var
approval_mode: suggest
log_level: info
```

---

### 3. Start Modeling

```bash
> Create a Color aggregate with a method to change tone. Also add a tone property.
```

The assistant will:
- Extract **intents**
- Understand your domain
- Generate code previews
- Apply changes (optionally with confirmation)

---

## 💬 Slash Commands

Use these to control the assistant and manage your sessions:

| Command         | Description |
|----------------|-------------|
| `/clear`        | Reset session state & history |
| `/clearhistory` | Clear conversation history only |
| `/compact`      | Summarize and compact the session |
| `/history`      | Show interaction history |
| `/sessions`     | Browse previous modeling sessions |
| `/approval`     | Switch between `suggest` and `auto` mode |
| `/model`        | Change LLM provider and model |
| `/diff`         | Show current working directory git diff |
| `/visualize`    | Show building blocks and driving adapter flows |
| `/show`         | Browse and read code for a specific building block |
| `/help`         | Display command reference and keyboard shortcuts |

> Bonus: `Ctrl+J` inserts newline. `Ctrl+C` exits.

---

## 🔧 How It Works

1. **Distills intent** from your input using a prompt-engineered LLM
2. **Analyzes project structure** (solution, layers, settings)
3. **Plans changes** using OpenDDD.NET conventions
4. **Generates code** using Jinja2 templates and AST-based transformations
5. **Previews & applies** with git-aware diffs

All actions are stored per session (`.openddd/sessions`) for future resumability.

---

## 🧱 Supported Modeling Intents

The CLI understands and generates code for:

- Aggregate Roots (create, modify, remove)
- Value Objects (add/remove, add properties)
- Repositories (create, add/remove methods)
- Event Listeners
- Custom code inside aggregates (methods, properties, commands)

---

## 📁 Project Structure

```
.
├── src/
│   ├── domain/                # Modeling logic, intent types
│   ├── graph/                 # LangGraph orchestration
│   ├── infrastructure/        # LLM, scanning, metadata, sessions
│   ├── templates/             # Jinja2 templates
│   ├── ui/                    # Prompt Toolkit + Rich UI
│   └── main.py                # Entry point
├── tests/                     # Unit + integration tests
└── .openddd/                  # Project-local config and session data
```

---

## 🧪 Testing

```bash
pytest
```

Includes full **integration tests** that verify code generation by comparing AST diffs against expected outputs. Uses sample projects like `Bookstore`.

---

## 🗝 Environment

You can use a `.env` file to set secrets:

```
OPENAI_API_KEY=sk-...
```

---

## 🛣 Roadmap

- [ ] Claude, Gemini, Mistral model support
- [ ] Plugin-based intent registry
- [ ] Git staging integration
- [ ] VSCode extension

---

## 📄 License

Licensed under the **GNU GPLv3**  
See: https://www.gnu.org/licenses/gpl-3.0.html

---

## 🙋‍♂️ About

Created by [David Runemalm](https://www.davidrunemalm.com).  
This project is part of the [OpenDDD.NET](https://github.com/runemalm/OpenDDD.NET) ecosystem.

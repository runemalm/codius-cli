# Codius

A coding assistant for domain-driven design projects.

---

## ✨ Why Codius?

`Codius` is inspired by coding assistants like OpenAI’s Codex and Anthropic’s Claude.  
If you're familiar with those tools, the interface will feel instantly familiar.

If you're a domain-driven design practitioner — or curious contributor — try it out by following the instructions below.

Want to contribute? Reach out — or just create a feature branch and submit a PR. I’ll review and get back to you ASAP.

---

## 🚀 Get Started

```bash
$ pip install codius  # Temporary package name
$ cd /my/project/root # Go to your project's root
$ codius              # Starts Codius CLI
```

On first run, Codius will create `.openddd/config.yaml` and initialize a modeling session.

---

## 🗣 Example

> _TODO: Insert a screenshot at `/images/screenshot.png` showing the CLI interface._

Sample prompt:

```bash
> Create an aggregate called Order with a method to calculate total price.
```

Codius will:

- Understand your intent
- Plan code changes
- Generate the code
- Ask for approval
- Apply the changes

---

## 🧩 Slash Commands

| Command         | Description |
|----------------|-------------|
| `/clear`        | Reset session state and history |
| `/clearhistory` | Reset session history |
| `/compact`      | Summarize and condense history |
| `/model`        | Change LLM provider/model |
| `/approval`     | Switch approval mode (suggest/auto) |
| `/sessions`     | List previous sessions |
| `/history`      | Show session history |

---

## 🧱 What is OpenDDD.NET?

Codius is built for projects using [**OpenDDD.NET**](https://www.openddd.net) — an open-source framework for building distributed, event-driven systems using **Domain-Driven Design (DDD)** in ASP.NET Core.

OpenDDD.NET helps you:

- Organize your code into bounded contexts and building blocks
- Work with aggregates, repositories, and events
- Build reliable, scalable applications using DDD best practices

To learn more, visit [www.openddd.net](https://www.openddd.net).

---

## 🔧 Requirements

- Python 3.11+
- A project built with [OpenDDD.NET](https://github.com/runemalm/OpenDDD.NET)
- OpenAI or Anthropic API key (set in `config.yaml` or use `/model` in the CLI)

---

## 🤝 Contribute

Codius is **under active development**.

If you're into:
- Domain-Driven Design
- Developer tooling
- LLM-based assistants
- Improving the modeling experience

...then jump in! Try it out, explore the codebase, and open an issue or PR.

---

## 📄 License

Licensed under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html).

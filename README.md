# Codius

A coding assistant for domain-driven design projects in ASP.NET Core.

---


## ✨ Why Codius?

`Codius` is a tool under active development with one clear goal:

> Free domain-driven designers from boilerplate and let them focus on modeling.

Instead of writing out every aggregate, method, and repository by hand, you describe what you want to build — and Codius helps generate the code that matches your intent, aligned with the [OpenDDD.NET](https://www.openddd.net) framework.

It doesn’t try to replace your thinking — it amplifies it.  
You stay in control of the model. Codius handles the scaffolding and code generation.

If you’re passionate about DDD, code quality, and improving developer flow, try Codius — or help shape it by contributing to its development.

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

![Codius CLI screenshot](images/screenshot.png)

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

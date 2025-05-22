<p align="center">
    <a href="#readme">
        <img alt="HyperFocus logo" src="https://raw.githubusercontent.com/u8slvn/hyperfocus/main/docs/source/_static/logo.png">
    </a>
</p>
<p align="center">
    <a href="https://pypi.org/project/hyperfocus/"><img src="https://img.shields.io/pypi/v/hyperfocus.svg" alt="Pypi Version"></a>
    <a href="https://pypi.org/project/hyperfocus/"><img src="https://img.shields.io/pypi/pyversions/hyperfocus" alt="Python Version"></a>
    <a href="https://github.com/u8slvn/hyperfocus/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/u8slvn/hyperfocus/ci.yml?label=CI" alt="CI"></a>
    <a href="https://hyperfocus.readthedocs.io/"><img alt="Read the Docs" src="https://img.shields.io/readthedocs/hyperfocus"></a>
    <a href="https://coveralls.io/github/u8slvn/hyperfocus?branch=main"><img src="https://coveralls.io/repos/github/u8slvn/hyperfocus/badge.svg?branch=main" alt="Coverage Status"></a>
    <a href="https://app.codacy.com/gh/u8slvn/hyperfocus/dashboard"><img src="https://img.shields.io/codacy/grade/01ddd5668dbf4fc09f20ef215d0eec0b" alt="Code Quality"></a>
    <a href="https://pypi.org/project/hyperfocus/"><img src="https://img.shields.io/pypi/l/hyperfocus" alt="Project license"></a>
</p>

---

**HyperFocus** is a minimalist CLI daily tasks manager designed to help you maintain focus by eliminating distractions. It emphasizes daily planning and intentional task management, helping you concentrate only on what matters today.

## Features

- **Daily focus**: Plan and manage tasks one day at a time
- **Clean terminal UI**: Distraction-free interface with colorful, easy-to-read text formatting
- **Task lifecycle management**: Create, update, complete, and review tasks
- **Task details**: Add notes, links, and additional information to tasks
- **Simple workflow**: Review yesterday's tasks and build today's plan
- **Task stashing**: Temporarily set aside tasks that aren't relevant for today but might be needed later

## Philosophy

**HyperFocus** embraces the principle that productivity comes from intentional constraint rather than endless possibility. By deliberately limiting your planning horizon to a single day, it eliminates the anxiety of long-term task accumulation and the paralysis that comes from seeing an overwhelming future workload. This philosophy recognizes that meaningful progress happens through consistent daily action, not through elaborate multi-week planning that often becomes outdated or ignored.

## Quickstart

### Installation

#### Using pipx (recommended)

[pipx](https://pypa.github.io/pipx/) installs and runs Python applications in isolated environments, keeping your system clean.

```bash
pipx install hyperfocus
```

#### Using pip

```bash
pip install hyperfocus
```

#### Verify Installation

```bash
hyf --version
```

### Initialization

HyperFocus needs to initialize a database and configuration file in your home directory:

```bash
hyf init
```

## Usage Examples

### Basic Task Management

```bash
# Add a new task
hyf add "Implement the new super feature"

# Add a task with details
hyf add "Read article about Python" -d "https://python-article.com"

# View your daily tasks, each task has a unique ID
hyf status

# Complete a task
hyf done 1
```

### Additional Commands

```bash
# Show task details
hyf show 2

# Edit a task
hyf edit 2 --title "Read article about Python 3"

# Copy task details to clipboard
hyf copy 2

# Delete a task
hyf delete 2

# Hard delete a task (permanently)
hyf delete 2 --hard

# Previous day's tasks
hyf log
```

### Stash Tasks

```bash
# Stash a task for later
hyf stash 2

# View your stashed tasks
hyf stash list

# Restore a stashed task to today
hyf stash pop 1
```

Find more information about all the commands in the documentation: [hyperfocus.readthedocs.io](https://hyperfocus.readthedocs.io)

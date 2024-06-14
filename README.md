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

**HyperFocus** is a minimalist CLI daily tasks manager that helps you stay focused on your work by avoiding distractions.

## 📜 Philosophy

You won't anticipate more than your daily goal with **HyperFocus**. No tasks prepared for the next week or month. The workflow is designed around the idea that, on a daily basis, you will review each unfinished tasks from the past day and choose whether you want to add it to the daily tasks. You are then able to prepare all your tasks for the day and update them to follow your work. The intention is to avoid overwhelming yourself and focus only on what you have prepared to do, for you and only you.

## 🚀 Quickstart

### Installation

The library [pipx](https://pypa.github.io/pipx/) allows to install and run Python applications in isolated environments so it does not mess around with your local installed library versions by keeping your local machine clean even after an uninstallation.

```bash
pipx install hyperfocus
```

Test your installation:

```bash
hyf --version
```

### Initialization

In order to work properly, **HyperFocus** needs to initialize a database and a configuration file. Both are generated into your home directory, unless you specified another location.

```bash
hyf init
```

### Example Usage

Add a new task:

```bash
hyf add "Implement the new super feature"
```

Add a new task with details:

```bash
hyf add "Read the great article about Python" -d
>>> ? Task details: https://python-article.com
```

Follow your daily tasks:

```bash
hyf status
```

or:

```bash
hyf
```

Find more information about all the commands in the documentation: [hyperfocus.readthedocs.io](https://hyperfocus.readthedocs.io)

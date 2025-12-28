# Interactive Mode Flags

> **Documentation for interactive mode flags**

## Overview

Lixplore offers three interactive modes for easier usage without memorizing command-line flags.

**Total Interactive Flags:** 3

---

## `--tui`

**Description:** Launch enhanced TUI (Text User Interface) mode - the primary interactive interface.

**Syntax:**
```bash
lixplore --tui
lixplore  # Default when no arguments provided
```

**Type:** Boolean flag

### Features
- Visual search interface
- Browse and select articles
- Annotation management
- Statistics dashboard
- Export functionality
- Beautiful terminal UI

### Examples

**Example 1: Launch TUI**
```bash
lixplore --tui
```

**Example 2: Default Mode**
```bash
lixplore
# Automatically launches TUI if no query provided
```

### Navigation
- **Arrow keys:** Navigate menus
- **Enter:** Select option
- **Space:** Mark/unmark items
- **q:** Quit
- **h:** Help

### TUI Screens
1. **Search:** Enter query and select sources
2. **Results:** Browse and select articles
3. **Annotations:** Manage annotations
4. **Statistics:** View analytics
5. **Export:** Export selected items

---

## `--shell`

**Description:** Launch interactive shell mode (persistent session).

**Status:** Deprecated - use `--tui` instead

**Syntax:**
```bash
lixplore --shell
```

**Type:** Boolean flag

### Features
- Persistent session
- Command history
- No need to type 'lixplore' repeatedly
- Tab completion

### Examples

**Example 1: Shell Mode**
```bash
lixplore --shell

lixplore> search "cancer" -P -m 20
lixplore> annotate 5 --rating 5
lixplore> list annotations
lixplore> export markdown
lixplore> exit
```

**Note:** This mode is deprecated. Use `--tui` for better experience.

---

## `--wizard`

**Description:** Launch wizard mode with guided workflows.

**Status:** Deprecated - use `--tui` instead

**Syntax:**
```bash
lixplore --wizard
```

**Type:** Boolean flag

### Features
- Step-by-step guided workflows
- No flags to memorize
- Interactive prompts
- Beginner-friendly

### Examples

**Example 1: Wizard Mode**
```bash
lixplore --wizard

What do you want to do?
  1. Search for articles
  2. Annotate an article
  3. View annotations
  4. Export results

Select option: 1

Which sources do you want to search?
  [ ] PubMed
  [ ] Crossref
  [x] arXiv
  ...
```

**Note:** This mode is deprecated. Use `--tui` for better experience.

---

## Best Practices

### When to Use Interactive Modes

**Use TUI Mode When:**
- Learning Lixplore for the first time
- You prefer visual interfaces
- Complex multi-step workflows
- Exploring features

**Use Command Line When:**
- Scripting and automation
- Quick one-off searches
- Integrating with other tools
- CI/CD pipelines

---

**Last Updated:** 2024-12-28

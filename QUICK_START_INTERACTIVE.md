# 🚀 Quick Start: Interactive Modes

## NEW! Two Easy Ways to Use Lixplore

### Option 1: Shell Mode (Like OpenBB Terminal) 🐚

**Perfect for: Power users, multiple operations, continuous workflow**

```bash
# Launch shell
lixplore --shell

# Inside shell - no need to type 'lixplore' anymore!
lixplore> search "cancer treatment" -P -m 20
lixplore> annotate 5 --rating 5 --tags "important"
lixplore> list annotations
lixplore> export markdown
lixplore> exit
```

**Key Benefits:**
- ⚡ No repetitive typing
- 📋 Command history (use arrow keys)
- 🔄 Persistent session
- 💡 Built-in help system

---

### Option 2: Wizard Mode (Guided Experience) 🧙

**Perfect for: Beginners, learning, when you forget syntax**

```bash
# Launch wizard
lixplore --wizard
```

**Interactive Prompts:**
```
What do you want to do?
  1. Search for articles
  2. Annotate an article
  3. View my annotations
  4. Export annotations
  5. Download PDFs

Your choice [1]: 1

What do you want to search for?: kidney transplant

Which database?
  1. PubMed (biomedical)
  2. arXiv (CS/physics)
  3. All databases

Your choice [1]: 1

How many results? [10]: 20

✓ Done! Found 20 articles
```

**Key Benefits:**
- 🎯 Step-by-step guidance
- 📝 No flags to remember
- 💭 Helpful examples
- ✨ Perfect for learning

---

## 🎮 Try It Now!

### 5-Minute Tutorial

**Step 1: Launch Shell**
```bash
lixplore --shell
```

**Step 2: Search**
```bash
lixplore> search "machine learning" -x -m 10
```

**Step 3: View**
```bash
lixplore> list
lixplore> view 3
```

**Step 4: Annotate**
```bash
lixplore> annotate 3 --rating 5 --tags "important"
```

**Step 5: Export**
```bash
lixplore> export markdown
```

**Done!** 🎉

---

## 🆚 Which Mode Should I Use?

| If you want... | Use this |
|----------------|----------|
| Fast workflow, multiple commands | **Shell Mode** |
| Guidance, learning | **Wizard Mode** |
| One quick command | Command Line |
| Automation, scripts | Command Line |

---

## 💡 Pro Tip: Combine Them!

```bash
# Start shell
lixplore --shell

# Use wizard when needed
lixplore> wizard
  [Follow prompts]

# Back to shell for quick commands
lixplore> list annotations
lixplore> export json
```

---

## 📖 Learn More

- Full Guide: `INTERACTIVE_MODES_GUIDE.md`
- All Features: `README.md`
- Man Page: `man lixplore`

**Happy Researching! 🚀**

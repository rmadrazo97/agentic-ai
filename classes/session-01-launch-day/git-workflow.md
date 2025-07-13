# Git Workflow for Teams

## 📁 Folder-Based Branch Management

Instead of complex git branching, we use a simple folder structure:

```
course-repo/
├── team-alpha/
│   ├── main/       # Production code (protected)
│   ├── dev/        # Active development
│   └── feature-x/  # Feature branches
├── team-beta/
│   ├── main/
│   ├── dev/
│   └── feature-y/
└── team-gamma/
    ├── main/
    └── dev/
```

## 🔄 Workflow Examples

### Daily Development
```bash
# Always work in dev folder
cd team-alpha/dev/
# Make changes
git add .
git commit -m "feat: add memory to agent"
git push
```

### Feature Development
```bash
# Create feature folder
mkdir team-alpha/feature-rag
cp -r team-alpha/dev/* team-alpha/feature-rag/
cd team-alpha/feature-rag/
# Develop feature
git add .
git commit -m "feat: implement RAG pipeline"
git push
```

### Promote to Main (End of Sprint)
```bash
# After testing in dev
cp -r team-alpha/dev/* team-alpha/main/
cd team-alpha/main/
git add .
git commit -m "release: sprint 3 - working chat agent"
git push
```

## ✅ Benefits

1. **Simple** - No merge conflicts between teams
2. **Visual** - See all work in file explorer
3. **Safe** - Main folder is protected
4. **Flexible** - Easy feature experiments

## 🚫 Rules

1. **Never** edit directly in `main/` during development
2. **Always** test in `dev/` first
3. **Copy** to `main/` only when feature is complete
4. **Each team** owns their folder completely

## 📝 Example Team Structure After Sprint 3

```
team-alpha/
├── main/
│   ├── agents/
│   │   ├── chat_agent.py      ✅ (tested & working)
│   │   └── memory.py          ✅ (tested & working)
│   ├── tests/
│   └── requirements.txt
├── dev/
│   ├── agents/
│   │   ├── chat_agent.py      🔄 (improving)
│   │   ├── memory.py
│   │   └── planner.py         🆕 (new feature)
│   └── tests/
└── feature-voice/
    └── agents/
        └── voice_interface.py  🧪 (experimental)
```
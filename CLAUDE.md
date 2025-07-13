# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is the **Agentic AI Course repository** - an educational repository for a 17-week computer science course teaching students to build production-ready AI agents through a startup simulation format. Students work in teams of 1-3 to develop real AI agent applications.

## Course Structure & Architecture

### Educational Format
- **34 sessions** (2 per week, 80 minutes each)
- **Session rhythm**: 10min standup → 15-20min lecture → 45-50min lab → 5min wrap-up
- **Startup simulation**: Teams build actual products from concept to deployment
- **External demo day**: Final presentations to industry panel

### Team Workflow - Folder-Based Branch Management
This repository uses a **unique folder-based approach** instead of traditional git branching:

```
course-repo/
├── team-[name]/
│   ├── main/       # Production-ready code (protected)
│   ├── dev/        # Active development work
│   └── feature-x/  # Feature branch folders
```

**Key workflow commands:**
```bash
# Daily development (always work in dev/)
cd team-name/dev/
git add . && git commit -m "feat: description" && git push

# Feature development
mkdir team-name/feature-rag
cp -r team-name/dev/* team-name/feature-rag/
cd team-name/feature-rag/

# Promote to production (end of sprint)
cp -r team-name/dev/* team-name/main/
cd team-name/main/
git add . && git commit -m "release: sprint X - description" && git push
```

### Technology Stack
- **Agent Frameworks**: LangChain, AutoGen
- **LLM Providers**: OpenAI GPT-4o, Anthropic Claude, Google Gemini, X AI Grok
- **Backend**: FastAPI
- **Vector Databases**: Chroma, Pinecone
- **Development**: GitHub Classroom, Docker, VS Code

## Session Materials Structure

Session content is organized in `/classes/session-XX-name/` directories containing:
- `README.md` - Interactive presentation guide (PowerPoint replacement)
- Python demo files with live coding examples
- Shell scripts for automated setup
- Workflow templates and documentation

### Session 1 Files
- `README.md` - Launch day presentation with visual timeline
- `agent-types-demo.py` - Live demos of 6 agent types
- `team-setup.sh` - Automated team initialization
- `git-workflow.md` - Folder-based workflow documentation
- `standup-template.md` - Daily standup format

## Agent Architecture Patterns

The course covers 6 types of AI agents:
1. **Conversational Assistants** (ChatGPT-style dialogue)
2. **Task Loop Agents** (Auto-GPT autonomous loops)
3. **Tool-Calling Agents** (ReAct pattern with function calling)
4. **Planning Agents** (Goal decomposition and execution)
5. **Multi-Agent Systems** (Collaborative agent teams)
6. **Edge/Embodied Agents** (Local, real-time, physical)

## Development Practices

### Student Team Management
- Teams use GitHub Classroom for project repositories
- Daily standups via PR comments using provided template
- Issue-driven development with sprint planning
- Progress tracking through folder structure and commits

### Assessment Components
- Sprint Participation (15%) - Standup quality, git activity
- Lab Checkpoints (30%) - Technical correctness, CI tests
- Mid-Semester Demo (20%) - Week 8 functionality demo
- Final Demo Day (35%) - External panel presentation

## Content Creation Guidelines

When creating new session materials:
- Use interactive README.md as presentation slides
- Include live coding examples in separate .py files
- Provide automation scripts for setup tasks
- Maintain visual formatting with emojis and clear sections
- Link to external resources for extended learning

## Course Phases

1. **Foundations (Weeks 1-4)**: LLM basics, prompt engineering, ReAct patterns
2. **Advanced Patterns (Weeks 5-8)**: Autonomous loops, memory, function calling
3. **Production Systems (Weeks 9-12)**: Multi-agent, voice, cost optimization
4. **Deployment & Demo (Weeks 13-17)**: Ethics, human-in-loop, final projects
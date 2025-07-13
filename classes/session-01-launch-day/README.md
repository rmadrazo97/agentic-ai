# Session 1: Launch Day & Team Formation 🚀

**Duration**: 80 minutes | **Time**: 8:30 - 9:50

---

## 🎯 Session Goals
- Launch your AI agent startup journey
- Form teams & pick your domain
- Set up your development environment
- Understand the 6 types of AI agents

---

## ⏱️ Session Timeline

### 1. Welcome & Course Vision (10 min)
> **"Build a venture-grade autonomous agent in 17 weeks"**

#### 🔥 Quick Facts
- **34 sessions** = Your runway
- **5 LLM providers** = Your toolkit  
- **1 product** = Your portfolio piece
- **Real startup rules** = Your experience

#### 📊 Success Metrics
- ✅ Working agent deployed to production
- ✅ Multi-provider integration
- ✅ External panel demo
- ✅ Industry-ready skills

---

### 2. Startup Simulation Rules (10 min)

#### 🏢 Your "Company" Structure
```
Team Size: 1-3 developers
Workflow:  GitHub = Your Office
           PRs = Team Demos
           Issues = Product Backlog
           CI/CD = Quality Control
```

#### 📋 Sprint Rules
- **2 sessions = 1 sprint**
- **Daily standup** at class start
- **Everyone commits** (no free-riders!)
- **Public progress** (transparency)

#### 🎮 [Accept GitHub Classroom Invite →](https://classroom.github.com/a/YOUR_ASSIGNMENT_ID)

---

### 3. Repo Onboarding LIVE (10 min)

#### 🛠️ Follow Along:
```bash
# 1. Clone the course repo
git clone https://github.com/ufm-agentic-ai/course-repo
cd course-repo

# 2. Create your team folder structure
mkdir -p [team-name]/main
cd [team-name]/main

# 3. Make your first commit
echo "# Team [Name] is here! 🚀" > README.md
git add .
git commit -m "feat: team [name] initialization"
git push

# 4. Create dev branch folder
git checkout -b dev
mkdir ../dev
cp README.md ../dev/
git add ../dev
git commit -m "feat: setup dev environment"
git push -u origin dev
```

#### 📁 Team Folder Structure:
```
[team-name]/
├── main/          # Production-ready code
├── dev/           # Development work
└── feature-x/     # Feature branches
```

---

### 4. The 6 Types of AI Agents (15 min)

#### 🤖 Agent Taxonomy

##### 1️⃣ **Conversational Assistants**
```python
# Like ChatGPT, Claude
agent.chat("Help me write code")
→ Natural dialogue interface
```
**Examples**: Customer support, coding assistants

##### 2️⃣ **Task Loop Agents**
```python
# Auto-GPT style
while not goal_achieved:
    task = agent.plan_next_task()
    result = agent.execute(task)
    agent.reflect(result)
```
**Examples**: Research automation, data analysis

##### 3️⃣ **Tool-Calling Agents**
```python
# ReAct pattern
thought = agent.think(query)
action = agent.select_tool(thought)
result = tool.execute(action)
```
**Examples**: [GitHub Copilot Workspace](https://github.com/features/copilot), API orchestrators

##### 4️⃣ **Planning Agents**
```python
# Decompose then execute
plan = agent.create_plan(goal)
for step in plan:
    agent.execute_step(step)
```
**Examples**: [Devin](https://www.cognition-labs.com/), project managers

##### 5️⃣ **Multi-Agent Systems**
```python
# Specialized team collaboration
manager = Agent("coordinator")
coder = Agent("developer")
tester = Agent("qa")
manager.delegate(task, [coder, tester])
```
**Examples**: [AutoGen](https://github.com/microsoft/autogen), CrewAI

##### 6️⃣ **Edge/Embodied Agents**
```python
# Local, real-time, physical
sensor_data = device.read_sensors()
action = local_model.decide(sensor_data)
device.execute(action)
```
**Examples**: Smart home, robotics, IoT

---

### 5. Domain Selection Workshop (15 min)

#### 🎯 Choose Your Arena

<table>
<tr>
<td width="33%">

**🎓 EdTech**
- Personalized tutors
- Auto-grading
- Study buddies
- Content generation

</td>
<td width="33%">

**💰 FinTech**
- Trading assistants
- Risk analyzers
- Report generators
- Fraud detection

</td>
<td width="33%">

**🛠️ DevOps**
- PR reviewers
- Bug triagers
- Deploy agents
- Doc writers

</td>
</tr>
<tr>
<td width="33%">

**📈 Productivity**
- Email drafters
- Meeting summaries
- Task automation
- Knowledge base

</td>
<td width="33%">

**🏥 HealthTech**
- Symptom checkers
- Med reminders
- Mental health
- Data analysis

</td>
<td width="33%">

**🎮 Creative**
- Game NPCs
- Story writers
- Music composers
- Art assistants

</td>
</tr>
</table>

#### 💡 Problem Brainstorm (5 min)
> What specific problem will YOUR agent solve?

#### 🗳️ Team Formation (5 min)
1. Find 1-2 partners OR go solo
2. Agree on domain + problem
3. Pick a team name!

---

### 6. Project Charter Sprint (15 min)

#### 📝 Create Your Charter

```markdown
# Team: [Your Team Name]

## 🎯 Problem Statement
What specific problem are we solving?

## 👥 Target Users
Who will use this agent?

## 🤖 Agent Type
Which of the 6 types fits best?

## 📊 Success Metric
How do we measure if it works?

## 🚀 MVP Features (Top 3)
1. 
2. 
3. 
```

#### 📍 Save as: `[team-name]/main/PROJECT-CHARTER.md`

#### 🎫 Create First Issue
```
Title: Sprint 1 - Basic Agent Skeleton
Body:
- [ ] Set up LangChain project
- [ ] Create basic prompt template  
- [ ] Connect to OpenAI API
- [ ] Simple CLI interface
- [ ] Basic error handling
```

---

### 7. Wrap-up & Next Steps (5 min)

#### ✅ Before You Leave
- [ ] Team formed & charter committed
- [ ] GitHub repo access confirmed
- [ ] Draft PR opened
- [ ] First issue created

#### 📚 Homework (Due Session 2)
1. **Read**: [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
2. **Read**: [Anthropic's Claude Prompting](https://docs.anthropic.com/claude/docs/introduction-to-prompt-design)
3. **Watch**: [ReAct Paper Explained (12min)](https://www.youtube.com/watch?v=Eug2clsLtFs)
4. **Do**: Get API keys from OpenAI (we'll use free tier)

#### 💬 First Standup Comment
On your Draft PR, comment:
```
**Sprint 1 Plan:**
- What: [Your first technical goal]
- Blockers: [Any setup issues?]
- Help needed: [Specific questions]
```

---

## 🎉 Welcome to Your AI Agent Startup!

### Remember:
- **Ship early, ship often**
- **Perfect is the enemy of done**
- **Your code is your resume**

### Quick Links:
- 📖 [Course Repo](https://github.com/ufm-agentic-ai)
- 💬 [Class Slack](https://ufm-agentic-ai.slack.com)
- 🎯 [Submission Deadlines](../deadlines.md)

---

*Next Session: LLM Fundamentals & Prompt Engineering with OpenAI*
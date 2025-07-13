# Daily Standup Template

## Format for PR Comments

Copy and paste this template for your standup updates:

```markdown
## 📅 Standup - [Date]

### ✅ What I did:
- 

### 🎯 What I'm doing today:
- 

### 🚧 Blockers:
- None
<!-- OR -->
- [Describe specific blocker and what help you need]

### 💭 Questions/Help needed:
- 
```

---

## Examples of Good Standups

### Example 1: Making Progress
```markdown
## 📅 Standup - Sept 5

### ✅ What I did:
- Set up project structure and GitHub repo
- Researched LangChain documentation
- Created basic agent class skeleton

### 🎯 What I'm doing today:
- Implement first prompt template
- Test connection to OpenAI API
- Write unit test for agent initialization

### 🚧 Blockers:
- None

### 💭 Questions/Help needed:
- Best practice for storing API keys locally?
```

### Example 2: Facing Blockers
```markdown
## 📅 Standup - Sept 7

### ✅ What I did:
- Tried to implement ReAct pattern
- Read research paper on agent architectures

### 🎯 What I'm doing today:
- Debug why agent loops infinitely
- Simplify prompt to basic version first

### 🚧 Blockers:
- Agent gets stuck in thinking loop, never reaches action

### 💭 Questions/Help needed:
- Can someone review my ReAct implementation?
- Is there a simpler pattern I should try first?
```

### Example 3: Pivot/Change
```markdown
## 📅 Standup - Sept 10

### ✅ What I did:
- Team discussion about project scope
- Decided to pivot from finance to edtech

### 🎯 What I'm doing today:
- Update PROJECT-CHARTER.md with new direction
- Research education-specific APIs
- Create new user stories

### 🚧 Blockers:
- Need to find good education datasets

### 💭 Questions/Help needed:
- Anyone know good sources for practice problems?
```

---

## Standup Best Practices

### ✅ DO:
- Be specific ("implemented function X" not "worked on code")
- Mention PR numbers or commits when relevant
- Ask for help early when stuck
- Keep it concise but informative

### ❌ DON'T:
- Write novels (3-5 bullet points per section)
- Be vague ("stuff", "things", "various tasks")
- Hide blockers (we're here to help!)
- Copy yesterday's standup

---

## Red Flags We Watch For:

1. **Same blocker 3+ days** → Needs intervention
2. **No commits for a sprint** → Check team dynamics
3. **Vague updates repeatedly** → May need guidance
4. **No questions ever** → Might be struggling silently

Remember: Standups are for **communication**, not judgment!
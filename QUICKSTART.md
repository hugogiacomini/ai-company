# Quick Reference Guide

## 🚀 Getting Started (1 Minute)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. View organizational structure
python main.py --show-org

# 4. Run a quick test
python src/quick_start.py
```

## 📊 Organizational Structure

```
CEO (Executive)
├── CTO (Executive)
│   └── Head of Software Development
│       ├── Senior Software Developer
│       ├── Software Developer
│       └── QA Analyst
│
├── Head of Marketing
│   ├── Marketing Analyst
│   └── Content Marketing Expert
│
├── Head of Operations
│   ├── Operations Analyst
│   └── Quality Assurance Expert
│
├── Head of HR
│   ├── Recruitment Specialist
│   └── HR Analyst
│
└── Head of Commercial
    ├── Sales Analyst
    └── Business Development Expert
```

## 💡 Common Use Cases

### 1. Run Department Workflow
```python
from company import AICompany, Department

company = AICompany()

# Marketing campaign
company.run_department_workflow(
    Department.MARKETING,
    campaign_goal="Product launch"
)
```

### 2. Product Launch (Cross-functional)
```python
company.run_product_launch("AI Assistant Pro")
```

### 3. Strategic Planning
```python
company.run_strategic_planning("2025 Strategy")
```

### 4. Quarterly Business Review
```python
company.run_quarterly_review("Q4 2024")
```

## 🎯 Example Scenarios

Run predefined scenarios:

```bash
# Marketing campaign
python src/examples.py --scenario 1

# Software development
python src/examples.py --scenario 2

# HR recruitment
python src/examples.py --scenario 3

# Product launch (cross-functional)
python src/examples.py --scenario 4

# Quarterly review
python src/examples.py --scenario 5

# Strategic planning
python src/examples.py --scenario 6
```

## 🏗️ Project Structure

```
ai-company/
├── src/company/          # Main package
│   ├── models/          # Organizational hierarchy
│   ├── agents/          # Agent definitions
│   ├── tasks/           # Task templates
│   ├── crews/           # Department crews
│   └── company.py       # Main orchestration
│
├── src/examples.py      # Example scenarios
├── src/quick_start.py   # Quick start guide
├── main.py              # CLI interface
└── tests/               # Unit & integration tests
```

## 🔧 Customization

### Add a New Role

Edit `src/company/models/hierarchy.py`:

```python
Role(
    title="Product Manager",
    level=RoleLevel.EXPERT,
    department=Department.SOFTWARE_DEVELOPMENT,
    reports_to="Head of Software Development",
    responsibilities=[...],
    skills=[...]
)
```

### Create a Custom Agent

Edit `src/company/agents/company_agents.py`:

```python
@staticmethod
def create_product_manager() -> Agent:
    return Agent(
        role="Product Manager",
        goal="Define product roadmap",
        backstory="Experienced PM...",
        verbose=True
    )
```

### Define a Custom Task

Edit `src/company/tasks/company_tasks.py`:

```python
@staticmethod
def create_roadmap_task(agent) -> Task:
    return Task(
        description="Create product roadmap",
        agent=agent,
        expected_output="Roadmap document"
    )
```

## 📈 Departments Overview

| Department | Roles | Key Responsibilities |
|------------|-------|---------------------|
| **Executive** | 2 | Strategy, Leadership, Technology |
| **Marketing** | 3 | Campaigns, Content, Analysis |
| **Operations** | 3 | Processes, Quality, Efficiency |
| **HR** | 3 | Recruitment, Engagement, Analytics |
| **Software Dev** | 4 | Development, Testing, Quality |
| **Commercial** | 3 | Sales, Business Development, Analysis |

## ⚙️ Configuration

### Environment Variables
- `OPENAI_API_KEY` (required): Your OpenAI API key
- `COMPANY_NAME` (optional): Custom company name

### Agent Settings
- `verbose`: Show detailed logs
- `allow_delegation`: Enable task delegation
- `max_iter`: Maximum iterations per task

### Crew Processes
- `Process.sequential`: Tasks execute in order
- `Process.hierarchical`: Follow management hierarchy

## 🧪 Testing

```bash
# Run all tests
python tests/run_tests.py

# Run specific test file
python -m pytest tests/test_hierarchy.py -v

# Run with coverage
python -m pytest tests/ --cov=src/company
```

## ⚠️ Important Notes

### API Costs
- Each workflow makes multiple LLM API calls
- Costs vary by complexity and number of agents
- Monitor your OpenAI usage dashboard

### Rate Limits
- OpenAI has request/minute limits
- Large workflows may need delays
- Consider batch processing for many tasks

### Best Practices
1. Start with simple, single-department workflows
2. Test with small teams before scaling
3. Monitor API costs closely
4. Use specific, focused prompts
5. Review outputs for quality

## 🐛 Troubleshooting

### "No module named 'crewai'"
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"
```bash
cp .env.example .env
# Add your API key to .env
```

### Import errors
```bash
# Run from project root
cd ai-company
python main.py --show-org
```

### Tests failing
```bash
# Set test API key
export OPENAI_API_KEY=test-key
python tests/run_tests.py
```

## 📚 Learn More

- **README.md**: Complete documentation
- **ARCHITECTURE.md**: System design details
- **CONTRIBUTING.md**: How to contribute
- **CrewAI Docs**: https://docs.crewai.com/

## 🎓 Tutorials

### Tutorial 1: First Workflow
1. Set up environment
2. View org chart
3. Run marketing workflow
4. Review results

### Tutorial 2: Custom Scenario
1. Define new task
2. Create crew
3. Execute workflow
4. Analyze output

### Tutorial 3: Cross-functional Project
1. Use product launch crew
2. Coordinate departments
3. Review deliverables
4. Iterate based on feedback

---

**Need Help?** Open an issue on GitHub or check the documentation.

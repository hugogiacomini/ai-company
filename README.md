# AI Company Simulation

A sophisticated simulation of a real software development company with **dual-backend support**: **CrewAI** for traditional sequential orchestration and **Claude Code** for custom subagents with parallel execution. The system implements a complete organizational hierarchy with CEO, CTO, Department Heads, Experts, Developers, Analysts, and more.

## 🏢 Overview

This project simulates a full-featured AI-powered company with:

- **Complete Organizational Hierarchy**: From C-level executives to junior staff
- **Multiple Departments**: Marketing, Operations, HR, Software Development, Commercial
- **Intelligent AI Agents**: Each agent has specific roles, expertise, and responsibilities
- **Realistic Workflows**: Cross-functional collaboration, product launches, quarterly reviews
- **Dual Backend Support**: Choose between CrewAI or Claude Code custom subagents
- **Parallel Execution**: Claude Code backend supports concurrent agent workflows

## 🔧 Backend Options

### CrewAI Backend (Default)
- Traditional sequential agent orchestration
- Stable and production-ready
- Requires OpenAI API key

### Claude Code Backend
- Custom subagents defined in `.claude/agents/` markdown files
- Supports parallel task execution
- Runs within Claude Code environment
- 16 specialized subagent definitions included

**See [BACKEND_GUIDE.md](BACKEND_GUIDE.md) for detailed backend documentation.**

## 📋 Organizational Structure

### Executive Level
- **CEO**: Strategic leadership and company vision
- **CTO**: Technology strategy and innovation

### Departments

#### 🎯 Marketing Department
- Head of Marketing
- Marketing Analyst
- Content Marketing Expert

#### ⚙️ Operations Department
- Head of Operations
- Operations Analyst
- Quality Assurance Expert

#### 👥 Human Resources Department
- Head of HR
- Recruitment Specialist
- HR Analyst

#### 💻 Software Development Department
- Head of Software Development
- Senior Software Developer
- Software Developer
- QA Analyst

#### 💼 Commercial Department
- Head of Commercial
- Sales Analyst
- Business Development Expert

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/hugogiacomini/ai-company.git
cd ai-company
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. **Run the quick start example**
```bash
python src/quick_start.py
```

## 💡 Usage Examples

### Display Organizational Chart

```python
from company import AICompany

company = AICompany("My AI Company")
company.display_organizational_chart()
```

### Run a Department Workflow

```python
from company import AICompany, Department

company = AICompany()

# Marketing campaign
result = company.run_department_workflow(
    Department.MARKETING,
    campaign_goal="Launch new AI product"
)

# Software development
result = company.run_department_workflow(
    Department.SOFTWARE_DEVELOPMENT,
    feature="User authentication system"
)

# HR recruitment
result = company.run_department_workflow(
    Department.HUMAN_RESOURCES,
    focus="talent acquisition"
)
```

### Run Cross-Functional Scenarios

```python
# Product launch (involves multiple departments)
company.run_product_launch("AI Assistant Pro")

# Quarterly business review
company.run_quarterly_review("Q4 2024")

# Strategic planning session
company.run_strategic_planning("2025 Annual Strategy")
```

### Run Example Scenarios

```bash
# Show organizational structure
python src/examples.py --show-structure

# Run specific scenario
python src/examples.py --scenario 1  # Marketing campaign
python src/examples.py --scenario 2  # Software development
python src/examples.py --scenario 3  # HR recruitment
python src/examples.py --scenario 4  # Product launch
python src/examples.py --scenario 5  # Quarterly review
python src/examples.py --scenario 6  # Strategic planning
```

## 🎭 Available Scenarios

1. **Marketing Campaign**: Marketing team plans and executes a campaign
2. **Software Development**: Dev team builds a new feature
3. **HR Recruitment**: HR team recruits new talent
4. **Product Launch**: Cross-functional team launches a product
5. **Quarterly Review**: All departments present quarterly performance
6. **Strategic Planning**: Executives plan company strategy

## 🏗️ Project Structure

```
ai-company/
├── src/
│   ├── company/
│   │   ├── __init__.py
│   │   ├── company.py              # Main AICompany class
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   └── company_agents.py   # Agent definitions
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   └── company_tasks.py    # Task definitions
│   │   ├── crews/
│   │   │   ├── __init__.py
│   │   │   └── company_crews.py    # Crew configurations
│   │   └── models/
│   │       ├── __init__.py
│   │       └── hierarchy.py        # Organizational models
│   ├── examples.py                 # Example scenarios
│   └── quick_start.py              # Quick start script
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔑 Key Features

### Hierarchical Organization
- Realistic company structure with reporting relationships
- Clear role definitions and responsibilities
- Skills and expertise mapping for each role

### Intelligent Agents
- Each agent has a unique personality and backstory
- Agents can delegate tasks based on hierarchy
- Specialized expertise in their domain

### Flexible Task System
- Pre-defined task templates for common scenarios
- Customizable task parameters
- Support for complex workflows

### Department Crews
- Teams organized by department
- Cross-functional collaboration support
- Sequential and parallel task execution

## 🛠️ Customization

### Adding New Roles

Edit `src/company/models/hierarchy.py` to add new roles to the organizational chart:

```python
Role(
    title="New Role Title",
    level=RoleLevel.EXPERT,
    department=Department.MARKETING,
    reports_to="Head of Marketing",
    responsibilities=["Responsibility 1", "Responsibility 2"],
    skills=["Skill 1", "Skill 2"]
)
```

### Creating New Agents

Add agent factory methods in `src/company/agents/company_agents.py`:

```python
@staticmethod
def create_new_agent() -> Agent:
    return Agent(
        role="New Agent Role",
        goal="Agent's goal",
        backstory="Agent's backstory",
        verbose=True,
        allow_delegation=False
    )
```

### Defining Custom Tasks

Add task creation methods in `src/company/tasks/company_tasks.py`:

```python
@staticmethod
def create_custom_task(agent, context: str) -> Task:
    return Task(
        description=f"Task description with {context}",
        agent=agent,
        expected_output="Expected output description"
    )
```

## 📊 Example Output

When you run a workflow, you'll see detailed execution logs showing:
- Agent reasoning and decision-making
- Task execution progress
- Inter-agent collaboration
- Final deliverables

## 🔒 Environment Variables

Required environment variables (see `.env.example`):

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `COMPANY_NAME`: Company name for simulation (optional)

Optional LLM provider keys:
- `ANTHROPIC_API_KEY`: For Claude models
- `GOOGLE_API_KEY`: For Google models

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new departments and roles
- Create new scenarios and workflows
- Improve agent capabilities
- Enhance documentation

## 📚 Learn More

### Project Documentation

- [BACKEND_GUIDE.md](BACKEND_GUIDE.md) - Comprehensive guide to using both backends
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - High-priority improvements (testing, logging, exceptions)
- [MEDIUM_PRIORITY_IMPROVEMENTS.md](MEDIUM_PRIORITY_IMPROVEMENTS.md) - Performance & quality enhancements (caching, validation)
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines

### External Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [LangChain Documentation](https://python.langchain.com/)

## ⚠️ Notes

- This simulation requires OpenAI API credits
- Each workflow execution makes multiple API calls
- Costs depend on the complexity and number of agents/tasks
- Set appropriate rate limits for production use

## 🎯 Use Cases

- **Training**: Understand organizational dynamics
- **Prototyping**: Test business processes and workflows
- **Education**: Learn about AI agent orchestration
- **Research**: Experiment with multi-agent systems
- **Planning**: Model organizational changes

---

Built with ❤️ using [CrewAI](https://www.crewai.com/)

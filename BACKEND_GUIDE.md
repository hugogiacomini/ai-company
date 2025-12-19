# AI Company Backend Guide

This guide explains how to use the dual-backend architecture in the AI Company simulation.

## Table of Contents

- [Overview](#overview)
- [Available Backends](#available-backends)
- [Quick Start](#quick-start)
- [Backend Selection](#backend-selection)
- [Claude Code Subagents](#claude-code-subagents)
- [Comparison](#comparison)
- [Troubleshooting](#troubleshooting)

## Overview

The AI Company simulation supports two different backends for agent orchestration:

1. **CrewAI Backend** - Traditional sequential agent orchestration using the CrewAI framework
2. **Claude Code Backend** - Custom subagents with support for parallel execution

Both backends implement the same organizational structure (16 agents across 6 departments) and support the same workflows.

## Available Backends

### CrewAI Backend (`crewai`)

- **Framework**: CrewAI with LangChain and OpenAI
- **Execution**: Sequential task processing
- **API Required**: OpenAI API key
- **Best For**: Production workflows, stable execution, existing CrewAI users

### Claude Code Backend (`claude_code`)

- **Framework**: Claude Code custom subagents
- **Execution**: Supports parallel task execution
- **API Required**: None (runs within Claude Code environment)
- **Best For**: Development with Claude Code, parallel workflows, enhanced capabilities

## Quick Start

### Using CrewAI Backend (Default)

```python
from src.company import AICompany
from src.company.models.hierarchy import Department

# Initialize with CrewAI backend (default)
company = AICompany()

# Run a marketing workflow
result = company.run_department_workflow(
    Department.MARKETING,
    campaign_goal='product launch'
)
```

### Using Claude Code Backend

```python
from src.company import AICompany
from src.company.models.hierarchy import Department

# Initialize with Claude Code backend
company = AICompany(backend='claude_code')

# Run a marketing workflow (with parallel execution support)
result = company.run_department_workflow(
    Department.MARKETING,
    campaign_goal='product launch'
)
```

## Backend Selection

There are three ways to select the backend:

### 1. Programmatically (Recommended)

```python
# Explicit backend selection in code
company = AICompany(backend='crewai')
# or
company = AICompany(backend='claude_code')
```

### 2. Environment Variable

Set in your `.env` file:

```bash
AI_COMPANY_BACKEND=claude_code
```

Then initialize without specifying backend:

```python
company = AICompany()  # Uses backend from .env
```

### 3. Configuration File

Edit `config/company_config.yaml`:

```yaml
backend: claude_code  # or crewai
```

**Priority**: Programmatic > Environment Variable > Config File > Default (crewai)

## Claude Code Subagents

When using the Claude Code backend, 16 custom subagent files are automatically generated in `.claude/agents/`:

### Executive Level

- `ceo.md` - Chief Executive Officer
- `cto.md` - Chief Technology Officer

### Department Heads

- `head_of_marketing.md`
- `head_of_operations.md`
- `head_of_hr.md`
- `head_of_software_development.md`
- `head_of_commercial.md`

### Specialists

- Marketing: `marketing_analyst.md`, `content_marketing_expert.md`
- Operations: `operations_analyst.md`, `qa_expert.md`
- HR: `recruitment_specialist.md`, `hr_analyst.md`
- Software Dev: `senior_developer.md`, `software_developer.md`, `qa_analyst.md`
- Commercial: `sales_analyst.md`, `business_development_expert.md`

### Subagent Structure

Each subagent file contains:

- **YAML Frontmatter**: Name, description, tools, model
- **System Prompt**: Role, background, skills, work methodology

Example (`.claude/agents/ceo.md`):

```markdown
---
name: ceo
description: Lead the company to success by making strategic decisions...
tools:
  - Read
  - Glob
  - Grep
  - WebSearch
  - Task
model: sonnet
---

# Chief Executive Officer (CEO)

## Role and Background
You are the CEO of a forward-thinking AI-powered company...

## How You Work
1. **Analyze the request carefully**
2. **Delegate when appropriate**: Use the Task tool to delegate to department heads
...
```

### Tool Assignment by Role

| Role Type | Tools |
| ----------- | ------- |
| **Executives (CEO, CTO)** | Read, Glob, Grep, WebSearch, WebFetch, Task (for delegation) |
| **Department Heads** | Read, Glob, Grep, WebSearch, Task + department-specific tools |
| **Software Development** | Read, Glob, Grep, Edit, Write, Bash |
| **Marketing** | Read, Glob, Grep, WebSearch, WebFetch, Write |
| **Operations/HR/Commercial** | Read, Glob, Grep, WebSearch |

**Note**: Leaders (executives and heads) have the Task tool for delegating to team members. Specialists cannot delegate.

## Comparison

| Feature | CrewAI Backend | Claude Code Backend |
| --------- | ---------------- | --------------------- |
| **Execution Mode** | Sequential only | Sequential + Parallel |
| **API Required** | OpenAI API Key | None (runs in Claude Code) |
| **Agent Definition** | Python code | Markdown files (.md) |
| **Tool Control** | Framework-level | Per-agent granular control |
| **Delegation** | via allow_delegation flag | via Task tool |
| **Best For** | Production, stability | Development, experimentation |
| **Setup Complexity** | Simple (pip install) | Requires Claude Code |

## Workflows Supported

Both backends support all workflows:

### Department Workflows

```python
# Marketing
company.run_department_workflow(Department.MARKETING, campaign_goal='...')

# Software Development
company.run_department_workflow(Department.SOFTWARE_DEVELOPMENT, feature='...')

# Operations
company.run_department_workflow(Department.OPERATIONS, process='...')

# Human Resources
company.run_department_workflow(Department.HUMAN_RESOURCES, position='...')

# Commercial
company.run_department_workflow(Department.COMMERCIAL, product='...')

# Executive
company.run_strategic_planning('annual planning')
```

### Cross-Functional Workflows

```python
# Product Launch (4 departments)
company.run_product_launch('AI Assistant Pro')

# Quarterly Review (all departments)
company.run_quarterly_review('Q1 2025')
```

## Troubleshooting

### CrewAI Backend Issues

**Error: "OPENAI_API_KEY not found"**

- Solution: Add your OpenAI API key to `.env` file:

  ```bash
  OPENAI_API_KEY=sk-...
  ```

**Error: "No module named 'crewai'"**

- Solution: Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

### Claude Code Backend Issues

**Error: "Claude Code backend not available"**

- Solution: Ensure you're running within Claude Code environment

**Subagent files not found**

- Solution: Subagents are auto-generated when backend is initialized. Check `.claude/agents/` directory.

**Tools not working in subagents**

- Solution: Verify tool names in subagent YAML frontmatter match Claude Code tool names exactly (case-sensitive)

### General Issues

**Error: "Unknown backend type"**

- Solution: Use `'crewai'` or `'claude_code'` (lowercase)

**Backend selection not working**

- Check priority: Programmatic > Environment Variable > Config File
- Verify `.env` file is in project root
- Ensure `python-dotenv` is installed

### Switching Backends

To switch from CrewAI to Claude Code:

1. Update environment variable:

   ```bash
   # In .env file
   AI_COMPANY_BACKEND=claude_code
   ```

2. Or pass programmatically:

   ```python
   company = AICompany(backend='claude_code')
   ```

3. Verify backend:

   ```python
   print(company.backend.get_backend_type().value)
   # Output: claude_code
   ```

## Advanced Usage

### Custom Backend Configuration

Edit `config/company_config.yaml` for backend-specific settings:

```yaml
backend: claude_code

crewai:
  verbose: true
  max_iterations:
    executive: 5
    head: 5
    specialist: 3

claude_code:
  subagents_dir: .claude/agents
  model: sonnet
  parallel_execution: true
  max_parallel_tasks: 5
```

### Accessing Backend Directly

```python
# Get backend instance
backend = company.backend

# Check backend type
backend_type = backend.get_backend_type()
print(f"Using: {backend_type.value}")

# Check parallel support
if backend.supports_parallel_execution():
    print("Parallel execution available!")
```

### Creating Custom Workflows

```python
from src.company.orchestration.workflow_manager import WorkflowManager
from src.company.backends.factory import BackendFactory

# Create custom backend
backend = BackendFactory.create_backend('claude_code')
workflow_manager = WorkflowManager(backend)

# Run custom department workflow
result = workflow_manager.create_department_workflow(
    department=Department.MARKETING,
    scenario_params={
        'campaign_goal': 'brand awareness',
        'budget': '$50,000',
        'duration': '3 months'
    }
)
```

## Best Practices

1. **Development**: Use Claude Code backend for rapid iteration and parallel execution
2. **Production**: Use CrewAI backend for stability and production deployments
3. **Testing**: Test workflows on both backends to ensure compatibility
4. **Version Control**: Commit `.claude/agents/` directory to share subagents with team
5. **API Keys**: Never commit API keys - use `.env` files (excluded from git)

## Further Reading

- [Main README](README.md) - Project overview and setup
- [Quick Start Guide](QUICK_START.md) - Getting started examples
- [Architecture Documentation](ARCHITECTURE.md) - System design details
- [CrewAI Documentation](https://docs.crewai.com/) - CrewAI framework docs
- [Claude Code Documentation](https://docs.anthropic.com/claude-code/) - Claude Code docs

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section above
2. Review error messages carefully
3. Verify API keys and environment setup
4. Ensure all dependencies are installed

---

**Note**: This is an experimental dual-backend architecture. Both backends are actively maintained, but CrewAI remains the default for backward compatibility.

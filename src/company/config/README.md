# AI Company Configuration

This directory contains configuration files for different aspects of the AI Company simulation.

## Configuration Files

- Environment variables should be set in `.env` file in the root directory
- Use `.env.example` as a template

## Customizing Agents

Agents can be customized by modifying the following parameters:

- `role`: The agent's job title and role
- `goal`: What the agent is trying to achieve
- `backstory`: The agent's background and expertise
- `verbose`: Whether to show detailed logs
- `allow_delegation`: Whether the agent can delegate tasks to others
- `max_iter`: Maximum number of iterations for task completion

## Customizing Tasks

Tasks can be customized with:

- `description`: Detailed description of what needs to be done
- `agent`: The agent responsible for the task
- `expected_output`: What the deliverable should look like

## Customizing Crews

Crews can use different processes:

- `Process.sequential`: Tasks are executed one after another
- `Process.hierarchical`: Tasks follow a management hierarchy

## LLM Configuration

By default, the system uses OpenAI's GPT models. You can configure different LLMs by:

1. Setting the appropriate API keys in `.env`
2. Modifying agent configurations to use specific models

Example for using different models:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0.7)

agent = Agent(
    role="CEO",
    goal="Lead the company",
    backstory="Experienced executive",
    llm=llm
)
```

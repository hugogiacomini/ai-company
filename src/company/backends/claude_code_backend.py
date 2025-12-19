"""
Claude Code backend implementation.
Generates custom subagent .md files and orchestrates task execution via Claude Code.
"""
import os
from typing import Dict, Any, List
from pathlib import Path

from .base import BaseBackend, BackendType, AgentRole, TaskDefinition, WorkflowResult


class ClaudeCodeBackend(BaseBackend):
    """Claude Code implementation using custom subagents"""

    def __init__(self):
        self._subagents_dir = ".claude/agents"
        self._config: Dict[str, Any] = {}
        self._agent_definitions: Dict[str, Dict[str, Any]] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize Claude Code backend with configuration.

        Args:
            config: Configuration dict with 'subagents_dir', 'model', etc.
        """
        self._config = config
        self._subagents_dir = config.get('subagents_dir', '.claude/agents')
        self._ensure_subagents_directory()

    def _ensure_subagents_directory(self):
        """Ensure .claude/agents directory exists"""
        os.makedirs(self._subagents_dir, exist_ok=True)

    def create_agent(self, agent_def: AgentRole) -> str:
        """
        Create a Claude Code subagent by writing .md file.

        Args:
            agent_def: Unified agent role definition

        Returns:
            Agent role name (identifier for later use)
        """
        # Convert role to filename (e.g., "CEO" -> "ceo.md")
        filename = self._role_to_filename(agent_def.role)
        filepath = os.path.join(self._subagents_dir, filename)

        # Determine tools based on role
        tools = self._determine_tools(agent_def)

        # Build YAML frontmatter and system prompt
        content = self._build_subagent_content(agent_def, tools)

        # Write subagent file
        with open(filepath, 'w') as f:
            f.write(content)

        # Cache agent definition
        self._agent_definitions[agent_def.role] = {
            'file': filepath,
            'can_delegate': agent_def.can_delegate,
            'department': agent_def.department,
            'tools': tools
        }

        return agent_def.role

    def _role_to_filename(self, role: str) -> str:
        """
        Convert role name to filename.

        Args:
            role: Role name (e.g., "Chief Executive Officer (CEO)")

        Returns:
            Filename (e.g., "ceo.md")
        """
        # Extract acronym or simplify name
        role_lower = role.lower()

        # Common role mappings
        role_mappings = {
            "chief executive officer (ceo)": "ceo",
            "chief technology officer (cto)": "cto",
            "head of marketing": "head_of_marketing",
            "head of operations": "head_of_operations",
            "head of human resources": "head_of_hr",
            "head of hr": "head_of_hr",
            "head of software development": "head_of_software_development",
            "head of commercial": "head_of_commercial",
            "marketing analyst": "marketing_analyst",
            "content marketing expert": "content_marketing_expert",
            "operations analyst": "operations_analyst",
            "quality assurance expert": "qa_expert",
            "recruitment specialist": "recruitment_specialist",
            "hr analyst": "hr_analyst",
            "senior software developer": "senior_developer",
            "software developer": "software_developer",
            "qa analyst": "qa_analyst",
            "sales analyst": "sales_analyst",
            "business development expert": "business_development_expert"
        }

        # Use mapping or create from role name
        filename = role_mappings.get(role_lower, role_lower.replace(" ", "_"))
        return f"{filename}.md"

    def _determine_tools(self, agent_def: AgentRole) -> List[str]:
        """
        Determine which tools an agent should have access to.

        Args:
            agent_def: Agent role definition

        Returns:
            List of tool names
        """
        # Base tools for all agents
        tools = ["Read", "Glob", "Grep"]

        # Add department-specific tools
        dept = agent_def.department.lower()

        if dept == "software_development":
            tools.extend(["Bash", "Edit", "Write"])
        elif dept == "marketing":
            tools.extend(["WebSearch", "WebFetch", "Write"])
        elif dept == "operations":
            tools.extend(["Bash"])
        elif dept == "human_resources":
            tools.extend(["WebSearch"])
        elif dept == "commercial":
            tools.extend(["WebSearch", "WebFetch"])
        elif dept == "executive":
            tools.extend(["WebSearch", "WebFetch"])

        # Add delegation capability (Task tool) for leaders
        if agent_def.can_delegate:
            tools.append("Task")

        return list(set(tools))  # Remove duplicates

    def _build_subagent_content(self, agent_def: AgentRole, tools: List[str]) -> str:
        """
        Build the subagent .md file content with YAML frontmatter and system prompt.

        Args:
            agent_def: Agent role definition
            tools: List of tools for this agent

        Returns:
            Complete markdown file content
        """
        # Extract simple role name for the 'name' field
        simple_name = self._role_to_filename(agent_def.role).replace('.md', '')

        # YAML frontmatter
        tools_yaml = "\n".join(f"  - {tool}" for tool in tools)
        frontmatter = f"""---
name: {simple_name}
description: {agent_def.goal}
tools:
{tools_yaml}
model: {self._config.get('model', 'sonnet')}
---

"""

        # System prompt
        system_prompt = f"""# {agent_def.role}

## Role and Background
{agent_def.backstory}

## Primary Goal
{agent_def.goal}

## Key Skills and Expertise
{chr(10).join(f'- {skill}' for skill in agent_def.skills) if agent_def.skills else '- General business acumen'}

## How You Work

1. **Analyze the request carefully**: Understand what is being asked and what deliverable is expected.

2. **Leverage your expertise**: Apply your specialized knowledge in {agent_def.department} to provide high-quality results.

3. **Use available tools**: You have access to various tools to help you complete tasks effectively:
{chr(10).join(f'   - {tool}' for tool in tools)}
"""

        # Add delegation instructions if applicable
        if agent_def.can_delegate:
            system_prompt += """
4. **Delegate when appropriate**: As a leader, you can delegate tasks to team members using the Task tool.
   - Break complex work into smaller tasks
   - Assign tasks to appropriate specialists
   - Review and synthesize the results
   - Make final decisions based on team input

"""

        system_prompt += f"""
## Expected Output Quality

Always provide:
- Clear, actionable deliverables
- Well-structured and professional output
- Relevant insights based on your expertise
- Practical recommendations where applicable

Remember: You represent the {agent_def.role} role in this organization. Maintain professionalism and focus on delivering value that aligns with your department's objectives.
"""

        return frontmatter + system_prompt

    def create_task(self, task_def: TaskDefinition) -> Dict[str, Any]:
        """
        Create a task definition (doesn't execute yet in Claude Code backend).

        Args:
            task_def: Unified task definition

        Returns:
            Task dictionary for later execution
        """
        return {
            'description': task_def.description,
            'agent_role': task_def.agent_role,
            'expected_output': task_def.expected_output,
            'context': task_def.context,
            'depends_on': task_def.depends_on,
            'task_id': task_def.task_id
        }

    def execute_workflow(
        self,
        agents: List[str],  # Agent role names
        tasks: List[Dict[str, Any]],
        process_type: str = "sequential"
    ) -> WorkflowResult:
        """
        Execute workflow using Claude Code subagents.

        Note: In a real Claude Code environment, this would invoke subagents via the Task tool.
        For this implementation, we simulate the workflow structure.

        Args:
            agents: List of agent role names
            tasks: List of task dictionaries
            process_type: Execution mode ("sequential" or "parallel")

        Returns:
            WorkflowResult with execution results and metadata
        """
        results = {}
        task_outputs = {}

        if process_type == "parallel" and self.supports_parallel_execution():
            results = self._execute_parallel(tasks, task_outputs)
        else:
            results = self._execute_sequential(tasks, task_outputs)

        return WorkflowResult(
            success=True,
            outputs=results,
            metadata={
                "backend": "claude_code",
                "agents_count": len(agents),
                "tasks_count": len(tasks),
                "process": process_type,
                "note": "Claude Code backend - subagents defined in .claude/agents/"
            }
        )

    def _execute_sequential(
        self,
        tasks: List[Dict[str, Any]],
        task_outputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute tasks sequentially.

        In actual Claude Code, this would invoke subagents via Task tool.
        For now, this creates a workflow plan.

        Args:
            tasks: List of task dictionaries
            task_outputs: Dictionary to store task outputs

        Returns:
            Dictionary of results by agent role
        """
        results = {}

        for i, task in enumerate(tasks):
            task_id = task.get('task_id', f"task_{i}")

            # Build context from previous task outputs
            context = task.get('context', {}).copy()
            for dep_id in task.get('depends_on', []):
                if dep_id in task_outputs:
                    context[f'previous_output_{dep_id}'] = task_outputs[dep_id]

            # In real implementation, this would invoke the subagent
            # For now, create a workflow instruction
            result = self._create_workflow_instruction(task, context)

            task_outputs[task_id] = result
            results[task['agent_role']] = result

        return results

    def _execute_parallel(
        self,
        tasks: List[Dict[str, Any]],
        task_outputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute independent tasks in parallel.

        Args:
            tasks: List of task dictionaries
            task_outputs: Dictionary to store task outputs

        Returns:
            Dictionary of results by agent role
        """
        # Group tasks by dependencies
        independent_tasks = [t for t in tasks if not t.get('depends_on')]

        results = {}

        # In real implementation, would execute in parallel
        # For now, create workflow instructions for parallel execution
        for task in independent_tasks:
            result = self._create_workflow_instruction(task, task.get('context', {}))
            results[task['agent_role']] = result

        return results

    def _create_workflow_instruction(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """
        Create a workflow instruction for Claude Code subagent invocation.

        In actual use, this would be executed by invoking the subagent.

        Args:
            task: Task dictionary
            context: Context for task execution

        Returns:
            Workflow instruction string
        """
        agent_role = task['agent_role']
        description = task['description']

        instruction = f"""
[Claude Code Subagent Workflow]
Agent: @{self._role_to_filename(agent_role).replace('.md', '')}
Task: {description}
Expected Output: {task['expected_output']}
"""

        if context:
            instruction += "\nContext:\n"
            for key, value in context.items():
                instruction += f"- {key}: {value}\n"

        instruction += f"""
To execute this workflow in Claude Code, use:
> @{self._role_to_filename(agent_role).replace('.md', '')}, {description}

The subagent file has been created at: {self._subagents_dir}/{self._role_to_filename(agent_role)}
"""

        return instruction

    def supports_parallel_execution(self) -> bool:
        """
        Claude Code supports parallel task execution.

        Returns:
            True if parallel execution is enabled in config
        """
        return self._config.get('parallel_execution', True)

    def get_backend_type(self) -> BackendType:
        """
        Return the backend type.

        Returns:
            BackendType.CLAUDE_CODE
        """
        return BackendType.CLAUDE_CODE

    def cleanup(self) -> None:
        """Clean up cached agent definitions"""
        self._agent_definitions.clear()

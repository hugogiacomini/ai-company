"""
Workflow manager for orchestrating multi-agent workflows.
Coordinates agent and task creation across different backends.
"""
from typing import Dict, List, Any, Optional
from ..backends.base import BaseBackend, AgentRole, TaskDefinition
from ..models.hierarchy import OrganizationalChart, Department, Role
from .context_manager import ContextManager


class WorkflowManager:
    """
    Manages multi-agent workflows across different backends.

    Handles:
    - Converting organizational roles to agent definitions
    - Creating department-specific workflows
    - Creating cross-functional workflows
    - Managing context between tasks
    """

    def __init__(self, backend: BaseBackend):
        """
        Initialize workflow manager with a backend.

        Args:
            backend: Backend instance to use for workflow execution
        """
        self.backend = backend
        self.org_chart = OrganizationalChart()
        self.context_manager = ContextManager()

    def create_department_workflow(
        self,
        department: Department,
        scenario_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create and execute a department-specific workflow.

        Args:
            department: Department to run workflow for
            scenario_params: Parameters for the workflow scenario

        Returns:
            Dictionary with workflow results
        """
        # Get roles for department
        roles = self.org_chart.get_roles_by_department(department)

        # Create agents
        agents = []
        for role in roles:
            agent_def = self._role_to_agent_def(role)
            agent = self.backend.create_agent(agent_def)
            agents.append(agent)

        # Create tasks based on department and scenario
        tasks = self._create_department_tasks(department, roles, scenario_params)

        # Set workflow metadata
        self.context_manager.set_workflow_metadata({
            'department': department.value,
            'scenario': scenario_params
        })

        # Execute workflow
        process_type = "parallel" if self.backend.supports_parallel_execution() else "sequential"
        result = self.backend.execute_workflow(agents, tasks, process_type)

        # Clear context for next workflow
        self.context_manager.clear()

        return result.outputs

    def create_cross_functional_workflow(
        self,
        departments: List[Department],
        scenario_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create and execute a cross-functional workflow involving multiple departments.

        Args:
            departments: List of departments to involve
            scenario_params: Parameters for the workflow scenario

        Returns:
            Dictionary with workflow results
        """
        # Get department heads for each department
        agents = []
        roles = []

        for department in departments:
            dept_roles = self.org_chart.get_roles_by_department(department)
            # Find the head of department
            head = next((r for r in dept_roles if r.level.value == "head"), None)
            if head:
                agent_def = self._role_to_agent_def(head)
                agent = self.backend.create_agent(agent_def)
                agents.append(agent)
                roles.append(head)

        # Create cross-functional tasks
        tasks = self._create_cross_functional_tasks(roles, scenario_params)

        # Set workflow metadata
        self.context_manager.set_workflow_metadata({
            'type': 'cross_functional',
            'departments': [d.value for d in departments],
            'scenario': scenario_params
        })

        # Execute workflow (usually sequential for cross-functional)
        result = self.backend.execute_workflow(agents, tasks, "sequential")

        # Clear context
        self.context_manager.clear()

        return result.outputs

    def _role_to_agent_def(self, role: Role) -> AgentRole:
        """
        Convert organizational role to agent definition.

        Args:
            role: Organizational role from hierarchy

        Returns:
            AgentRole definition for backend
        """
        # Build goal from responsibilities
        goal = " ".join(role.responsibilities[:2]) if role.responsibilities else f"Contribute to {role.department.value} success"

        # Build backstory
        backstory = self._generate_backstory(role)

        return AgentRole(
            role=role.title,
            goal=goal,
            backstory=backstory,
            department=role.department.value,
            level=role.level.value,
            can_delegate=role.level.value in ["executive", "head"],
            skills=role.skills
        )

    def _generate_backstory(self, role: Role) -> str:
        """
        Generate agent backstory from organizational role.

        Args:
            role: Organizational role

        Returns:
            Backstory string
        """
        level_descriptions = {
            "executive": "senior leadership",
            "head": "department leadership",
            "senior": "senior-level expertise",
            "expert": "specialized expertise",
            "developer": "software development",
            "analyst": "analytical expertise"
        }

        level_desc = level_descriptions.get(role.level.value, "professional expertise")
        skills_str = ", ".join(role.skills[:3]) if len(role.skills) >= 3 else ", ".join(role.skills)

        return f"""You are the {role.title} with {level_desc} in {role.department.value}.
        Your expertise includes: {skills_str}.
        Your key responsibilities: {', '.join(role.responsibilities[:2]) if role.responsibilities else 'supporting the organization'}.
        You report to {role.reports_to if role.reports_to else 'the board'} and are committed to excellence."""

    def _create_department_tasks(
        self,
        department: Department,
        roles: List[Role],
        params: Dict[str, Any]
    ) -> List[Any]:
        """
        Create tasks for a department workflow.

        Args:
            department: Department for workflow
            roles: List of roles in department
            params: Scenario parameters

        Returns:
            List of backend-specific task objects
        """
        tasks = []

        # Common task patterns by department
        if department == Department.MARKETING:
            tasks = self._create_marketing_tasks(roles, params)
        elif department == Department.SOFTWARE_DEVELOPMENT:
            tasks = self._create_software_tasks(roles, params)
        elif department == Department.OPERATIONS:
            tasks = self._create_operations_tasks(roles, params)
        elif department == Department.HUMAN_RESOURCES:
            tasks = self._create_hr_tasks(roles, params)
        elif department == Department.COMMERCIAL:
            tasks = self._create_commercial_tasks(roles, params)
        elif department == Department.EXECUTIVE:
            tasks = self._create_executive_tasks(roles, params)

        return tasks

    def _create_marketing_tasks(self, roles: List[Role], params: Dict[str, Any]) -> List[Any]:
        """Create marketing department tasks"""
        tasks = []
        campaign_goal = params.get('campaign_goal', 'brand awareness campaign')

        # Task 1: Analyst analyzes market
        if any(r.title == "Marketing Analyst" for r in roles):
            task_def = TaskDefinition(
                description=f"Analyze market trends and target audience for {campaign_goal}",
                agent_role="Marketing Analyst",
                expected_output="Market analysis report with target audience insights"
            )
            tasks.append(self.backend.create_task(task_def))

        # Task 2: Content Expert creates content strategy
        if any(r.title == "Content Marketing Expert" for r in roles):
            task_def = TaskDefinition(
                description=f"Develop content strategy for {campaign_goal}",
                agent_role="Content Marketing Expert",
                expected_output="Content strategy with key messages and channels"
            )
            tasks.append(self.backend.create_task(task_def))

        # Task 3: Head approves and finalizes
        if any(r.title == "Head of Marketing" for r in roles):
            task_def = TaskDefinition(
                description=f"Review team inputs and create final campaign plan for {campaign_goal}",
                agent_role="Head of Marketing",
                expected_output="Complete campaign plan with budget and timeline"
            )
            tasks.append(self.backend.create_task(task_def))

        return tasks

    def _create_software_tasks(self, roles: List[Role], params: Dict[str, Any]) -> List[Any]:
        """Create software development department tasks"""
        tasks = []
        feature = params.get('feature', 'new feature')

        # Task 1: Head plans architecture
        if any(r.title == "Head of Software Development" for r in roles):
            task_def = TaskDefinition(
                description=f"Design technical architecture for {feature}",
                agent_role="Head of Software Development",
                expected_output="Architecture design and implementation plan"
            )
            tasks.append(self.backend.create_task(task_def))

        # Task 2: Senior developer implements core
        if any(r.title == "Senior Software Developer" for r in roles):
            task_def = TaskDefinition(
                description=f"Implement core functionality for {feature}",
                agent_role="Senior Software Developer",
                expected_output="Core implementation with tests"
            )
            tasks.append(self.backend.create_task(task_def))

        # Task 3: QA tests
        if any(r.title == "QA Analyst" for r in roles):
            task_def = TaskDefinition(
                description=f"Create test plan and test {feature}",
                agent_role="QA Analyst",
                expected_output="Test results and quality report"
            )
            tasks.append(self.backend.create_task(task_def))

        return tasks

    def _create_operations_tasks(self, roles: List[Role], params: Dict[str, Any]) -> List[Any]:
        """Create operations department tasks"""
        tasks = []
        process = params.get('process', 'business process')

        if any(r.title == "Operations Analyst" for r in roles):
            task_def = TaskDefinition(
                description=f"Analyze current {process} and identify improvement opportunities",
                agent_role="Operations Analyst",
                expected_output="Process analysis with improvement recommendations"
            )
            tasks.append(self.backend.create_task(task_def))

        if any(r.title == "Head of Operations" for r in roles):
            task_def = TaskDefinition(
                description=f"Review analysis and create optimization plan for {process}",
                agent_role="Head of Operations",
                expected_output="Process optimization plan with implementation steps"
            )
            tasks.append(self.backend.create_task(task_def))

        return tasks

    def _create_hr_tasks(self, roles: List[Role], params: Dict[str, Any]) -> List[Any]:
        """Create HR department tasks"""
        tasks = []
        position = params.get('position', 'key position')

        if any(r.title == "Recruitment Specialist" for r in roles):
            task_def = TaskDefinition(
                description=f"Develop recruitment strategy for {position}",
                agent_role="Recruitment Specialist",
                expected_output="Recruitment plan with sourcing channels and timeline"
            )
            tasks.append(self.backend.create_task(task_def))

        if any(r.title == "Head of Human Resources" for r in roles):
            task_def = TaskDefinition(
                description=f"Review recruitment plan and finalize hiring strategy for {position}",
                agent_role="Head of Human Resources",
                expected_output="Complete hiring strategy with budget and success metrics"
            )
            tasks.append(self.backend.create_task(task_def))

        return tasks

    def _create_commercial_tasks(self, roles: List[Role], params: Dict[str, Any]) -> List[Any]:
        """Create commercial department tasks"""
        tasks = []
        product = params.get('product', 'product')

        if any(r.title == "Sales Analyst" for r in roles):
            task_def = TaskDefinition(
                description=f"Analyze sales potential and forecast for {product}",
                agent_role="Sales Analyst",
                expected_output="Sales forecast and market potential analysis"
            )
            tasks.append(self.backend.create_task(task_def))

        if any(r.title == "Head of Commercial" for r in roles):
            task_def = TaskDefinition(
                description=f"Develop sales strategy for {product} based on analysis",
                agent_role="Head of Commercial",
                expected_output="Complete sales strategy with targets and tactics"
            )
            tasks.append(self.backend.create_task(task_def))

        return tasks

    def _create_executive_tasks(self, roles: List[Role], params: Dict[str, Any]) -> List[Any]:
        """Create executive department tasks"""
        tasks = []
        scenario = params.get('scenario', 'strategic initiative')

        if any(r.title == "CTO" for r in roles):
            task_def = TaskDefinition(
                description=f"Assess technical feasibility and requirements for {scenario}",
                agent_role="CTO",
                expected_output="Technical assessment with recommendations"
            )
            tasks.append(self.backend.create_task(task_def))

        if any(r.title == "CEO" for r in roles):
            task_def = TaskDefinition(
                description=f"Review inputs and make strategic decision on {scenario}",
                agent_role="CEO",
                expected_output="Strategic decision with implementation roadmap"
            )
            tasks.append(self.backend.create_task(task_def))

        return tasks

    def _create_cross_functional_tasks(
        self,
        roles: List[Role],
        params: Dict[str, Any]
    ) -> List[Any]:
        """
        Create tasks for cross-functional workflows.

        Args:
            roles: List of roles involved (usually department heads)
            params: Scenario parameters

        Returns:
            List of backend-specific task objects
        """
        tasks = []
        initiative = params.get('initiative', 'company initiative')

        # Each department head provides input
        for role in roles:
            task_def = TaskDefinition(
                description=f"Provide {role.department.value} perspective and recommendations for {initiative}",
                agent_role=role.title,
                expected_output=f"{role.department.value} analysis and recommendations"
            )
            tasks.append(self.backend.create_task(task_def))

        return tasks

"""
AI Company - A simulation of a real software development company using CrewAI framework.

This package provides a complete organizational structure with agents representing
different roles across departments like Marketing, Operations, HR, Software Development,
and Commercial, following a proper hierarchy with CEO, CTO, Department Heads, and specialists.
"""

from .company import AICompany
from .models.hierarchy import Department, RoleLevel, OrganizationalChart
from .agents.company_agents import CompanyAgents
from .tasks.company_tasks import CompanyTasks
from .crews.company_crews import CompanyCrews

__version__ = "0.1.0"

__all__ = [
    "AICompany",
    "Department",
    "RoleLevel",
    "OrganizationalChart",
    "CompanyAgents",
    "CompanyTasks",
    "CompanyCrews",
]

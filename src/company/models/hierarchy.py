"""
Organizational hierarchy models for the AI Company.
Defines the structure of roles and departments.
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class RoleLevel(str, Enum):
    """Hierarchy levels in the organization"""
    EXECUTIVE = "executive"  # CEO, CTO
    HEAD = "head"  # Department Heads
    SENIOR = "senior"  # Senior Experts
    EXPERT = "expert"  # Specialists
    DEVELOPER = "developer"  # Developers
    ANALYST = "analyst"  # Analysts
    JUNIOR = "junior"  # Junior staff


class Department(str, Enum):
    """Company departments"""
    EXECUTIVE = "executive"
    MARKETING = "marketing"
    OPERATIONS = "operations"
    HUMAN_RESOURCES = "human_resources"
    SOFTWARE_DEVELOPMENT = "software_development"
    COMMERCIAL = "commercial"


class Role(BaseModel):
    """Represents a role in the organization"""
    title: str = Field(description="Job title")
    level: RoleLevel = Field(description="Hierarchy level")
    department: Department = Field(description="Department")
    reports_to: Optional[str] = Field(None, description="Title of supervisor")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities")
    skills: List[str] = Field(default_factory=list, description="Required skills")


class OrganizationalChart:
    """Defines the complete organizational structure"""
    
    @staticmethod
    def get_hierarchy() -> List[Role]:
        """Returns the complete organizational hierarchy"""
        return [
            # Executive Level
            Role(
                title="CEO",
                level=RoleLevel.EXECUTIVE,
                department=Department.EXECUTIVE,
                reports_to=None,
                responsibilities=[
                    "Define company vision and strategy",
                    "Oversee all departments",
                    "Make final decisions on major initiatives",
                    "Ensure company goals are met"
                ],
                skills=["strategic planning", "leadership", "decision making", "business development"]
            ),
            Role(
                title="CTO",
                level=RoleLevel.EXECUTIVE,
                department=Department.EXECUTIVE,
                reports_to="CEO",
                responsibilities=[
                    "Lead technology strategy",
                    "Oversee Software Development department",
                    "Ensure technical excellence",
                    "Drive innovation"
                ],
                skills=["technical leadership", "architecture", "innovation", "team management"]
            ),
            
            # Department Heads
            Role(
                title="Head of Marketing",
                level=RoleLevel.HEAD,
                department=Department.MARKETING,
                reports_to="CEO",
                responsibilities=[
                    "Develop marketing strategy",
                    "Lead marketing campaigns",
                    "Manage brand reputation",
                    "Oversee marketing team"
                ],
                skills=["marketing strategy", "brand management", "campaign planning", "analytics"]
            ),
            Role(
                title="Head of Operations",
                level=RoleLevel.HEAD,
                department=Department.OPERATIONS,
                reports_to="CEO",
                responsibilities=[
                    "Optimize business processes",
                    "Manage operational efficiency",
                    "Ensure quality standards",
                    "Coordinate cross-department operations"
                ],
                skills=["process optimization", "project management", "quality assurance", "logistics"]
            ),
            Role(
                title="Head of HR",
                level=RoleLevel.HEAD,
                department=Department.HUMAN_RESOURCES,
                reports_to="CEO",
                responsibilities=[
                    "Manage recruitment and hiring",
                    "Develop employee programs",
                    "Handle employee relations",
                    "Foster company culture"
                ],
                skills=["recruitment", "employee relations", "training", "organizational development"]
            ),
            Role(
                title="Head of Software Development",
                level=RoleLevel.HEAD,
                department=Department.SOFTWARE_DEVELOPMENT,
                reports_to="CTO",
                responsibilities=[
                    "Lead development teams",
                    "Ensure code quality",
                    "Plan technical roadmap",
                    "Coordinate with other departments"
                ],
                skills=["software architecture", "team leadership", "agile methodology", "code review"]
            ),
            Role(
                title="Head of Commercial",
                level=RoleLevel.HEAD,
                department=Department.COMMERCIAL,
                reports_to="CEO",
                responsibilities=[
                    "Drive sales strategy",
                    "Manage client relationships",
                    "Negotiate contracts",
                    "Meet revenue targets"
                ],
                skills=["sales strategy", "negotiation", "client relations", "revenue management"]
            ),
            
            # Marketing Department
            Role(
                title="Marketing Analyst",
                level=RoleLevel.ANALYST,
                department=Department.MARKETING,
                reports_to="Head of Marketing",
                responsibilities=[
                    "Analyze market trends",
                    "Track campaign performance",
                    "Provide data-driven insights",
                    "Monitor competitor activities"
                ],
                skills=["data analysis", "market research", "reporting", "analytics tools"]
            ),
            Role(
                title="Content Marketing Expert",
                level=RoleLevel.EXPERT,
                department=Department.MARKETING,
                reports_to="Head of Marketing",
                responsibilities=[
                    "Create marketing content",
                    "Develop content strategy",
                    "Manage content calendar",
                    "Ensure brand consistency"
                ],
                skills=["content creation", "copywriting", "SEO", "content strategy"]
            ),
            
            # Operations Department
            Role(
                title="Operations Analyst",
                level=RoleLevel.ANALYST,
                department=Department.OPERATIONS,
                reports_to="Head of Operations",
                responsibilities=[
                    "Analyze operational metrics",
                    "Identify process improvements",
                    "Generate operational reports",
                    "Track KPIs"
                ],
                skills=["process analysis", "data analytics", "reporting", "efficiency optimization"]
            ),
            Role(
                title="Quality Assurance Expert",
                level=RoleLevel.EXPERT,
                department=Department.OPERATIONS,
                reports_to="Head of Operations",
                responsibilities=[
                    "Ensure quality standards",
                    "Conduct quality audits",
                    "Develop QA processes",
                    "Train teams on quality practices"
                ],
                skills=["quality assurance", "testing", "process improvement", "documentation"]
            ),
            
            # HR Department
            Role(
                title="Recruitment Specialist",
                level=RoleLevel.EXPERT,
                department=Department.HUMAN_RESOURCES,
                reports_to="Head of HR",
                responsibilities=[
                    "Source and recruit candidates",
                    "Conduct interviews",
                    "Manage hiring process",
                    "Build talent pipeline"
                ],
                skills=["recruitment", "interviewing", "talent sourcing", "candidate assessment"]
            ),
            Role(
                title="HR Analyst",
                level=RoleLevel.ANALYST,
                department=Department.HUMAN_RESOURCES,
                reports_to="Head of HR",
                responsibilities=[
                    "Analyze HR metrics",
                    "Track employee satisfaction",
                    "Prepare HR reports",
                    "Monitor retention rates"
                ],
                skills=["HR analytics", "reporting", "data analysis", "employee engagement"]
            ),
            
            # Software Development Department
            Role(
                title="Senior Software Developer",
                level=RoleLevel.SENIOR,
                department=Department.SOFTWARE_DEVELOPMENT,
                reports_to="Head of Software Development",
                responsibilities=[
                    "Design and develop software",
                    "Review code from junior developers",
                    "Mentor development team",
                    "Ensure best practices"
                ],
                skills=["software development", "code review", "mentoring", "architecture design"]
            ),
            Role(
                title="Software Developer",
                level=RoleLevel.DEVELOPER,
                department=Department.SOFTWARE_DEVELOPMENT,
                reports_to="Head of Software Development",
                responsibilities=[
                    "Write clean, efficient code",
                    "Implement features",
                    "Fix bugs",
                    "Collaborate with team"
                ],
                skills=["programming", "problem solving", "testing", "version control"]
            ),
            Role(
                title="QA Analyst",
                level=RoleLevel.ANALYST,
                department=Department.SOFTWARE_DEVELOPMENT,
                reports_to="Head of Software Development",
                responsibilities=[
                    "Test software quality",
                    "Write test cases",
                    "Report bugs",
                    "Ensure product quality"
                ],
                skills=["testing", "bug tracking", "test automation", "quality metrics"]
            ),
            
            # Commercial Department
            Role(
                title="Sales Analyst",
                level=RoleLevel.ANALYST,
                department=Department.COMMERCIAL,
                reports_to="Head of Commercial",
                responsibilities=[
                    "Analyze sales data",
                    "Track sales performance",
                    "Forecast revenue",
                    "Generate sales reports"
                ],
                skills=["sales analytics", "forecasting", "reporting", "CRM tools"]
            ),
            Role(
                title="Business Development Expert",
                level=RoleLevel.EXPERT,
                department=Department.COMMERCIAL,
                reports_to="Head of Commercial",
                responsibilities=[
                    "Identify business opportunities",
                    "Develop partnerships",
                    "Expand market presence",
                    "Drive revenue growth"
                ],
                skills=["business development", "networking", "negotiation", "market analysis"]
            ),
        ]
    
    @staticmethod
    def get_roles_by_department(department: Department) -> List[Role]:
        """Get all roles in a specific department"""
        return [role for role in OrganizationalChart.get_hierarchy() 
                if role.department == department]
    
    @staticmethod
    def get_roles_by_level(level: RoleLevel) -> List[Role]:
        """Get all roles at a specific hierarchy level"""
        return [role for role in OrganizationalChart.get_hierarchy() 
                if role.level == level]

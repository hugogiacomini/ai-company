"""
Main AI Company orchestration.
This module provides the main interface for running company simulations.
"""
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from .models.hierarchy import Department, OrganizationalChart
from .agents.company_agents import CompanyAgents
from .tasks.company_tasks import CompanyTasks
from .crews.company_crews import CompanyCrews


class AICompany:
    """
    Main class for the AI Company simulation.
    Orchestrates agents, tasks, and crews to simulate a real company.
    """
    
    def __init__(self, company_name: str = "AI Company Inc."):
        """
        Initialize the AI Company.
        
        Args:
            company_name: Name of the company
        """
        load_dotenv()
        self.company_name = company_name
        self._validate_environment()
        
    def _validate_environment(self):
        """Validate that required environment variables are set"""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY not found in environment. "
                "Please set it in .env file or environment variables."
            )
    
    def display_organizational_chart(self):
        """Display the complete organizational hierarchy"""
        print(f"\n{'='*80}")
        print(f"ORGANIZATIONAL CHART - {self.company_name}")
        print(f"{'='*80}\n")
        
        hierarchy = OrganizationalChart.get_hierarchy()
        
        # Group by department
        departments = {}
        for role in hierarchy:
            dept = role.department.value
            if dept not in departments:
                departments[dept] = []
            departments[dept].append(role)
        
        # Display by department
        for dept_name, roles in departments.items():
            print(f"\n{dept_name.upper().replace('_', ' ')} DEPARTMENT")
            print("-" * 60)
            
            # Sort by hierarchy level
            level_order = ["executive", "head", "senior", "expert", "developer", "analyst", "junior"]
            roles.sort(key=lambda r: level_order.index(r.level.value) if r.level.value in level_order else 999)
            
            for role in roles:
                reports_to = f" (Reports to: {role.reports_to})" if role.reports_to else ""
                print(f"  • {role.title} [{role.level.value}]{reports_to}")
                if role.responsibilities:
                    print(f"    Responsibilities: {', '.join(role.responsibilities[:2])}")
        
        print(f"\n{'='*80}\n")
    
    def run_department_workflow(
        self, 
        department: Department, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run a workflow for a specific department.
        
        Args:
            department: The department to run
            **kwargs: Additional parameters for the crew
            
        Returns:
            Dictionary with workflow results
        """
        print(f"\n{'='*80}")
        print(f"RUNNING {department.value.upper().replace('_', ' ')} DEPARTMENT WORKFLOW")
        print(f"{'='*80}\n")
        
        crew = CompanyCrews.get_crew_by_department(department, **kwargs)
        result = crew.kickoff()
        
        print(f"\n{'='*80}")
        print(f"WORKFLOW COMPLETED")
        print(f"{'='*80}\n")
        
        return {
            "department": department.value,
            "result": result,
            "agents_count": len(crew.agents),
            "tasks_count": len(crew.tasks)
        }
    
    def run_product_launch(self, product_name: str) -> Dict[str, Any]:
        """
        Run a cross-functional product launch scenario.
        
        Args:
            product_name: Name of the product to launch
            
        Returns:
            Dictionary with launch results
        """
        print(f"\n{'='*80}")
        print(f"PRODUCT LAUNCH: {product_name}")
        print(f"{'='*80}\n")
        
        crew = CompanyCrews.create_product_launch_crew(product_name)
        result = crew.kickoff()
        
        print(f"\n{'='*80}")
        print(f"PRODUCT LAUNCH COMPLETED")
        print(f"{'='*80}\n")
        
        return {
            "product": product_name,
            "result": result,
            "departments_involved": len(crew.agents)
        }
    
    def run_quarterly_review(self, quarter: str) -> Dict[str, Any]:
        """
        Run a quarterly review across all departments.
        
        Args:
            quarter: The quarter to review (e.g., "Q1 2024")
            
        Returns:
            Dictionary with review results
        """
        print(f"\n{'='*80}")
        print(f"QUARTERLY REVIEW: {quarter}")
        print(f"{'='*80}\n")
        
        crew = CompanyCrews.create_quarterly_review_crew(quarter)
        result = crew.kickoff()
        
        print(f"\n{'='*80}")
        print(f"QUARTERLY REVIEW COMPLETED")
        print(f"{'='*80}\n")
        
        return {
            "quarter": quarter,
            "result": result,
            "departments_reviewed": len(crew.agents)
        }
    
    def run_strategic_planning(self, scenario: str = "annual planning") -> Dict[str, Any]:
        """
        Run an executive strategic planning session.
        
        Args:
            scenario: The planning scenario
            
        Returns:
            Dictionary with planning results
        """
        print(f"\n{'='*80}")
        print(f"STRATEGIC PLANNING SESSION")
        print(f"{'='*80}\n")
        
        crew = CompanyCrews.create_executive_crew(scenario)
        result = crew.kickoff()
        
        print(f"\n{'='*80}")
        print(f"STRATEGIC PLANNING COMPLETED")
        print(f"{'='*80}\n")
        
        return {
            "scenario": scenario,
            "result": result
        }
    
    def list_available_departments(self):
        """List all available departments"""
        print(f"\nAvailable Departments in {self.company_name}:")
        print("-" * 60)
        for dept in Department:
            roles_count = len(OrganizationalChart.get_roles_by_department(dept))
            print(f"  • {dept.value.replace('_', ' ').title()} ({roles_count} roles)")
        print()


def main():
    """Main entry point for the AI Company simulation"""
    print("\n" + "="*80)
    print("WELCOME TO AI COMPANY SIMULATION")
    print("Powered by CrewAI Framework")
    print("="*80 + "\n")
    
    # Initialize the company
    company = AICompany("AI Company Inc.")
    
    # Display organizational chart
    company.display_organizational_chart()
    
    # List available departments
    company.list_available_departments()
    
    print("\nAI Company simulation initialized successfully!")
    print("Use the AICompany class to run various workflows and scenarios.")
    print("\nExample usage:")
    print("  company = AICompany()")
    print("  company.run_department_workflow(Department.MARKETING, campaign_goal='product launch')")
    print("  company.run_product_launch('AI Assistant Pro')")
    print("  company.run_quarterly_review('Q4 2024')")
    print()


if __name__ == "__main__":
    main()

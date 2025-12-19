"""
Crew configurations for the AI Company.
Each crew represents a department or cross-functional team.
"""
from crewai import Crew, Process
from typing import List, Dict
from ..agents.company_agents import CompanyAgents
from ..tasks.company_tasks import CompanyTasks
from ..models.hierarchy import Department


class CompanyCrews:
    """Factory class for creating department crews"""
    
    @staticmethod
    def create_executive_crew(scenario: str = "strategic planning") -> Crew:
        """Create the executive leadership crew"""
        agents = CompanyAgents()
        tasks = CompanyTasks()
        
        ceo = agents.create_ceo()
        cto = agents.create_cto()
        
        # Create tasks based on scenario
        ceo_task = tasks.create_strategic_planning_task(ceo, scenario)
        cto_task = tasks.create_technology_roadmap_task(cto, scenario)
        
        return Crew(
            agents=[ceo, cto],
            tasks=[ceo_task, cto_task],
            process=Process.sequential,
            verbose=True
        )
    
    @staticmethod
    def create_marketing_crew(campaign_goal: str = "brand awareness") -> Crew:
        """Create the marketing department crew"""
        agents = CompanyAgents()
        tasks = CompanyTasks()
        
        head = agents.create_head_of_marketing()
        analyst = agents.create_marketing_analyst()
        content_expert = agents.create_content_marketing_expert()
        
        # Create coordinated tasks
        analysis_task = tasks.create_market_analysis_task(analyst, "target market")
        campaign_task = tasks.create_marketing_campaign_task(head, campaign_goal)
        content_task = tasks.create_content_creation_task(
            content_expert, 
            "blog post", 
            "related to the campaign"
        )
        
        return Crew(
            agents=[head, analyst, content_expert],
            tasks=[analysis_task, campaign_task, content_task],
            process=Process.sequential,
            verbose=True
        )
    
    @staticmethod
    def create_operations_crew(focus: str = "process optimization") -> Crew:
        """Create the operations department crew"""
        agents = CompanyAgents()
        tasks = CompanyTasks()
        
        head = agents.create_head_of_operations()
        analyst = agents.create_operations_analyst()
        qa_expert = agents.create_qa_expert()
        
        # Create operational tasks
        analysis_task = tasks.create_process_optimization_task(analyst, "key business process")
        audit_task = tasks.create_quality_audit_task(qa_expert, focus)
        
        return Crew(
            agents=[head, analyst, qa_expert],
            tasks=[analysis_task, audit_task],
            process=Process.sequential,
            verbose=True
        )
    
    @staticmethod
    def create_hr_crew(focus: str = "talent acquisition") -> Crew:
        """Create the HR department crew"""
        agents = CompanyAgents()
        tasks = CompanyTasks()
        
        head = agents.create_head_of_hr()
        recruiter = agents.create_recruitment_specialist()
        analyst = agents.create_hr_analyst()
        
        # Create HR tasks
        if "recruitment" in focus.lower() or "talent" in focus.lower():
            recruitment_task = tasks.create_recruitment_task(
                recruiter, 
                "Software Developer", 
                "3+ years experience in Python and AI"
            )
            engagement_task = tasks.create_employee_engagement_task(analyst, "onboarding")
            task_list = [recruitment_task, engagement_task]
        else:
            engagement_task = tasks.create_employee_engagement_task(analyst, focus)
            task_list = [engagement_task]
        
        return Crew(
            agents=[head, recruiter, analyst],
            tasks=task_list,
            process=Process.sequential,
            verbose=True
        )
    
    @staticmethod
    def create_software_development_crew(feature: str = "new API endpoint") -> Crew:
        """Create the software development department crew"""
        agents = CompanyAgents()
        tasks = CompanyTasks()
        
        head = agents.create_head_of_software_development()
        senior_dev = agents.create_senior_developer()
        developer = agents.create_software_developer()
        qa = agents.create_qa_analyst()
        
        # Create development workflow tasks
        dev_task = tasks.create_feature_development_task(senior_dev, feature)
        review_task = tasks.create_code_review_task(head, feature)
        test_task = tasks.create_testing_task(qa, feature)
        
        return Crew(
            agents=[head, senior_dev, developer, qa],
            tasks=[dev_task, review_task, test_task],
            process=Process.sequential,
            verbose=True
        )
    
    @staticmethod
    def create_commercial_crew(target: str = "enterprise clients") -> Crew:
        """Create the commercial department crew"""
        agents = CompanyAgents()
        tasks = CompanyTasks()
        
        head = agents.create_head_of_commercial()
        analyst = agents.create_sales_analyst()
        bd_expert = agents.create_business_development_expert()
        
        # Create commercial tasks
        analysis_task = tasks.create_sales_analysis_task(analyst, "quarterly")
        strategy_task = tasks.create_sales_strategy_task(head, target)
        bd_task = tasks.create_business_development_task(
            bd_expert, 
            f"partnership opportunities in {target} market"
        )
        
        return Crew(
            agents=[head, analyst, bd_expert],
            tasks=[analysis_task, strategy_task, bd_task],
            process=Process.sequential,
            verbose=True
        )
    
    @staticmethod
    def create_product_launch_crew(product_name: str) -> Crew:
        """Create a cross-functional product launch crew"""
        agents = CompanyAgents()
        tasks = CompanyTasks()
        
        # Cross-functional team
        ceo = agents.create_ceo()
        cto = agents.create_cto()
        marketing_head = agents.create_head_of_marketing()
        dev_head = agents.create_head_of_software_development()
        commercial_head = agents.create_head_of_commercial()
        
        # Department-specific launch tasks
        exec_task = tasks.create_product_launch_task(ceo, product_name)
        tech_task = tasks.create_product_launch_task(cto, product_name)
        marketing_task = tasks.create_product_launch_task(marketing_head, product_name)
        dev_task = tasks.create_product_launch_task(dev_head, product_name)
        sales_task = tasks.create_product_launch_task(commercial_head, product_name)
        
        return Crew(
            agents=[ceo, cto, marketing_head, dev_head, commercial_head],
            tasks=[tech_task, dev_task, marketing_task, sales_task, exec_task],
            process=Process.sequential,
            verbose=True
        )
    
    @staticmethod
    def create_quarterly_review_crew(quarter: str) -> Crew:
        """Create a cross-functional quarterly review crew"""
        agents = CompanyAgents()
        tasks = CompanyTasks()
        
        # All department heads
        ceo = agents.create_ceo()
        marketing_head = agents.create_head_of_marketing()
        ops_head = agents.create_head_of_operations()
        hr_head = agents.create_head_of_hr()
        dev_head = agents.create_head_of_software_development()
        commercial_head = agents.create_head_of_commercial()
        
        # Review tasks from each department
        marketing_review = tasks.create_quarterly_review_task(marketing_head, quarter)
        ops_review = tasks.create_quarterly_review_task(ops_head, quarter)
        hr_review = tasks.create_quarterly_review_task(hr_head, quarter)
        dev_review = tasks.create_quarterly_review_task(dev_head, quarter)
        commercial_review = tasks.create_quarterly_review_task(commercial_head, quarter)
        exec_review = tasks.create_quarterly_review_task(ceo, quarter)
        
        return Crew(
            agents=[ceo, marketing_head, ops_head, hr_head, dev_head, commercial_head],
            tasks=[marketing_review, ops_review, hr_review, dev_review, commercial_review, exec_review],
            process=Process.sequential,
            verbose=True
        )
    
    @staticmethod
    def get_crew_by_department(department: Department, **kwargs) -> Crew:
        """Get a crew for a specific department with optional parameters"""
        crew_mapping = {
            Department.EXECUTIVE: CompanyCrews.create_executive_crew,
            Department.MARKETING: CompanyCrews.create_marketing_crew,
            Department.OPERATIONS: CompanyCrews.create_operations_crew,
            Department.HUMAN_RESOURCES: CompanyCrews.create_hr_crew,
            Department.SOFTWARE_DEVELOPMENT: CompanyCrews.create_software_development_crew,
            Department.COMMERCIAL: CompanyCrews.create_commercial_crew,
        }
        
        crew_factory = crew_mapping.get(department)
        if crew_factory:
            return crew_factory(**kwargs)
        else:
            raise ValueError(f"No crew defined for department: {department}")

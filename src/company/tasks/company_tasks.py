"""
Task configurations for the AI Company.
Defines tasks that agents will perform based on different scenarios.
"""
from crewai import Task
from typing import List


class CompanyTasks:
    """Factory class for creating company tasks"""
    
    # Strategic Planning Tasks
    
    @staticmethod
    def create_strategic_planning_task(agent, context: str = "") -> Task:
        """Create a strategic planning task for executives"""
        return Task(
            description=f"""Develop a comprehensive strategic plan for the company.
            
            Consider the following:
            - Company vision and mission
            - Market opportunities and threats
            - Competitive landscape
            - Resource allocation
            - Key performance indicators
            
            Context: {context if context else 'General strategic planning'}
            
            Provide a detailed strategic plan with actionable recommendations.""",
            agent=agent,
            expected_output="A comprehensive strategic plan document with vision, goals, and action items"
        )
    
    @staticmethod
    def create_technology_roadmap_task(agent, context: str = "") -> Task:
        """Create a technology roadmap task"""
        return Task(
            description=f"""Develop a technology roadmap for the company.
            
            Address:
            - Current technology stack assessment
            - Future technology needs
            - Innovation opportunities
            - Technical debt management
            - Infrastructure requirements
            
            Context: {context if context else 'Annual technology planning'}
            
            Deliver a detailed technology roadmap with timelines and priorities.""",
            agent=agent,
            expected_output="A technology roadmap with priorities, timelines, and resource requirements"
        )
    
    # Marketing Tasks
    
    @staticmethod
    def create_marketing_campaign_task(agent, campaign_goal: str) -> Task:
        """Create a marketing campaign planning task"""
        return Task(
            description=f"""Plan and design a marketing campaign.
            
            Campaign Goal: {campaign_goal}
            
            Your plan should include:
            - Target audience analysis
            - Campaign messaging and positioning
            - Channel strategy (social media, email, content, etc.)
            - Budget recommendations
            - Success metrics and KPIs
            - Timeline and milestones
            
            Create a comprehensive campaign plan that maximizes impact.""",
            agent=agent,
            expected_output="A detailed marketing campaign plan with strategy, tactics, and metrics"
        )
    
    @staticmethod
    def create_market_analysis_task(agent, market_focus: str = "general") -> Task:
        """Create a market analysis task"""
        return Task(
            description=f"""Conduct a thorough market analysis.
            
            Focus Area: {market_focus}
            
            Analyze:
            - Market size and growth trends
            - Customer segments and behaviors
            - Competitor analysis
            - Market opportunities
            - Potential risks and challenges
            
            Provide data-driven insights and recommendations.""",
            agent=agent,
            expected_output="A comprehensive market analysis report with insights and recommendations"
        )
    
    @staticmethod
    def create_content_creation_task(agent, content_type: str, topic: str) -> Task:
        """Create a content creation task"""
        return Task(
            description=f"""Create engaging {content_type} content on the topic: {topic}
            
            Requirements:
            - Align with brand voice and values
            - Engage target audience
            - Include call-to-action
            - Optimize for SEO (if applicable)
            - Ensure accuracy and quality
            
            Deliver high-quality, compelling content.""",
            agent=agent,
            expected_output=f"High-quality {content_type} content ready for publication"
        )
    
    # Operations Tasks
    
    @staticmethod
    def create_process_optimization_task(agent, process_name: str) -> Task:
        """Create a process optimization task"""
        return Task(
            description=f"""Analyze and optimize the {process_name} process.
            
            Steps:
            1. Document current process flow
            2. Identify bottlenecks and inefficiencies
            3. Propose improvements and optimizations
            4. Estimate impact (time saved, cost reduction, etc.)
            5. Create implementation plan
            
            Deliver actionable process improvements.""",
            agent=agent,
            expected_output="A process optimization plan with current state, proposed improvements, and implementation steps"
        )
    
    @staticmethod
    def create_quality_audit_task(agent, audit_scope: str) -> Task:
        """Create a quality audit task"""
        return Task(
            description=f"""Conduct a quality audit for: {audit_scope}
            
            Audit checklist:
            - Review quality standards and compliance
            - Identify quality issues and gaps
            - Assess process adherence
            - Recommend corrective actions
            - Suggest preventive measures
            
            Provide a comprehensive audit report.""",
            agent=agent,
            expected_output="A quality audit report with findings, issues, and recommendations"
        )
    
    # HR Tasks
    
    @staticmethod
    def create_recruitment_task(agent, position: str, requirements: str) -> Task:
        """Create a recruitment task"""
        return Task(
            description=f"""Manage recruitment for the position: {position}
            
            Requirements: {requirements}
            
            Your responsibilities:
            - Create job description
            - Define candidate profile
            - Outline sourcing strategy
            - Design interview process
            - Recommend assessment criteria
            
            Deliver a comprehensive recruitment plan.""",
            agent=agent,
            expected_output="A recruitment plan with job description, candidate profile, and hiring process"
        )
    
    @staticmethod
    def create_employee_engagement_task(agent, focus_area: str = "general") -> Task:
        """Create an employee engagement task"""
        return Task(
            description=f"""Develop an employee engagement initiative.
            
            Focus: {focus_area}
            
            Consider:
            - Current engagement levels
            - Employee feedback and concerns
            - Engagement programs and activities
            - Recognition and rewards
            - Career development opportunities
            
            Create an actionable engagement plan.""",
            agent=agent,
            expected_output="An employee engagement plan with initiatives, activities, and success metrics"
        )
    
    # Software Development Tasks
    
    @staticmethod
    def create_feature_development_task(agent, feature_description: str) -> Task:
        """Create a feature development task"""
        return Task(
            description=f"""Develop the following feature: {feature_description}
            
            Development process:
            - Analyze requirements
            - Design technical solution
            - Write clean, maintainable code
            - Include unit tests
            - Document implementation
            
            Deliver production-ready code.""",
            agent=agent,
            expected_output="Production-ready code with tests and documentation"
        )
    
    @staticmethod
    def create_code_review_task(agent, code_context: str) -> Task:
        """Create a code review task"""
        return Task(
            description=f"""Review code for: {code_context}
            
            Review checklist:
            - Code quality and standards
            - Best practices adherence
            - Performance considerations
            - Security vulnerabilities
            - Test coverage
            - Documentation completeness
            
            Provide constructive feedback and recommendations.""",
            agent=agent,
            expected_output="A code review report with feedback, issues, and recommendations"
        )
    
    @staticmethod
    def create_testing_task(agent, test_scope: str) -> Task:
        """Create a software testing task"""
        return Task(
            description=f"""Test the following: {test_scope}
            
            Testing activities:
            - Design test cases
            - Execute functional tests
            - Perform regression testing
            - Document bugs and issues
            - Verify fixes
            
            Ensure comprehensive test coverage.""",
            agent=agent,
            expected_output="A test report with test cases, results, and identified issues"
        )
    
    # Commercial Tasks
    
    @staticmethod
    def create_sales_strategy_task(agent, target_market: str) -> Task:
        """Create a sales strategy task"""
        return Task(
            description=f"""Develop a sales strategy for: {target_market}
            
            Strategy components:
            - Target customer identification
            - Value proposition
            - Sales approach and tactics
            - Pricing strategy
            - Sales enablement needs
            - Performance metrics
            
            Create a comprehensive sales strategy.""",
            agent=agent,
            expected_output="A sales strategy document with tactics, targets, and metrics"
        )
    
    @staticmethod
    def create_business_development_task(agent, opportunity: str) -> Task:
        """Create a business development task"""
        return Task(
            description=f"""Explore and develop business opportunity: {opportunity}
            
            Activities:
            - Assess opportunity viability
            - Identify potential partners
            - Develop partnership approach
            - Estimate revenue potential
            - Create action plan
            
            Deliver a business development plan.""",
            agent=agent,
            expected_output="A business development plan with opportunity assessment and action items"
        )
    
    @staticmethod
    def create_sales_analysis_task(agent, analysis_period: str = "quarterly") -> Task:
        """Create a sales analysis task"""
        return Task(
            description=f"""Analyze sales performance for the {analysis_period} period.
            
            Analysis areas:
            - Revenue performance vs targets
            - Sales trends and patterns
            - Customer acquisition metrics
            - Product/service performance
            - Sales team productivity
            - Forecast for next period
            
            Provide actionable insights.""",
            agent=agent,
            expected_output="A sales analysis report with performance data, trends, and recommendations"
        )
    
    # Cross-functional Tasks
    
    @staticmethod
    def create_product_launch_task(agent, product_name: str) -> Task:
        """Create a product launch coordination task"""
        return Task(
            description=f"""Coordinate the launch of: {product_name}
            
            From your department's perspective, address:
            - Launch readiness assessment
            - Department-specific deliverables
            - Timeline and milestones
            - Cross-functional dependencies
            - Risk mitigation
            - Success criteria
            
            Ensure successful product launch.""",
            agent=agent,
            expected_output="A department-specific product launch plan with deliverables and timeline"
        )
    
    @staticmethod
    def create_quarterly_review_task(agent, quarter: str) -> Task:
        """Create a quarterly review task"""
        return Task(
            description=f"""Conduct a quarterly performance review for {quarter}.
            
            Review areas:
            - Goals achievement
            - Key accomplishments
            - Challenges faced
            - Lessons learned
            - Plans for next quarter
            
            Provide comprehensive quarterly insights.""",
            agent=agent,
            expected_output="A quarterly review report with performance summary and forward-looking plans"
        )

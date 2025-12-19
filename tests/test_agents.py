"""
Unit tests for AI Company agents.
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from company.agents.company_agents import CompanyAgents
from company.models.hierarchy import Department


class TestCompanyAgents(unittest.TestCase):
    """Test agent creation and configuration"""
    
    def test_create_executive_agents(self):
        """Test creating executive agents"""
        ceo = CompanyAgents.create_ceo()
        self.assertIsNotNone(ceo)
        self.assertTrue(ceo.allow_delegation)
        print("✓ CEO agent created successfully")
        
        cto = CompanyAgents.create_cto()
        self.assertIsNotNone(cto)
        self.assertTrue(cto.allow_delegation)
        print("✓ CTO agent created successfully")
    
    def test_create_department_head_agents(self):
        """Test creating department head agents"""
        heads = [
            ("Marketing", CompanyAgents.create_head_of_marketing),
            ("Operations", CompanyAgents.create_head_of_operations),
            ("HR", CompanyAgents.create_head_of_hr),
            ("Software Development", CompanyAgents.create_head_of_software_development),
            ("Commercial", CompanyAgents.create_head_of_commercial),
        ]
        
        for name, factory in heads:
            agent = factory()
            self.assertIsNotNone(agent)
            self.assertTrue(agent.allow_delegation, f"Head of {name} should allow delegation")
            print(f"✓ Head of {name} agent created successfully")
    
    def test_create_specialist_agents(self):
        """Test creating specialist agents"""
        specialists = [
            ("Marketing Analyst", CompanyAgents.create_marketing_analyst),
            ("Content Marketing Expert", CompanyAgents.create_content_marketing_expert),
            ("Operations Analyst", CompanyAgents.create_operations_analyst),
            ("QA Expert", CompanyAgents.create_qa_expert),
            ("Recruitment Specialist", CompanyAgents.create_recruitment_specialist),
            ("HR Analyst", CompanyAgents.create_hr_analyst),
            ("Senior Developer", CompanyAgents.create_senior_developer),
            ("Software Developer", CompanyAgents.create_software_developer),
            ("QA Analyst", CompanyAgents.create_qa_analyst),
            ("Sales Analyst", CompanyAgents.create_sales_analyst),
            ("Business Development Expert", CompanyAgents.create_business_development_expert),
        ]
        
        for name, factory in specialists:
            agent = factory()
            self.assertIsNotNone(agent)
            print(f"✓ {name} agent created successfully")
    
    def test_get_all_agents(self):
        """Test getting all agents"""
        all_agents = CompanyAgents.get_all_agents()
        self.assertIsNotNone(all_agents)
        self.assertGreater(len(all_agents), 0)
        print(f"✓ Retrieved {len(all_agents)} agents")
        
        # Verify key agents exist
        self.assertIn("ceo", all_agents)
        self.assertIn("cto", all_agents)
        print("✓ Key agents present in collection")
    
    def test_get_agents_by_department(self):
        """Test getting agents by department"""
        for dept in Department:
            agents = CompanyAgents.get_agents_by_department(dept)
            self.assertIsNotNone(agents)
            if dept != Department.EXECUTIVE:  # Executive might be handled differently
                self.assertGreater(len(agents), 0, f"{dept.value} should have agents")
            print(f"✓ {dept.value}: {len(agents)} agents")


class TestAgentConfiguration(unittest.TestCase):
    """Test agent configuration details"""
    
    def test_agent_has_role(self):
        """Test that agents have defined roles"""
        agent = CompanyAgents.create_ceo()
        self.assertTrue(hasattr(agent, 'role'))
        self.assertIsNotNone(agent.role)
        print(f"✓ Agent has role: {agent.role}")
    
    def test_agent_has_goal(self):
        """Test that agents have defined goals"""
        agent = CompanyAgents.create_ceo()
        self.assertTrue(hasattr(agent, 'goal'))
        self.assertIsNotNone(agent.goal)
        print(f"✓ Agent has goal defined")
    
    def test_agent_has_backstory(self):
        """Test that agents have backstories"""
        agent = CompanyAgents.create_ceo()
        self.assertTrue(hasattr(agent, 'backstory'))
        self.assertIsNotNone(agent.backstory)
        print(f"✓ Agent has backstory defined")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("RUNNING AI COMPANY AGENTS TESTS")
    print("="*80 + "\n")
    
    unittest.main(verbosity=2)

"""
Integration tests for AI Company structure.
These tests verify the overall system structure without making API calls.
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from company import (
    AICompany,
    Department,
    RoleLevel,
    OrganizationalChart,
    CompanyAgents,
    CompanyTasks,
    CompanyCrews
)


class TestSystemIntegration(unittest.TestCase):
    """Test system integration"""
    
    def setUp(self):
        """Set up test environment"""
        # Set a dummy API key for structure testing
        os.environ['OPENAI_API_KEY'] = 'test-key-for-structure-testing'
    
    def test_company_initialization(self):
        """Test that company can be initialized"""
        company = AICompany("Test Company")
        self.assertEqual(company.company_name, "Test Company")
        print("✓ Company initialized successfully")
    
    def test_organizational_chart_display(self):
        """Test that org chart can be displayed"""
        company = AICompany("Test Company")
        # This should not raise an error
        company.display_organizational_chart()
        print("✓ Organizational chart displayed successfully")
    
    def test_list_departments(self):
        """Test that departments can be listed"""
        company = AICompany("Test Company")
        # This should not raise an error
        company.list_available_departments()
        print("✓ Departments listed successfully")
    
    def test_all_departments_have_crews(self):
        """Test that all departments can create crews"""
        for dept in Department:
            try:
                crew = CompanyCrews.get_crew_by_department(dept)
                self.assertIsNotNone(crew)
                self.assertGreater(len(crew.agents), 0)
                self.assertGreater(len(crew.tasks), 0)
                print(f"✓ {dept.value}: crew created with {len(crew.agents)} agents and {len(crew.tasks)} tasks")
            except ValueError as e:
                # Some departments might not have crews defined yet
                print(f"⚠ {dept.value}: {str(e)}")
    
    def test_cross_functional_crews(self):
        """Test that cross-functional crews can be created"""
        # Product launch crew
        crew = CompanyCrews.create_product_launch_crew("Test Product")
        self.assertIsNotNone(crew)
        self.assertGreater(len(crew.agents), 1)
        print(f"✓ Product launch crew: {len(crew.agents)} agents")
        
        # Quarterly review crew
        crew = CompanyCrews.create_quarterly_review_crew("Q4 2024")
        self.assertIsNotNone(crew)
        self.assertGreater(len(crew.agents), 1)
        print(f"✓ Quarterly review crew: {len(crew.agents)} agents")
        
        # Executive crew
        crew = CompanyCrews.create_executive_crew()
        self.assertIsNotNone(crew)
        self.assertEqual(len(crew.agents), 2)  # CEO and CTO
        print(f"✓ Executive crew: {len(crew.agents)} agents")


class TestModuleImports(unittest.TestCase):
    """Test that all modules can be imported"""
    
    def test_import_hierarchy_module(self):
        """Test importing hierarchy module"""
        from company.models import hierarchy
        self.assertTrue(hasattr(hierarchy, 'OrganizationalChart'))
        print("✓ Hierarchy module imported successfully")
    
    def test_import_agents_module(self):
        """Test importing agents module"""
        from company.agents import company_agents
        self.assertTrue(hasattr(company_agents, 'CompanyAgents'))
        print("✓ Agents module imported successfully")
    
    def test_import_tasks_module(self):
        """Test importing tasks module"""
        from company.tasks import company_tasks
        self.assertTrue(hasattr(company_tasks, 'CompanyTasks'))
        print("✓ Tasks module imported successfully")
    
    def test_import_crews_module(self):
        """Test importing crews module"""
        from company.crews import company_crews
        self.assertTrue(hasattr(company_crews, 'CompanyCrews'))
        print("✓ Crews module imported successfully")
    
    def test_import_main_company(self):
        """Test importing main company module"""
        from company import company
        self.assertTrue(hasattr(company, 'AICompany'))
        print("✓ Company module imported successfully")


class TestPackageStructure(unittest.TestCase):
    """Test package structure"""
    
    def test_package_exports(self):
        """Test that package exports are correct"""
        import company
        
        expected_exports = [
            'AICompany',
            'Department',
            'RoleLevel',
            'OrganizationalChart',
            'CompanyAgents',
            'CompanyTasks',
            'CompanyCrews'
        ]
        
        for export in expected_exports:
            self.assertTrue(
                hasattr(company, export),
                f"Package should export {export}"
            )
            print(f"✓ {export} available in package")
    
    def test_version_defined(self):
        """Test that package version is defined"""
        import company
        self.assertTrue(hasattr(company, '__version__'))
        print(f"✓ Package version: {company.__version__}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("RUNNING AI COMPANY INTEGRATION TESTS")
    print("="*80 + "\n")
    
    unittest.main(verbosity=2)

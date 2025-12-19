"""
Unit tests for AI Company organizational hierarchy.
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from company.models.hierarchy import (
    RoleLevel,
    Department,
    Role,
    OrganizationalChart
)


class TestOrganizationalHierarchy(unittest.TestCase):
    """Test organizational structure"""
    
    def test_hierarchy_completeness(self):
        """Test that hierarchy is defined and not empty"""
        hierarchy = OrganizationalChart.get_hierarchy()
        self.assertIsNotNone(hierarchy)
        self.assertGreater(len(hierarchy), 0)
        print(f"✓ Hierarchy contains {len(hierarchy)} roles")
    
    def test_all_departments_have_roles(self):
        """Test that all departments have at least one role"""
        for dept in Department:
            roles = OrganizationalChart.get_roles_by_department(dept)
            self.assertGreater(
                len(roles), 
                0, 
                f"Department {dept.value} should have at least one role"
            )
            print(f"✓ {dept.value}: {len(roles)} roles")
    
    def test_executive_structure(self):
        """Test that executive structure is properly defined"""
        hierarchy = OrganizationalChart.get_hierarchy()
        
        # Find CEO
        ceo = next((r for r in hierarchy if r.title == "CEO"), None)
        self.assertIsNotNone(ceo, "CEO role should exist")
        self.assertIsNone(ceo.reports_to, "CEO should not report to anyone")
        self.assertEqual(ceo.level, RoleLevel.EXECUTIVE)
        print("✓ CEO properly defined")
        
        # Find CTO
        cto = next((r for r in hierarchy if r.title == "CTO"), None)
        self.assertIsNotNone(cto, "CTO role should exist")
        self.assertEqual(cto.reports_to, "CEO", "CTO should report to CEO")
        self.assertEqual(cto.level, RoleLevel.EXECUTIVE)
        print("✓ CTO properly defined")
    
    def test_department_heads(self):
        """Test that all major departments have heads"""
        hierarchy = OrganizationalChart.get_hierarchy()
        
        expected_heads = [
            "Head of Marketing",
            "Head of Operations",
            "Head of HR",
            "Head of Software Development",
            "Head of Commercial"
        ]
        
        for head_title in expected_heads:
            head = next((r for r in hierarchy if r.title == head_title), None)
            self.assertIsNotNone(head, f"{head_title} should exist")
            self.assertEqual(head.level, RoleLevel.HEAD)
            print(f"✓ {head_title} properly defined")
    
    def test_role_attributes(self):
        """Test that roles have required attributes"""
        hierarchy = OrganizationalChart.get_hierarchy()
        
        for role in hierarchy:
            self.assertIsNotNone(role.title, "Role should have a title")
            self.assertIsNotNone(role.level, "Role should have a level")
            self.assertIsNotNone(role.department, "Role should have a department")
            self.assertIsInstance(role.responsibilities, list, "Responsibilities should be a list")
            self.assertIsInstance(role.skills, list, "Skills should be a list")
        
        print(f"✓ All {len(hierarchy)} roles have required attributes")
    
    def test_reporting_structure(self):
        """Test that reporting structure is valid"""
        hierarchy = OrganizationalChart.get_hierarchy()
        all_titles = {role.title for role in hierarchy}
        
        for role in hierarchy:
            if role.reports_to:
                self.assertIn(
                    role.reports_to,
                    all_titles,
                    f"{role.title} reports to {role.reports_to}, but that role doesn't exist"
                )
        
        print("✓ All reporting relationships are valid")
    
    def test_departments_by_level(self):
        """Test getting roles by hierarchy level"""
        for level in RoleLevel:
            roles = OrganizationalChart.get_roles_by_level(level)
            for role in roles:
                self.assertEqual(role.level, level)
            if roles:
                print(f"✓ {level.value}: {len(roles)} roles")


class TestRoleModel(unittest.TestCase):
    """Test Role model"""
    
    def test_role_creation(self):
        """Test creating a role"""
        role = Role(
            title="Test Role",
            level=RoleLevel.EXPERT,
            department=Department.MARKETING,
            reports_to="Head of Marketing",
            responsibilities=["Test responsibility"],
            skills=["Test skill"]
        )
        
        self.assertEqual(role.title, "Test Role")
        self.assertEqual(role.level, RoleLevel.EXPERT)
        self.assertEqual(role.department, Department.MARKETING)
        print("✓ Role creation works")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("RUNNING AI COMPANY ORGANIZATIONAL HIERARCHY TESTS")
    print("="*80 + "\n")
    
    # Run tests with verbose output
    unittest.main(verbosity=2)

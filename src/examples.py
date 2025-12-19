"""
Example scenarios demonstrating the AI Company simulation.
Run this script to see the company in action.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from company import AICompany, Department


def scenario_1_marketing_campaign():
    """
    Scenario 1: Marketing Department runs a campaign
    
    This scenario demonstrates the marketing department working together
    to plan and execute a marketing campaign.
    """
    print("\n" + "="*80)
    print("SCENARIO 1: MARKETING CAMPAIGN")
    print("="*80)
    
    company = AICompany()
    
    result = company.run_department_workflow(
        Department.MARKETING,
        campaign_goal="Launch new AI product to enterprise market"
    )
    
    print("\n✓ Marketing campaign planning completed!")
    print(f"  Agents involved: {result['agents_count']}")
    print(f"  Tasks completed: {result['tasks_count']}")
    
    return result


def scenario_2_software_development():
    """
    Scenario 2: Software Development builds a new feature
    
    This scenario shows the development team working through the full
    development lifecycle from design to testing.
    """
    print("\n" + "="*80)
    print("SCENARIO 2: SOFTWARE DEVELOPMENT")
    print("="*80)
    
    company = AICompany()
    
    result = company.run_department_workflow(
        Department.SOFTWARE_DEVELOPMENT,
        feature="User authentication with OAuth2 and JWT tokens"
    )
    
    print("\n✓ Feature development completed!")
    print(f"  Agents involved: {result['agents_count']}")
    print(f"  Tasks completed: {result['tasks_count']}")
    
    return result


def scenario_3_hr_recruitment():
    """
    Scenario 3: HR Department recruits new talent
    
    This scenario demonstrates the HR team working on recruitment
    and employee engagement initiatives.
    """
    print("\n" + "="*80)
    print("SCENARIO 3: HR RECRUITMENT")
    print("="*80)
    
    company = AICompany()
    
    result = company.run_department_workflow(
        Department.HUMAN_RESOURCES,
        focus="talent acquisition"
    )
    
    print("\n✓ HR recruitment process completed!")
    print(f"  Agents involved: {result['agents_count']}")
    print(f"  Tasks completed: {result['tasks_count']}")
    
    return result


def scenario_4_product_launch():
    """
    Scenario 4: Cross-functional Product Launch
    
    This scenario shows multiple departments coordinating to launch
    a new product, demonstrating cross-functional collaboration.
    """
    print("\n" + "="*80)
    print("SCENARIO 4: CROSS-FUNCTIONAL PRODUCT LAUNCH")
    print("="*80)
    
    company = AICompany()
    
    result = company.run_product_launch("AI Assistant Pro")
    
    print("\n✓ Product launch completed!")
    print(f"  Departments involved: {result['departments_involved']}")
    
    return result


def scenario_5_quarterly_review():
    """
    Scenario 5: Quarterly Business Review
    
    This scenario demonstrates all department heads presenting
    their quarterly performance to the CEO.
    """
    print("\n" + "="*80)
    print("SCENARIO 5: QUARTERLY BUSINESS REVIEW")
    print("="*80)
    
    company = AICompany()
    
    result = company.run_quarterly_review("Q4 2024")
    
    print("\n✓ Quarterly review completed!")
    print(f"  Departments reviewed: {result['departments_reviewed']}")
    
    return result


def scenario_6_strategic_planning():
    """
    Scenario 6: Executive Strategic Planning
    
    This scenario shows the CEO and CTO collaborating on
    strategic planning for the company.
    """
    print("\n" + "="*80)
    print("SCENARIO 6: EXECUTIVE STRATEGIC PLANNING")
    print("="*80)
    
    company = AICompany()
    
    result = company.run_strategic_planning("2025 Annual Strategy")
    
    print("\n✓ Strategic planning completed!")
    
    return result


def run_all_scenarios():
    """Run all example scenarios"""
    print("\n" + "="*80)
    print("AI COMPANY SIMULATION - ALL SCENARIOS")
    print("="*80)
    
    scenarios = [
        ("Marketing Campaign", scenario_1_marketing_campaign),
        ("Software Development", scenario_2_software_development),
        ("HR Recruitment", scenario_3_hr_recruitment),
        ("Product Launch", scenario_4_product_launch),
        ("Quarterly Review", scenario_5_quarterly_review),
        ("Strategic Planning", scenario_6_strategic_planning),
    ]
    
    print("\nAvailable scenarios:")
    for i, (name, _) in enumerate(scenarios, 1):
        print(f"  {i}. {name}")
    
    print("\nNote: Running all scenarios will take significant time and API calls.")
    print("For demonstration, run individual scenario functions instead.")
    

def display_company_structure():
    """Display the organizational structure"""
    company = AICompany()
    company.display_organizational_chart()
    company.list_available_departments()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Company Simulation Examples")
    parser.add_argument(
        "--scenario",
        type=int,
        choices=range(1, 7),
        help="Run a specific scenario (1-6)"
    )
    parser.add_argument(
        "--show-structure",
        action="store_true",
        help="Display organizational structure"
    )
    
    args = parser.parse_args()
    
    if args.show_structure:
        display_company_structure()
    elif args.scenario:
        scenario_map = {
            1: scenario_1_marketing_campaign,
            2: scenario_2_software_development,
            3: scenario_3_hr_recruitment,
            4: scenario_4_product_launch,
            5: scenario_5_quarterly_review,
            6: scenario_6_strategic_planning,
        }
        scenario_map[args.scenario]()
    else:
        # Default: show structure and available scenarios
        display_company_structure()
        run_all_scenarios()

#!/usr/bin/env python3
"""
Main entry point for AI Company simulation.
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from company import AICompany, Department


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AI Company Simulation - A CrewAI-powered organizational simulation"
    )
    
    parser.add_argument(
        '--show-org',
        action='store_true',
        help='Display organizational chart'
    )
    
    parser.add_argument(
        '--department',
        type=str,
        choices=['marketing', 'operations', 'hr', 'software', 'commercial', 'executive'],
        help='Run a department workflow'
    )
    
    parser.add_argument(
        '--product-launch',
        type=str,
        metavar='PRODUCT_NAME',
        help='Run a product launch scenario'
    )
    
    parser.add_argument(
        '--quarterly-review',
        type=str,
        metavar='QUARTER',
        help='Run a quarterly review (e.g., Q4 2024)'
    )
    
    parser.add_argument(
        '--strategic-planning',
        action='store_true',
        help='Run strategic planning session'
    )
    
    args = parser.parse_args()
    
    # Initialize company
    company = AICompany()
    
    # Handle different commands
    if args.show_org:
        company.display_organizational_chart()
        company.list_available_departments()
    
    elif args.department:
        dept_mapping = {
            'marketing': Department.MARKETING,
            'operations': Department.OPERATIONS,
            'hr': Department.HUMAN_RESOURCES,
            'software': Department.SOFTWARE_DEVELOPMENT,
            'commercial': Department.COMMERCIAL,
            'executive': Department.EXECUTIVE
        }
        department = dept_mapping[args.department]
        company.run_department_workflow(department)
    
    elif args.product_launch:
        company.run_product_launch(args.product_launch)
    
    elif args.quarterly_review:
        company.run_quarterly_review(args.quarterly_review)
    
    elif args.strategic_planning:
        company.run_strategic_planning()
    
    else:
        # Default: show help and structure
        parser.print_help()
        print("\n")
        company.display_organizational_chart()


if __name__ == "__main__":
    main()

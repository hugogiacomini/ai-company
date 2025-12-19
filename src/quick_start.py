"""
Simple example to get started with AI Company simulation.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv("OPENAI_API_KEY"):
    print("\n⚠️  WARNING: OPENAI_API_KEY not found!")
    print("Please copy .env.example to .env and add your OpenAI API key.\n")
    exit(1)

# Import AI Company
from company import AICompany, Department

# Initialize the company
company = AICompany("My AI Company")

# Display the organizational structure
print("\n" + "="*80)
print("STEP 1: View Organizational Structure")
print("="*80)
company.display_organizational_chart()

# List available departments
print("\n" + "="*80)
print("STEP 2: Available Departments")
print("="*80)
company.list_available_departments()

# Example: Run a simple marketing workflow
print("\n" + "="*80)
print("STEP 3: Run a Marketing Department Workflow")
print("="*80)
print("\nStarting marketing campaign planning...")
print("(This will make API calls to OpenAI)\n")

try:
    result = company.run_department_workflow(
        Department.MARKETING,
        campaign_goal="Increase brand awareness for AI products"
    )
    
    print("\n✓ SUCCESS!")
    print(f"Department: {result['department']}")
    print(f"Agents: {result['agents_count']}")
    print(f"Tasks: {result['tasks_count']}")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    print("\nMake sure:")
    print("1. You have installed all requirements: pip install -r requirements.txt")
    print("2. You have set OPENAI_API_KEY in .env file")
    print("3. You have sufficient OpenAI API credits")

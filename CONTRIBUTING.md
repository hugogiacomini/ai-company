# Contributing to AI Company

Thank you for your interest in contributing to AI Company! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Example implementation (if applicable)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add docstrings to new functions/classes
   - Update documentation as needed

4. **Test your changes**
   - Ensure existing functionality still works
   - Test new features thoroughly

5. **Commit your changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

## Development Setup

1. Clone the repository
   ```bash
   git clone https://github.com/hugogiacomini/ai-company.git
   cd ai-company
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where applicable
- Write clear, descriptive docstrings
- Keep functions focused and modular
- Use meaningful variable names

## Adding New Features

### Adding a New Department

1. Add the department to `Department` enum in `src/company/models/hierarchy.py`
2. Add roles for the department in `OrganizationalChart.get_hierarchy()`
3. Create agent factory methods in `src/company/agents/company_agents.py`
4. Add task templates in `src/company/tasks/company_tasks.py`
5. Create a crew factory in `src/company/crews/company_crews.py`
6. Update documentation

### Adding a New Agent Role

1. Add the role to `OrganizationalChart.get_hierarchy()` in `hierarchy.py`
2. Create an agent factory method in `company_agents.py`
3. Update the `get_all_agents()` method
4. Add the agent to appropriate department crews

### Adding a New Task Type

1. Create a task factory method in `company_tasks.py`
2. Follow the existing pattern with clear description and expected output
3. Use the task in appropriate crews

### Adding a New Scenario

1. Create a scenario function in `src/examples.py`
2. Follow the existing pattern
3. Add it to the scenarios list in `run_all_scenarios()`
4. Update documentation

## Testing Guidelines

- Test new agents with simple tasks first
- Verify task outputs are meaningful
- Test cross-functional scenarios
- Check for API rate limits and costs
- Validate error handling

## Documentation

- Update README.md for major features
- Add docstrings to all new code
- Include usage examples for new features
- Update configuration documentation

## Pull Request Guidelines

- Provide a clear description of changes
- Reference related issues
- Include examples of new functionality
- Update tests and documentation
- Ensure code passes all checks

## Questions?

Feel free to open an issue for:
- Questions about contributing
- Clarification on implementation
- Discussion of proposed features

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

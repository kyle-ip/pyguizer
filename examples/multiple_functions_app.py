"""
Comprehensive PyGUIzer Example: Project Management Dashboard

This example demonstrates all core features of PyGUIzer:
1. Automatic UI Generation for 15+ Python types
2. Advanced Type Mapping with complex data structures
3. Custom Layout Configuration
4. Preset Management System
5. Markdown Rendering for rich outputs
6. Real-time Updates with WebSockets
7. Multiple Functions Support
8. Custom Widget Registry

Real-life use case: Project Management Dashboard for a software development team
"""

from typing import List, Dict, Set, Tuple, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import date, time, datetime
from decimal import Decimal
from uuid import UUID, uuid4
from pathlib import Path
from pyguizer import PyGUIzer

# --- Custom Types & Enums for our project management system ---

class TaskStatus(Enum):
    """Status of a project task"""
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    REVIEW = "Review"
    DONE = "Done"
    BLOCKED = "Blocked"


class Priority(Enum):
    """Priority levels for tasks"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"


class Department(Enum):
    """Company departments"""
    ENGINEERING = "Engineering"
    DESIGN = "Design"
    MARKETING = "Marketing"
    SALES = "Sales"
    HR = "Human Resources"


@dataclass
class TeamMember:
    """Represents a team member"""
    id: UUID
    name: str
    email: str
    department: Department
    role: str
    is_available: bool = True


@dataclass
class Task:
    """Represents a project task"""
    id: UUID
    title: str
    description: str
    status: TaskStatus
    priority: Priority
    assignee: Optional[TeamMember]
    start_date: date
    end_date: date
    estimated_hours: float
    actual_hours: float = 0.0
    tags: Set[str] = None
    dependencies: List[UUID] = None


# --- Custom Layout Configuration ---
layout_config = {
    "sections": [
        {
            "name": "Task Basics",
            "widgets": ["title", "description", "status", "priority"]
        },
        {
            "name": "Timeline",
            "widgets": ["start_date", "end_date", "estimated_hours"]
        },
        {
            "name": "Assignment",
            "widgets": ["assignee_id", "tags"]
        }
    ]
}


# Create a PyGUIzer instance with custom layout for create_task function
pyguizer_create_task = PyGUIzer(layout=layout_config)

# Create a default PyGUIzer instance for other functions
pyguizer = PyGUIzer()


# --- Function 1: Create a new task ---
@pyguizer_create_task
def create_task(
    title: str,
    description: str,
    status: TaskStatus = TaskStatus.TODO,
    priority: Priority = Priority.MEDIUM,
    assignee_id: Optional[UUID] = None,
    start_date: date = None,
    end_date: date = None,
    estimated_hours: float = 8.0,
    tags: Set[str] = None,
    dependencies: List[UUID] = None
) -> Dict[str, Any]:
    """Create a new project task with detailed information."""
    # Generate a random UUID if not provided
    task_id = uuid4()
    
    # Simulate creating task in database
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "status": status.value,
        "priority": priority.value,
        "assignee_id": assignee_id,
        "start_date": start_date.isoformat() if start_date else None,
        "end_date": end_date.isoformat() if end_date else None,
        "estimated_hours": estimated_hours,
        "actual_hours": 0.0,
        "tags": tags or set(),
        "dependencies": dependencies or [],
        "created_at": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "message": f"Task '{title}' created successfully!",
        "task": task
    }


# --- Function 2: Assign team members to tasks ---
@pyguizer
def assign_team_members(
    task_id: UUID,
    team_members: List[UUID],
    roles: Dict[UUID, str],
    allocation_percentages: Dict[UUID, float] = None
) -> str:
    """Assign multiple team members to a task with specific roles and allocation percentages."""
    # Simulate assignment logic
    assignments = []
    for member_id in team_members:
        role = roles.get(member_id, "Team Member")
        allocation = allocation_percentages.get(member_id, 100.0) if allocation_percentages else 100.0
        assignments.append(f"- {member_id}: {role} ({allocation}%)")
    
    # Generate markdown output
    return f"""
# Team Assignment for Task {task_id}

## Assigned Members
{chr(10).join(assignments)}

## Assignment Details
- Total team members: {len(team_members)}
- Assignment date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Status: ✅ Successfully assigned
"""


# --- Function 3: Plan project timeline ---
@pyguizer
def plan_timeline(
    project_name: str,
    start_date: date,
    end_date: date,
    milestones: Dict[date, str],
    resource_allocations: Dict[str, List[Tuple[date, date]]]
) -> str:
    """Create a comprehensive project timeline with milestones and resource allocations."""
    # Generate timeline report in markdown
    milestone_list = "\n".join([f"- {date.isoformat()}: {description}" for date, description in sorted(milestones.items())])
    
    resource_list = []
    for resource, allocations in resource_allocations.items():
        alloc_text = "\n  ".join([f"{start.isoformat()} → {end.isoformat()}" for start, end in allocations])
        resource_list.append(f"- **{resource}**:\n  {alloc_text}")
    
    return f"""
# 📅 Project Timeline: {project_name}

## Basic Information
- **Start Date**: {start_date.isoformat()}
- **End Date**: {end_date.isoformat()}
- **Duration**: {(end_date - start_date).days} days

## Milestones
{milestone_list}

## Resource Allocations
{chr(10).join(resource_list)}

## Timeline Status
✅ Timeline created successfully!
"""


# --- Function 4: Track project budget ---
@pyguizer
def track_budget(
    project_id: UUID,
    budget: Decimal,
    expenses: List[Dict[str, Any]],
    contingency_percentage: float = 10.0,
    forecast_months: int = 3
) -> Dict[str, Any]:
    """Track project budget with expenses, contingencies, and forecasts."""
    # Calculate total expenses
    total_expenses = sum(Decimal(expense.get("amount", 0)) for expense in expenses)
    
    # Calculate contingency amount
    contingency = budget * Decimal(contingency_percentage / 100)
    
    # Calculate remaining budget
    remaining = budget - total_expenses - contingency
    
    # Generate forecast
    monthly_average = total_expenses / Decimal(forecast_months) if forecast_months > 0 else Decimal(0)
    forecast = {
        "monthly_average": float(monthly_average),
        "forecasted_total": float(total_expenses + monthly_average * Decimal(forecast_months)),
        "will_overrun": (total_expenses + monthly_average * Decimal(forecast_months)) > budget
    }
    
    return {
        "project_id": str(project_id),
        "total_budget": float(budget),
        "total_expenses": float(total_expenses),
        "contingency": float(contingency),
        "remaining_budget": float(remaining),
        "utilization_rate": float(total_expenses / budget * 100) if budget > 0 else 0,
        "forecast": forecast,
        "expense_count": len(expenses),
        "status": "Over budget!" if remaining < 0 else "On track!"
    }


# --- Function 5: Generate project report ---
@pyguizer
def generate_project_report(
    project_id: UUID,
    include_tasks: bool = True,
    include_budget: bool = True,
    include_team: bool = True,
    detailed: bool = False
) -> str:
    """Generate a comprehensive project report with markdown formatting."""
    # Simulate fetching project data
    project_name = f"Project Alpha"
    project_start = date(2024, 1, 1)
    project_end = date(2024, 6, 30)
    
    # Generate report sections
    report = [f"# 📊 Project Report: {project_name}", f"*Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"]
    
    report.append(f"""
## Project Overview
| Metric | Value |
|--------|-------|
| Project ID | {project_id} |
| Status | ✅ Active |
| Duration | {project_start.isoformat()} to {project_end.isoformat()} |
| Progress | 65% |
""")
    
    if include_tasks:
        report.append(f"""
## Task Summary
| Status | Count | Percentage |
|--------|-------|------------|
| Todo | 12 | 20% |
| In Progress | 24 | 40% |
| Review | 8 | 13% |
| Done | 14 | 23% |
| Blocked | 2 | 3% |
| **Total** | **60** | **100%** |
""")
    
    if include_budget:
        report.append(f"""
## Budget Overview
| Category | Planned | Actual | Variance |
|----------|---------|--------|----------|
| Development | $50,000 | $32,500 | -$17,500 |
| Design | $15,000 | $12,800 | -$2,200 |
| Marketing | $10,000 | $8,500 | -$1,500 |
| **Total** | **$75,000** | **$53,800** | **-$21,200** |
""")
    
    if include_team:
        report.append(f"""
## Team Members
- 👨‍💻 John Doe (Lead Developer)
- 👩‍🎨 Jane Smith (UX Designer)
- 📊 Mike Johnson (Project Manager)
- 🔧 Sarah Wilson (DevOps Engineer)
- 📱 Alex Brown (Mobile Developer)
""")
    
    if detailed:
        report.append(f"""
## Detailed Analysis
### Key Achievements
1. ✅ Completed core architecture design
2. ✅ Implemented user authentication system
3. ✅ Launched beta version to 500 users
4. ✅ Achieved 98% test coverage

### Challenges
1. ⚠️ Delayed API integration with third-party service
2. ⚠️ Resource constraints in QA team
3. ⚠️ Changing requirements from stakeholders

### Recommendations
1. 📌 Hire additional QA resources
2. 📌 Implement weekly stakeholder sync meetings
3. 📌 Adopt agile methodologies for faster iterations
""")
    
    report.append(f"""
---
*Report generated by PyGUIzer Project Management Dashboard*
""")
    
    return "\n".join(report)


# --- Function 6: Upload project files ---
@pyguizer
def upload_project_files(
    project_id: UUID,
    files: List[Path],
    tags: Set[str] = None,
    overwrite_existing: bool = False
) -> Dict[str, Any]:
    """Upload multiple files to a project with tags and metadata."""
    # Simulate file upload process
    uploaded_files = []
    for file_path in files:
        uploaded_files.append({
            "name": file_path.name,
            "size": f"{1 + len(file_path.name) * 100} KB",
            "path": str(file_path),
            "uploaded_at": datetime.now().isoformat()
        })
    
    return {
        "project_id": str(project_id),
        "uploaded_files": uploaded_files,
        "total_files": len(uploaded_files),
        "tags": tags or set(),
        "overwrite_existing": overwrite_existing,
        "status": "success",
        "message": f"Successfully uploaded {len(uploaded_files)} files to project {project_id}"
    }


# --- Function 7: Analyze project risks ---
@pyguizer
def analyze_project_risks(
    project_id: UUID,
    identified_risks: List[Dict[str, Any]],
    risk_threshold: float = 0.7
) -> str:
    """Analyze project risks and provide mitigation strategies."""
    # Simulate risk analysis
    high_risks = [risk for risk in identified_risks if risk.get("probability", 0.0) >= risk_threshold]
    medium_risks = [risk for risk in identified_risks if 0.3 <= risk.get("probability", 0.0) < risk_threshold]
    low_risks = [risk for risk in identified_risks if risk.get("probability", 0.0) < 0.3]
    
    # Generate risk report
    report = [
        "# ⚠️ Project Risk Analysis Report",
        "",
        "## Risk Overview",
        "| Risk Level | Count | Percentage |",
        "|------------|-------|------------|",
        f"| 🚨 High | {len(high_risks)} | {round(len(high_risks)/len(identified_risks)*100)}% |",
        f"| ⚠️ Medium | {len(medium_risks)} | {round(len(medium_risks)/len(identified_risks)*100)}% |",
        f"| ✅ Low | {len(low_risks)} | {round(len(low_risks)/len(identified_risks)*100)}% |",
        f"| **Total** | {len(identified_risks)} | **100%** |",
        "",
        "## Top Risks to Mitigate"
    ]
    
    for risk in high_risks[:3]:
        report.extend([
            f"### {risk['title']}",
            f"- Probability: {risk['probability']:.2f}",
            f"- Impact: {risk['impact']}",
            f"- Mitigation: {risk.get('mitigation', 'None specified')}",
            ""
        ])
    
    report.extend([
        "## Risk Management Recommendations",
        "1. **For High Risks**: Implement immediate mitigation strategies and assign owners",
        "2. **For Medium Risks**: Monitor closely and develop contingency plans",
        "3. **For Low Risks**: Document and review periodically",
        "4. **General**: Conduct weekly risk assessment meetings"
    ])
    
    return "\n".join(report)


# --- Run the application ---
if __name__ == "__main__":
    print("=== 🚀 PyGUIzer Comprehensive Project Management Dashboard ===")
    print("This example demonstrates all core features of PyGUIzer")
    print("\n📋 Available Functions:")
    for func in pyguizer.registered_functions:
        print(f"  - {func.__name__}: {func.__doc__.splitlines()[0]}")
    
    print("\n🌐 Access the application at: http://localhost:8080")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)
    
    # Run the PyGUIzer application
    pyguizer.run(
        title="Project Management Dashboard",
        description="Comprehensive project management dashboard with multiple functions",
        port=8080
    )

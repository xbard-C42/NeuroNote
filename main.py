import os
import json
import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
from dataclasses import dataclass, asdict, field

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Data models
@dataclass
class Task:
    id: str
    title: str
    description: str
    status: str = "Not Started"  # Not Started, In Progress, Completed
    priority: str = "Medium"     # Low, Medium, High
    risk_level: str = "Low"      # Low, Medium, High
    estimated_time: str = ""
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    resources: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    notes: str = ""
    
@dataclass
class Project:
    title: str
    description: str
    tasks: List[Task] = field(default_factory=list)
    created_date: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

# AI Functions
def breakdown_project(project_description: str) -> List[Dict]:
    """Use AI to break down a project into tasks"""
    prompt = f"""
    You are an expert project manager helping a neurodivergent entrepreneur with AuDHD traits.
    
    Break the following project description down into 5-10 clear, actionable tasks.
    
    For each task, provide:
    1. A clear, concise title
    2. A detailed description with specific steps
    3. Estimated time to complete (in hours or days)
    4. Required resources (skills, tools, people)
    5. Priority level (Low, Medium, High)
    6. Risk level (Low, Medium, High)
    7. Dependencies (which tasks must be completed first)
    
    Include specific considerations for AuDHD traits such as:
    - Clear starting points for each task
    - Visual organization suggestions 
    - Executive function support
    - Task switching minimization strategies
    
    Format the response as a JSON array of task objects.
    
    Project description:
    {project_description}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Ensure we have a "tasks" key
        if "tasks" not in result:
            if isinstance(result, list):
                return result
            else:
                return [result]
        else:
            return result["tasks"]
    
    except Exception as e:
        print(f"Error in AI task breakdown: {e}")
        return []

def analyze_risks(tasks: List[Dict]) -> List[Dict]:
    """Use AI to analyze risks for each task"""
    task_descriptions = "\n".join([f"Task {i+1}: {task['title']} - {task['description']}" 
                                  for i, task in enumerate(tasks)])
    
    prompt = f"""
    You are an expert risk analyst helping a neurodivergent entrepreneur.
    
    For each of the following tasks, identify potential risks, their impact, 
    probability, and suggest mitigation strategies specific for someone with AuDHD traits.
    
    Tasks:
    {task_descriptions}
    
    Format the response as a JSON array that matches the input tasks, with each object
    containing a "risks" array with identified risks and mitigations.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Merge risk information back into tasks
        if "tasks" in result:
            risk_data = result["tasks"]
        else:
            risk_data = result
            
        for i, task in enumerate(tasks):
            if i < len(risk_data):
                task["risks"] = risk_data[i].get("risks", [])
                
        return tasks
    
    except Exception as e:
        print(f"Error in risk analysis: {e}")
        return tasks

def suggest_resources(project_description: str, tasks: List[Dict]) -> Dict:
    """Use AI to suggest resources for the project"""
    task_descriptions = "\n".join([f"Task {i+1}: {task['title']} - {task['description']}" 
                                  for i, task in enumerate(tasks)])
    
    prompt = f"""
    You are an expert resource planner helping a neurodivergent entrepreneur.
    
    Based on the following project and tasks, suggest:
    1. Team members or roles needed
    2. Tools or technologies recommended
    3. Estimated budget breakdown
    4. Timeline with milestones
    5. Specific accommodations for AuDHD traits
    
    Project description:
    {project_description}
    
    Tasks:
    {task_descriptions}
    
    Format the response as a JSON object with sections for team, tools, budget, timeline, and accommodations.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        print(f"Error in resource suggestions: {e}")
        return {}

# Project Management Functions
def create_project(title: str, description: str) -> Project:
    """Create a new project"""
    return Project(title=title, description=description)

def add_tasks_to_project(project: Project, task_data: List[Dict]) -> Project:
    """Add AI-generated tasks to a project"""
    for i, task_dict in enumerate(task_data):
        task_id = f"task_{i+1}"
        task = Task(
            id=task_id,
            title=task_dict.get("title", f"Task {i+1}"),
            description=task_dict.get("description", ""),
            priority=task_dict.get("priority", "Medium"),
            risk_level=task_dict.get("risk_level", "Low"),
            estimated_time=task_dict.get("estimated_time", ""),
            resources=task_dict.get("resources", []),
            dependencies=task_dict.get("dependencies", [])
        )
        project.tasks.append(task)
    
    return project

def save_project(project: Project, filename: str = None) -> str:
    """Save project to a JSON file"""
    if filename is None:
        filename = f"{project.title.lower().replace(' ', '_')}_project.json"
    
    with open(filename, "w") as f:
        json.dump(asdict(project), f, indent=2)
    
    return filename

def save_markdown_report(project: Project, resources: Dict = None, filename: str = None) -> str:
    """Generate a markdown report of the project"""
    if filename is None:
        filename = f"{project.title.lower().replace(' ', '_')}_report.md"
    
    with open(filename, "w") as f:
        f.write(f"# {project.title}\n\n")
        f.write(f"*Created: {project.created_date[:10]}*\n\n")
        f.write(f"## Project Description\n\n{project.description}\n\n")
        
        # Tasks section
        f.write("## Tasks\n\n")
        for i, task in enumerate(project.tasks):
            f.write(f"### {i+1}. {task.title}\n\n")
            f.write(f"**Priority:** {task.priority} | **Risk Level:** {task.risk_level}")
            if task.estimated_time:
                f.write(f" | **Est. Time:** {task.estimated_time}")
            f.write("\n\n")
            
            f.write(f"{task.description}\n\n")
            
            if task.resources:
                f.write("**Resources Needed:**\n")
                for resource in task.resources:
                    f.write(f"- {resource}\n")
                f.write("\n")
            
            if task.dependencies:
                f.write("**Dependencies:**\n")
                for dep in task.dependencies:
                    f.write(f"- {dep}\n")
                f.write("\n")
        
        # Resources section
        if resources:
            f.write("## Resource Planning\n\n")
            
            if "team" in resources:
                f.write("### Team\n\n")
                if isinstance(resources["team"], list):
                    for item in resources["team"]:
                        f.write(f"- {item}\n")
                else:
                    f.write(f"{resources['team']}\n")
                f.write("\n")
            
            if "tools" in resources:
                f.write("### Tools & Technologies\n\n")
                if isinstance(resources["tools"], list):
                    for item in resources["tools"]:
                        f.write(f"- {item}\n")
                else:
                    f.write(f"{resources['tools']}\n")
                f.write("\n")
            
            if "budget" in resources:
                f.write("### Budget\n\n")
                if isinstance(resources["budget"], list):
                    for item in resources["budget"]:
                        f.write(f"- {item}\n")
                else:
                    f.write(f"{resources['budget']}\n")
                f.write("\n")
            
            if "timeline" in resources:
                f.write("### Timeline\n\n")
                if isinstance(resources["timeline"], list):
                    for item in resources["timeline"]:
                        f.write(f"- {item}\n")
                else:
                    f.write(f"{resources['timeline']}\n")
                f.write("\n")
            
            if "accommodations" in resources:
                f.write("### AuDHD Accommodations\n\n")
                if isinstance(resources["accommodations"], list):
                    for item in resources["accommodations"]:
                        f.write(f"- {item}\n")
                else:
                    f.write(f"{resources['accommodations']}\n")
                f.write("\n")
    
    return filename

# Main application
def main():
    print("\n🚀 NeuroProject Manager - AI-Powered Project Management for AuDHD\n")
    
    # Get project details
    project_title = input("Enter project title:\n> ")
    project_description = input("\nDescribe your project in detail:\n> ")
    
    print("\n📝 Generating project breakdown...\n")
    
    try:
        # Create project
        project = create_project(project_title, project_description)
        
        # Generate tasks with AI
        task_data = breakdown_project(project_description)
        print(f"✅ Generated {len(task_data)} tasks\n")
        
        # Analyze risks
        print("🔍 Analyzing potential risks...\n")
        task_data = analyze_risks(task_data)
        
        # Add tasks to project
        project = add_tasks_to_project(project, task_data)
        
        # Generate resource suggestions
        print("💼 Suggesting resources and timeline...\n")
        resources = suggest_resources(project_description, task_data)
        
        # Display summary
        print("\n✨ Project breakdown completed!\n")
        print(f"Project: {project_title}")
        print(f"Tasks: {len(project.tasks)}")
        
        # Save options
        save_option = input("\nSave project data? (y/n): ").lower()
        if save_option == 'y':
            json_file = save_project(project)
            md_file = save_markdown_report(project, resources)
            print(f"\n✅ Saved project data to {json_file}")
            print(f"✅ Generated report at {md_file}")
            
            print("\n📊 Next steps:")
            print("1. Review the generated report")
            print("2. Set up specific dates for tasks")
            print("3. Identify any additional resources needed")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()
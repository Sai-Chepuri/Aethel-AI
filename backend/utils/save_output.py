import os
import json
from datetime import datetime

def save_generated_plan(plan_dict: dict) -> str:
    """
    Saves the generated product plan as JSON to outputs/{timestamp}.json.
    Creates the outputs/ directory if it doesn't exist.
    
    Args:
        plan_dict: The dictionary containing the generated product plan.
        
    Returns:
        The absolute path to the saved file.
    """
    # Get current directory of this file (backend/utils/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Project root is two levels up from backend/utils/
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    outputs_dir = os.path.join(project_root, "outputs")
    
    # Ensure outputs directory exists
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Format timestamp: YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.json"
    file_path = os.path.join(outputs_dir, filename)
    
    # Write the dictionary as pretty-printed JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(plan_dict, f, indent=2, ensure_ascii=False)
        
    print(f"[save_output] Successfully saved generated plan to: {file_path}")
    return file_path

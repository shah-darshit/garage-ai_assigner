import sqlite3
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database/workshop.db')

TASKS_DATA = {
    'T001': {'name': 'Oil Change', 'time': 25},
    'T002': {'name': 'Oil Filter Replacement', 'time': 15},
    'T003': {'name': 'Air Filter Check', 'time': 15},
    'T004': {'name': 'Fluid Levels Check', 'time': 30},
    'T005': {'name': 'Tyre Pressure Check', 'time': 15},
    'T006': {'name': 'Visual Inspection', 'time': 20},
    'T007': {'name': 'Brake Inspection', 'time': 30},
    'T008': {'name': 'Tyre Condition and Alignment Check', 'time': 30},
    'T009': {'name': 'Battery Check', 'time': 25},
    'T010': {'name': 'Exhaust System Inspection', 'time': 45},
    'T011': {'name': 'Steering and Suspension Check', 'time': 60},
    'T012': {'name': 'Lights and Wipers Check', 'time': 20},
    'T013': {'name': 'Fuel System Inspection', 'time': 65},
    'T014': {'name': 'Transmission Check', 'time': 120},
    'T015': {'name': 'Spark Plugs Replacement', 'time': 180},
    'T016': {'name': 'Timing Belt Inspection', 'time': 35},
    'T017': {'name': 'Wheel Alignment and Balancing', 'time': 30},
    'T018': {'name': 'Cabin Filter Replacement', 'time': 20},
    'T019': {'name': 'Comprehensive Diagnostic Check', 'time': 120},
    'T020': {'name': 'Underbody Inspection', 'time': 60}
}

BASIC_SERVICE_TASKS = ['T001', 'T002', 'T003', 'T004', 'T005', 'T006']
INTERMEDIATE_SERVICE_TASKS = BASIC_SERVICE_TASKS + ['T007', 'T008', 'T009', 'T010', 'T011', 'T012']
FULL_SERVICE_TASKS = INTERMEDIATE_SERVICE_TASKS + ['T013', 'T014', 'T015', 'T016', 'T017', 'T018', 'T019', 'T020']
JOB_TO_TASKS_MAPPING = {
    'Basic Service': BASIC_SERVICE_TASKS,
    'Intermediate Service': INTERMEDIATE_SERVICE_TASKS,
    'Full Service': FULL_SERVICE_TASKS,
    'Custom Service': []
}

def get_next_job_id(cursor):
    """Queries the database to find the next available Job_ID."""
    # This selects the Job_ID with the highest numerical value
    cursor.execute("SELECT Job_ID FROM job_card ORDER BY CAST(SUBSTR(Job_ID, 4) AS INTEGER) DESC LIMIT 1")
    last_job_id = cursor.fetchone()
    if last_job_id:
        # Extract the number part, increment it, and format it back
        last_num = int(last_job_id[0].replace("JOB", ""))
        new_num = last_num + 1
        return f"JOB{new_num}"
    else:
        # If the table is empty, start with JOB1001
        return "JOB1001"
    

def create_new_job_card():
    """
    Simulates a manager creating a new job card, now with a shared Job_ID
    for all related tasks.
    """
    print("\n--- Creating a New Job Card ---")
    print("Available Job Types:", list(JOB_TO_TASKS_MAPPING.keys()))
    job_name = input("Enter the Job Name: ")
    if job_name not in JOB_TO_TASKS_MAPPING:
        print("Error: Invalid Job Name."); return

    tasks_to_perform = []
    if job_name == 'Custom Service':
        print("\n--- Available Tasks for Custom Service ---")
        available_task_ids = list(TASKS_DATA.keys())
        for i, task_id in enumerate(available_task_ids):
            print(f"  [{i+1}] {TASKS_DATA[task_id]['name']}")
        try:
            selection_str = input("\nEnter the numbers of the tasks to add, separated by commas: ")
            selected_indices = [int(s.strip()) - 1 for s in selection_str.split(',')]
            for index in selected_indices:
                if 0 <= index < len(available_task_ids):
                    tasks_to_perform.append(available_task_ids[index])
        except ValueError:
            print("Error: Invalid input."); return
    else:
        tasks_to_perform = JOB_TO_TASKS_MAPPING.get(job_name, [])

    if not tasks_to_perform:
        print("No valid tasks were selected. Aborting."); return

    print("\nEnter Vehicle Details:")
    vin = input("  VIN: "); make = input("  Make: "); model = input("  Model: ")
    try:
        mileage = int(input("  Mileage: "))
    except ValueError:
        print("Error: Mileage must be a number."); return
    urgency = input("Enter Urgency (Normal, High, Low): ")
    if urgency not in ['Normal', 'High', 'Low']:
        print("Error: Invalid Urgency level."); return

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # --- Generate ONE shared Job_ID for this entire work order ---
        shared_job_id = get_next_job_id(cursor)
        print(f"Assigning new shared Job_ID: {shared_job_id}")

        records_to_insert = []
        for task_id in tasks_to_perform:
            task_info = TASKS_DATA.get(task_id)
            if not task_info: continue
            
            # Prepare the record for this specific task
            record = (
                shared_job_id, # Use the same Job_ID for all tasks
                job_name, task_id, task_info['name'], 'Created',datetime.now().date(), urgency, vin, make, model,
                mileage, task_info['time']
            )
            records_to_insert.append(record)
        
        # Insert all task records into the database
        sql = """
        INSERT INTO job_card (
            Job_ID, Job_Name, Task_ID, Task_Description, Status, Date_Created, Urgency, VIN, Make, Model,
            Mileage, Estimated_Standard_Time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.executemany(sql, records_to_insert)
        conn.commit()
        
        print(f"\nSuccessfully created {len(records_to_insert)} tasks under Job_ID {shared_job_id}.")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_new_job_card()

'''def create_job_from_ui_input(job_name, vin, make, model, mileage, urgency, selected_tasks=None):
    """
    Accepts data from a UI/frontend and creates job card records in the database.
    Returns True on success, False on failure.
    """
    if job_name == 'Custom Service' and selected_tasks:
        tasks_to_perform = selected_tasks
    else:
        tasks_to_perform = JOB_TO_TASKS_MAPPING.get(job_name, [])

    if not tasks_to_perform:
        print(f"Error: No tasks found for job '{job_name}'.")
        return False, f"No tasks found for job '{job_name}'"
        
    records_to_insert = []
    for task_id in tasks_to_perform:
        task_info = TASKS_DATA.get(task_id)
        if not task_info:
            continue # Skip if task_id is invalid
            
        record = (
            job_name, task_id, task_info['name'], urgency, vin, make, model,
            mileage, task_info['time'], 'Pending', datetime.now().date()
        )
        records_to_insert.append(record)
        
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        sql = """
        INSERT INTO job_card (
            Job_Name, Task_ID, Task_Description, Urgency, VIN, Make, Model,
            Mileage, Estimated_Standard_Time, Status, Date_Created
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.executemany(sql, records_to_insert)
        conn.commit()
        
        print(f"Successfully inserted {len(records_to_insert)} tasks for Job '{job_name}' into job_card.")
        return True
    except sqlite3.Error as e:
        print(f"Database error in create_job_from_ui_input: {e}")
        return False, f"Database error: {e}"
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # This simulates the data coming from the UI form
    print("--- Simulating UI Input for a 'Basic Service' Job ---")
    
    # The UI collects this data from the manager
    ui_job_name = "Intermediate Service"
    ui_vin = "UI-67890123456789"
    ui_make = "Range Rover"
    ui_model = "Range Rover Sport"
    ui_mileage = 900
    ui_urgency = "Low"
    
    # The UI code calls your function
    success = create_job_from_ui_input(
        job_name=ui_job_name,
        vin=ui_vin,
        make=ui_make,
        model=ui_model,
        mileage=ui_mileage,
        urgency=ui_urgency
    )'''
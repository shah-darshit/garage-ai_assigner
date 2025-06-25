# In core/db_setup.py
import sqlite3
import os

DATABASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database')
DATABASE_NAME = os.path.join(DATABASE_DIR, 'workshop.db')

def create_connection(db_file):
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def execute_sql(conn, sql_statement):
    try:
        c = conn.cursor()
        c.execute(sql_statement)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error executing SQL: {e}")

def setup_database():
    sql_create_job_history_table = """
    CREATE TABLE IF NOT EXISTS job_history (
        Job_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Job_Name TEXT,
        Task_Id TEXT NOT NULL,
        Task_Description TEXT,
        Status TEXT,
        Date_Completed DATE,
        Urgency TEXT,
        VIN TEXT,
        Make TEXT,
        Model TEXT,
        Mileage INTEGER,
        Engineer_Id TEXT,
        Engineer_Name TEXT,
        Engineer_Level TEXT,
        Time_Started DATETIME,
        Time_Ended DATETIME,
        Time_Taken_minutes INTEGER,
        Estimated_Standard_Time INTEGER,
        Outcome_Score INTEGER
    );
    """

    sql_create_job_card_table = """
    CREATE TABLE IF NOT EXISTS job_card (
        Job_Id TEXT,
        Job_Name TEXT,
        Task_Id TEXT NOT NULL,
        Task_Description TEXT,
        Status TEXT,
        Date_Created DATE,
        Urgency TEXT,
        VIN TEXT,
        Make TEXT,
        Model TEXT,
        Mileage INTEGER,
        Engineer_Id TEXT,
        Engineer_Name TEXT,
        Engineer_Level TEXT,
        Time_Started DATETIME,
        Estimated_Standard_Time INTEGER
    );
    """

    sql_create_engineer_profiles_table = """
    CREATE TABLE IF NOT EXISTS engineer_profiles (
        Engineer_ID TEXT PRIMARY KEY,
        Engineer_Name TEXT,
        Availability TEXT,
        Years_of_Experience INTEGER,
        Avg_Job_Completion_Time INTEGER,
        Specialization TEXT,
        Certifications TEXT,
        Customer_Rating REAL,
        Overall_Performance_Score INTEGER,
        Overall_Basic_Service_Score REAL,
        Overall_Intermediate_Service_Score REAL,
        Overall_Full_Service_Score REAL,
        Oil_Change_Score REAL,
        Oil_Filter_Replacement_Score REAL,
        Air_Filter_Check_Score REAL,
        Fluid_Levels_Check_Score REAL,
        Tyre_Pressure_Check_Score REAL,
        Visual_Inspection_Score REAL,
        Brake_Inspection_Score REAL,
        Tyre_Condition_and_Alignment_Check_Score REAL,
        Battery_Check_Score REAL,
        Exhaust_System_Inspection_Score REAL,
        Steering_and_Suspension_Check_Score REAL,
        Lights_and_Wipers_Check_Score REAL,
        Transmission_Check_Score REAL,
        Spark_Plugs_Replacement_Score REAL,
        Fuel_System_Inspection_Score REAL,
        Timing_Belt_Inspection_Score REAL,
        Comprehensive_Diagnostic_Check_Score REAL,
        Underbody_Inspection_Score REAL,
        Cabin_Filter_Replacement_Score REAL
    );
    """

    conn = create_connection(DATABASE_NAME)

    if conn is not None:

        print("Connecting to database to set up tables...")
        execute_sql(conn, "DROP TABLE IF EXISTS job_card;")
        execute_sql(conn, "DROP TABLE IF EXISTS job_task_mapping;")
        execute_sql(conn, "DROP TABLE IF EXISTS job_definitions;")
        execute_sql(conn, "DROP TABLE IF EXISTS task_definitions;")
        execute_sql(conn, sql_create_job_card_table)

        conn.close()
        print("Database setup complete.")
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    setup_database()
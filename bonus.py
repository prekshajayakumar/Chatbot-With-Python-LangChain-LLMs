import os
import openai
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Database setup
username = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
host = os.getenv("PG_HOST", "localhost")
port = os.getenv("PG_PORT", "5432")
database = os.getenv("PG_DATABASE", "postgres")

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Base = declarative_base()

# Validation functions for different field types
def validate_string(value):
    return isinstance(value, str) and len(value) > 0

def validate_integer(value):
    try:
        int_value = int(value)
        return isinstance(int_value, int)
    except ValueError:
        return False

def validate_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Dictionary to map field types to validation functions
validators = {
    "string": validate_string,
    "integer": validate_integer,
    "date": validate_date
}

# Function to create a table dynamically based on the schema
def create_task_table(task_type, task_schema):
    columns = [Column("id", Integer, primary_key=True)]
    for field in task_schema["fields"]:
        field_name = field["name"]
        field_type = field["type"]
        
        if field_type == "string":
            columns.append(Column(field_name, String))
        elif field_type == "integer":
            columns.append(Column(field_name, Integer))
        elif field_type == "date":
            columns.append(Column(field_name, Date))
    
    # Create a dynamic class for the task type
    task_table = type(f"{task_type.capitalize()}Task", (Base,), {"__tablename__": f"{task_type}_tasks", "id": columns[0], **dict(zip([col.name for col in columns[1:]], columns[1:]))})

    # Create table if not exists
    Base.metadata.create_all(engine)

# Function to insert task data into the database
def insert_task_data(task_type, task_data, task_schema):
    # Create the task table based on schema (if not created already)
    create_task_table(task_type, task_schema)
    
    # Insert task data into the table
    Session = sessionmaker(bind=engine)
    session = Session()
    
    task_table = Base.metadata.tables[f"{task_type}_tasks"]
    insert_data = {field["name"]: task_data.get(field["name"]) for field in task_schema["fields"]}
    
    session.execute(task_table.insert().values(insert_data))
    session.commit()
    session.close()

# Chatbot logic - dynamically handle any task type and fields
def chatbot():
    username = input("Hello! What's your name? ")
    print(f"Nice to meet you, {username}!")

    # Ask for the task type (task types are now fully dynamic)
    task_type = input("What kind of task would you like to complete? ")

    # Dynamic schema loading (you can replace this with loading from an external source)
    task_schema = {
        "fields": []
    }

    # Ask the user for task details
    print(f"Now, let's define the task '{task_type}'. Please enter the fields and their types.")
    while True:
        field_name = input("Enter the field name (or type 'done' to finish): ")
        if field_name.lower() == 'done':
            break
        
        field_type = input(f"Enter the type for the field '{field_name}' (options: string, integer, date): ").lower()
        if field_type not in validators:
            print("Invalid type. Please enter one of the following: string, integer, date.")
            continue
        
        task_schema["fields"].append({"name": field_name, "type": field_type})

    # Collect data based on the dynamic task schema
    task_data = {}
    for field in task_schema["fields"]:
        field_name = field["name"]
        field_type = field["type"]

        while True:
            field_value = input(f"Please enter {field_name} ({field_type}): ")

            # Validate the input
            if not validators[field_type](field_value):
                print(f"Invalid value for {field_name}. Please enter a valid {field_type}.")
                continue

            task_data[field_name] = field_value
            break

    # Insert collected task data into the database
    insert_task_data(task_type, task_data, task_schema)

    print(f"Your {task_type} task has been saved!")
    print("Collected Data:", task_data)

if __name__ == "__main__":
    chatbot()

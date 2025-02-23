import os
import openai
import psycopg2
import time
import getpass
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

# Load OpenAI API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.Client()

# Retrieve credentials securely
username = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
host = os.getenv("PG_HOST", "localhost")
port = os.getenv("PG_PORT", "5432")
database = os.getenv("PG_DATABASE", "postgres")

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define table schema
user_goals_table = Table(
    "user_goals", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("goal", String),
    Column("weightage", Integer)
)
metadata.create_all(engine)

# Maintain conversation context
conversation_history = []

def insert_goal(username, goal, weightage):
    """Insert user goal into the database."""
    with engine.connect() as conn:
        conn.execute(user_goals_table.insert().values(username=username, goal=goal, weightage=weightage))
        conn.commit()

def chatbot():
    llm = ChatOpenAI()
    username = input("Hello! What's your name? ")
    print(f"Nice to meet you, {username}! Let's define your goals.")
    
    total_weight = 0
    goals = []
    
    while total_weight != 100:
        goal = input("Enter a goal: ")
        weight = int(input("Enter weightage (ensure total sums to 100%): "))
        goals.append((goal, weight))
        conversation_history.append({"goal": goal, "weightage": weight})  # Store in conversation history
        total_weight = sum(w for _, w in goals)
        
        if total_weight > 100:
            print("Total exceeds 100%. Please adjust your inputs.")
            total_weight = 0
            goals = []
    
    # Store in database
    for goal, weight in goals:
        insert_goal(username, goal, weight)
    
    print("Your goals have been saved!")
    print("Conversation History:", conversation_history)  # Display conversation history
    exit()  # End the program after saving goals

if __name__ == "__main__":
    chatbot()

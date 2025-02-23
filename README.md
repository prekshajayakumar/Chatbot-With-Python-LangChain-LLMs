# Chatbot
## Setup Instructions
1. Clone the repository: `git clone <repo_url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the `.env` file (see `.env.example` for the required variables).
4. Run the application: `python chatbot.py`
5. Run the application: `python bonus.py` for the bonus

## Database Setup
1. Create a PostgreSQL database and run the `schema.sql` script to create the necessary tables.
2. Update the `.env` file with your database connection details.

## Using the Chatbot
- The chatbot collects user goals, assigns weightage (ensuring a total of 100%), and stores the data in PostgreSQL.

## Bonus: Generic Agent
- The chatbot can use a flexible agent to adjust its behavior based on a schema, allowing it to interact dynamically with users.
-The chatbot allows users to define tasks with customizable fields. You can specify the type of data for each field (e.g., string, integer, or date) and then enter the data.
The chatbot will validate the inputs based on the field types and store the task data in the PostgreSQL database.

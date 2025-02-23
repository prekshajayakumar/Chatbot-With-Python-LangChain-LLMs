# Chatbot
## Setup Instructions
1. Clone the repository: `git clone <repo_url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the `.env` file (see `.env.example` for the required variables).
4. Run the application: `python chatbot.py`

## Database Setup
1. Create a PostgreSQL database and run the `schema.sql` script to create the necessary tables.
2. Update the `.env` file with your database connection details.

## Using the Chatbot
- The chatbot collects user goals, assigns weightage (ensuring a total of 100%), and stores the data in PostgreSQL.


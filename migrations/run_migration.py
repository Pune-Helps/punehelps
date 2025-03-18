import mysql.connector
import os
import sys

# Database connection parameters
DB_USERNAME = "admin"
DB_PASSWORD = "Pune9^0!"
DB_HOST = "ph-db-2.cpukwqkiuiyg.us-east-2.rds.amazonaws.com"
DB_PORT = "3306"
DB_NAME = "pune_seva"

def run_migration():
    # Connect to the database
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        cursor = conn.cursor()
        print("Connected to database successfully!")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)
    
    # Read the SQL script
    try:
        with open('add_categories_table.sql', 'r') as file:
            sql_script = file.read()
    except Exception as e:
        print(f"Error reading SQL file: {e}")
        sys.exit(1)
    
    # Execute each SQL statement
    statements = sql_script.split(';')
    
    try:
        for statement in statements:
            if statement.strip():
                print(f"\nExecuting: {statement[:100]}...")
                cursor.execute(statement)
                print("Statement executed successfully!")
        
        # Commit changes
        conn.commit()
        print("\nAll SQL statements executed successfully!")
    except Exception as e:
        print(f"Error executing SQL: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Change to the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Starting database migration...")
    run_migration()
    print("Migration completed successfully!")

import os
import re
import pymysql
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

# Database configuration using environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_user_input():
    user_input = input('Enter your name: ').strip()

    # Input validation (letters and spaces only)
    if not user_input or not re.match(r'^[A-Za-z\s]+$', user_input):
        print("Invalid input")
        return None

    return user_input


def send_email(to, subject, body):
    
    try:
        # Basic sanitization to reduce shell injection risk
        safe_body = body.replace('"', '').replace("'", "")
        os.system(f'echo "{safe_body}" | mail -s "{subject}" {to}')
    except Exception as e:
        print("Error sending email:", e)


def get_data():
    url = 'https://insecure-api.com/get-data'  # Changed to HTTPS
    try:
        response = urlopen(url)
        data = response.read().decode()
        return data
    except HTTPError as e:
        print("HTTP Error:", e.code)
    except URLError as e:
        print("URL Error:", e.reason)
    except Exception as e:
        print("Unexpected error:", e)

    return  None


def save_to_db(data):
    if not data:
        print("No data to save.")
        return

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Parameterized query (prevents SQL injection)
        query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
        cursor.execute(query, (data, 'Another Value'))

        connection.commit()
        print("Data saved successfully")

    except Exception as e:
        print("Database error:", e)

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass


if __name__ == '__main__':
    user_input = get_user_input()

    # Stop execution if input invalid
    if not user_input:
        exit()

    data = get_data()
    save_to_db(data)

    send_email('admin@example.com', 'User Input', user_input)

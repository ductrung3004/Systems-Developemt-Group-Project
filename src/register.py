from db import get_db_connection
from pwhash import hash_password

def register_user(username, password, first_name, last_name, email, role_name="Tenant"):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get role_id
        cursor.execute("SELECT role_id FROM roles WHERE role_name = %s", (role_name,))
        role = cursor.fetchone()

        if not role:
            return "Role not found"

        role_id = role[0]

        # Hash password and store it as UTF-8 string
        hashed_pw = hash_password(password)

        # Insert user
        cursor.execute("""
            INSERT INTO users
            (role_id, username, password_hash, first_name, last_name, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (role_id, username, hashed_pw, first_name, last_name, email))

        conn.commit()
        return "Success"

    except Exception as e:
        return str(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

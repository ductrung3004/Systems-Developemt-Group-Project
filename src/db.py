import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Database Username
        password="Bao200304", # Database password
        database="paragon_db"
    )

# --- STAFF MANAGEMENT QUERIES ---

def get_all_staff():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ni, name, role, status FROM staff")
    staff = cursor.fetchall()
    conn.close()
    return staff

def add_staff(ni, name, role, status="Active"):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO staff (ni, name, role, status) VALUES (%s, %s, %s, %s)", 
                       (ni, name, role, status))
        conn.commit()
        success = True
    except:
        success = False 
    finally:
        conn.close()
    return success

def delete_staff(ni):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM staff WHERE ni = %s", (ni,))
    conn.commit()
    conn.close()

def update_staff(ni, new_name, new_role, new_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE staff SET name = %s, role = %s, status = %s WHERE ni = %s", 
                   (new_name, new_role, new_status, ni))
    conn.commit()
    conn.close()

# --- RESIDENT APPROVAL QUERIES ---

def get_pending_residents():
    """Fetches Tenants (role 6) whose accounts are Inactive."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT user_id, CONCAT(first_name, ' ', last_name) AS name, created_at 
        FROM users 
        WHERE role_id = 6 AND account_status = 'Inactive'
    """
    cursor.execute(query)
    pending_users = cursor.fetchall()
    conn.close()
    return pending_users

def approve_resident(user_id):
    """Changes a user's status to Active."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET account_status = 'Active' WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()

def reject_resident(user_id):
    """Deletes the rejected user from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()
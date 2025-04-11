import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# MySQL Configuration
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password',
            database='respirex_db',
            auth_plugin='mysql_native_password'
        )
        return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        return None

# Create users table if not exists
conn = get_db_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL
                    )''')
    conn.commit()
    cursor.close()
    conn.close()

def register():
    email = email_entry.get()
    password = password_entry.get()
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Registration Successful! Please Login.")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")
    else:
        messagebox.showerror("Error", "Database connection failed!")

def login():
    email = email_entry.get()
    password = password_entry.get()
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            messagebox.showinfo("Success", "Login Successful!")
        else:
            messagebox.showerror("Error", "Invalid Credentials!")
    else:
        messagebox.showerror("Error", "Database connection failed!")

# Tkinter UI Setup
root = tk.Tk()
root.title("RespireX Login/Register")
root.geometry("300x250")

tk.Label(root, text="RespireX", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=login).pack(pady=5)
tk.Button(root, text="Register", command=register).pack()

root.mainloop()
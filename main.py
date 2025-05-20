import customtkinter as ctk
import sqlite3

import bcrypt
from tkinter import messagebox

# --- Global user variable ---
current_user = None

# --- Login Frame ---
class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=20)
        self.analyst_entry = ctk.CTkEntry(self, placeholder_text="Analyst ID", width=300, height=40, font=ctk.CTkFont(size=16))
        self.analyst_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=300, height=40, font=ctk.CTkFont(size=16))
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login, width=200, height=40, font=ctk.CTkFont(size=16)).pack(pady=20)
        ctk.CTkButton(self, text="Sign up", command=self.signup, width=200, height=40, font=ctk.CTkFont(size=16)).pack(pady=20)

    def login(self):
        global current_user
        analyst_id = self.analyst_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE analyst_id=?", (analyst_id,))
        result = cur.fetchone()
        conn.close()

        if result and bcrypt.checkpw(password.encode(), result[2].encode()):
            current_user = {"id": result[0], "analyst_id": result[1]}
            self.app.show_main_frame()
            return

        messagebox.showerror("Login Failed", "Invalid analyst ID or password.")

    def signup(self):
        analyst_id = self.analyst_entry.get()
        password = self.password_entry.get()

        if not analyst_id or not password:
            messagebox.showerror("Signup Failed", "Please fill in all fields.")
            return

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE analyst_id=?", (analyst_id,))
        if cur.fetchone():
            messagebox.showerror("Signup Failed", "Analyst ID already exists.")
            conn.close()
            return
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cur.execute("INSERT INTO users (analyst_id, password) VALUES (?, ?)", (analyst_id, hashed_password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Signup Success", "User added.")

# --- Main Frame ---
class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=24))
        self.label.pack(pady=40)

    def update_user(self):
        global current_user
        self.label.configure(text=f"Welcome, {current_user['analyst_id']}!")

# --- Main App ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Analyst Login App")
        self.geometry("500x400")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.login_frame = LoginFrame(self, self)
        self.main_frame = MainFrame(self)

        self.login_frame.pack(fill="both", expand=True)

    def show_main_frame(self):
        self.login_frame.pack_forget()
        self.main_frame.update_user()
        self.main_frame.pack(fill="both", expand=True)

# --- Main ---
if __name__ == "__main__":
    app = App()
    app.mainloop()

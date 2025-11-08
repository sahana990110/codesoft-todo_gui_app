#!/usr/bin/env python3
"""
To-Do List GUI Application
A graphical user interface for task management with file persistence.
Features: Login system, task editing, and professional UI design.
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from typing import List, Dict, Any
import hashlib


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List - Login")
        self.root.geometry("450x550")
        self.root.configure(bg='#ecf0f1')
        self.root.resizable(False, False)
        
        self.users_file = "users.json"
        self.current_user = None
        self.is_signup = False
        
        self.load_users()
        self.center_window()
        self.create_ui()
    
    def center_window(self):
        """Center window on screen."""
        self.root.update_idletasks()
        width, height = 450, 550
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_users(self):
        """Load user credentials."""
        self.users = {}
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
    
    def save_users(self):
        """Save user credentials."""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
    
    def hash_password(self, password):
        """Hash password."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def clear_ui(self):
        """Clear all widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_ui(self):
        """Create the user interface (login or signup)."""
        self.clear_ui()
        
        # Header
        header_color = '#27ae60' if self.is_signup else '#2c3e50'
        header_text = "Create Account" if self.is_signup else "Welcome Back"
        
        header = tk.Frame(self.root, bg=header_color, height=100)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="📝 To-Do List", font=("Segoe UI", 28, "bold"), 
                bg=header_color, fg='white').pack(pady=(15, 5))
        tk.Label(header, text=header_text, font=("Segoe UI", 12), 
                bg=header_color, fg='#ecf0f1').pack()
        
        # Form
        form = tk.Frame(self.root, bg='white')
        form.pack(fill='both', expand=True, padx=40, pady=25)
        
        title_text = "Create Your Account" if self.is_signup else "Sign In"
        tk.Label(form, text=title_text, font=("Segoe UI", 16, "bold"), 
                bg='white', fg='#2c3e50').pack(pady=(0, 25))
        
        # Username
        tk.Label(form, text="Username" + (" (min 3)" if self.is_signup else ""), 
                font=("Segoe UI", 10, "bold"), bg='white', fg='#34495e', anchor='w').pack(fill='x', pady=(0, 5))
        self.username_entry = tk.Entry(form, font=("Segoe UI", 11), bg='#ecf0f1', 
                                       fg='#2c3e50', relief='flat', bd=5, insertbackground='#2c3e50')
        self.username_entry.pack(fill='x', ipady=10, pady=(0, 15))
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus_set())
        
        # Password
        tk.Label(form, text="Password" + (" (min 4)" if self.is_signup else ""), 
                font=("Segoe UI", 10, "bold"), bg='white', fg='#34495e', anchor='w').pack(fill='x', pady=(0, 5))
        self.password_entry = tk.Entry(form, font=("Segoe UI", 11), bg='#ecf0f1', 
                                       fg='#2c3e50', show='•', relief='flat', bd=5, insertbackground='#2c3e50')
        self.password_entry.pack(fill='x', ipady=10, pady=(0, 15))
        
        # Confirm password (only for signup)
        self.confirm_password_entry = None
        if self.is_signup:
            tk.Label(form, text="Confirm Password", font=("Segoe UI", 10, "bold"), 
                    bg='white', fg='#34495e', anchor='w').pack(fill='x', pady=(0, 5))
            self.confirm_password_entry = tk.Entry(form, font=("Segoe UI", 11), bg='#ecf0f1', 
                                                   fg='#2c3e50', show='•', relief='flat', bd=5, insertbackground='#2c3e50')
            self.confirm_password_entry.pack(fill='x', ipady=10, pady=(0, 20))
            self.confirm_password_entry.bind('<Return>', lambda e: self.register())
            self.password_entry.bind('<Return>', lambda e: self.confirm_password_entry.focus_set())
        else:
            self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Button
        btn_text = "Sign Up" if self.is_signup else "Sign In"
        btn_color = '#27ae60' if self.is_signup else '#3498db'
        btn_cmd = self.register if self.is_signup else self.login
        btn = tk.Button(form, text=btn_text, command=btn_cmd, font=("Segoe UI", 11, "bold"),
                       bg=btn_color, fg='white', relief='flat', cursor='hand2', pady=10)
        btn.pack(fill='x', pady=(0, 15))
        
        # Switch link
        switch_text = "Already have an account? Sign In" if self.is_signup else "Don't have an account? Sign Up"
        switch_frame = tk.Frame(form, bg='white')
        switch_frame.pack(fill='x')
        tk.Label(switch_frame, text=switch_text.split('?')[0] + "?", 
                font=("Segoe UI", 9), bg='white', fg='#7f8c8d').pack(side='left')
        link = tk.Label(switch_frame, text=switch_text.split('?')[1].strip(), 
                       font=("Segoe UI", 9, "bold", "underline"), bg='white', fg='#3498db', cursor='hand2')
        link.pack(side='left', padx=5)
        link.bind('<Button-1>', lambda e: self.toggle_mode())
        
        self.username_entry.focus_set()
    
    def toggle_mode(self):
        """Switch between login and signup."""
        self.is_signup = not self.is_signup
        self.create_ui()
    
    def login(self):
        """Handle login."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
        
        if username not in self.users:
            if messagebox.askyesno("Not Found", f"Username '{username}' not found.\nCreate new account?"):
                self.is_signup = True
                self.create_ui()
                self.username_entry.insert(0, username)
            return
        
        if self.users[username]['password'] != self.hash_password(password):
            messagebox.showerror("Error", "Incorrect password!")
            self.password_entry.delete(0, tk.END)
            return
        
        self.current_user = username
        messagebox.showinfo("Success", f"Welcome, {username}!")
        self.root.quit()
    
    def register(self):
        """Handle registration."""
        if not self.is_signup or not self.confirm_password_entry:
            messagebox.showerror("Error", "Please use the Sign Up page!")
            return
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_password_entry.get()
        
        # Validate
        if not username:
            messagebox.showerror("Error", "Please enter username!")
            self.username_entry.focus_set()
            return
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters!")
            self.username_entry.focus_set()
            return
        if not password:
            messagebox.showerror("Error", "Please enter password!")
            self.password_entry.focus_set()
            return
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters!")
            self.password_entry.focus_set()
            return
        if not confirm:
            messagebox.showerror("Error", "Please confirm your password!")
            self.confirm_password_entry.focus_set()
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            self.password_entry.focus_set()
            return
        if username in self.users:
            messagebox.showerror("Error", "Username already exists!")
            self.username_entry.focus_set()
            return
        
        # Create account
        self.users[username] = {
            'password': self.hash_password(password),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_users()
        messagebox.showinfo("Success", f"Account created!\nWelcome, {username}!")
        
        # Switch to login
        self.is_signup = False
        self.create_ui()
        self.username_entry.insert(0, username)
        self.password_entry.focus_set()
    
    def get_current_user(self):
        """Get logged-in user."""
        return self.current_user


class TodoGUIApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"📝 To-Do List Application - {username}")
        # Start with a larger default size, enforce a minimum and open maximized
        self.root.geometry("1200x800")
        self.root.configure(bg='#ecf0f1')
        self.root.resizable(True, True)
        # Prevent window from being too small so bottom/action buttons remain visible
        self.root.minsize(1000, 700)  # Set minimum window size
        # Start maximized on Windows to ensure all controls are visible on most displays
        try:
            self.root.state('zoomed')
        except Exception:
            pass
        
        # Data
        self.filename = f"tasks_{username}.txt"
        self.tasks = []
        self.current_filter = None  # Track current filter state
        
        # Load existing tasks
        self.load_tasks()
        
        # Create GUI elements
        self.create_widgets()
        self.refresh_task_list()
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def load_tasks(self):
        """Load tasks from file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    self.tasks = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")
    
    def create_widgets(self):
        """Create all GUI widgets with professional styling."""
        # Header frame with title and user info
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="📝 To-Do List Manager", 
            font=("Segoe UI", 24, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(side='left', padx=30, pady=20)
        
        # User info and logout button
        user_frame = tk.Frame(header_frame, bg='#2c3e50')
        user_frame.pack(side='right', padx=30, pady=20)
        
        user_label = tk.Label(
            user_frame,
            text=f"👤 {self.username}",
            font=("Segoe UI", 11),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        user_label.pack(side='left', padx=(0, 15))
        
        logout_btn = tk.Button(
            user_frame,
            text="🚪 Logout",
            command=self.logout,
            font=("Segoe UI", 9, "bold"),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5
        )
        logout_btn.pack(side='left')
        
        # Main container frame
        main_container = tk.Frame(self.root, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=20, pady=(20, 80))  # Add bottom padding
        
        # Add task section
        add_section = tk.Frame(main_container, bg='#ffffff', relief='flat', bd=0)
        add_section.pack(fill='x', pady=(0, 15))
        
        # Add task header
        add_header = tk.Frame(add_section, bg='#3498db', height=40)
        add_header.pack(fill='x')
        add_header.pack_propagate(False)
        
        tk.Label(
            add_header,
            text="➕ Add New Task",
            font=("Segoe UI", 12, "bold"),
            bg='#3498db',
            fg='white'
        ).pack(side='left', padx=15, pady=10)
        
        # Add task input area
        add_input_area = tk.Frame(add_section, bg='#ffffff')
        add_input_area.pack(fill='x', padx=20, pady=20)
        
        input_container = tk.Frame(add_input_area, bg='#ffffff')
        input_container.pack(fill='x')
        
        self.task_entry = tk.Entry(
            input_container,
            font=("Segoe UI", 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            relief='flat',
            insertbackground='#2c3e50',
            bd=5
        )
        self.task_entry.pack(side='left', fill='x', expand=True, ipady=10, padx=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        add_button = tk.Button(
            input_container, 
            text="Add Task", 
            command=self.add_task,
            bg='#3498db',
            fg='white',
            font=("Segoe UI", 11, "bold"),
            activebackground='#2980b9',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=10
        )
        add_button.pack(side='left')
        
        # Task list section
        list_section = tk.Frame(main_container, bg='#ffffff', relief='flat', bd=0)
        list_section.pack(fill='both', expand=True, pady=(0, 15))
        
        # Task list header
        list_header = tk.Frame(list_section, bg='#34495e', height=40)
        list_header.pack(fill='x')
        list_header.pack_propagate(False)
        
        tk.Label(
            list_header,
            text="📋 Your Tasks",
            font=("Segoe UI", 12, "bold"),
            bg='#34495e',
            fg='white'
        ).pack(side='left', padx=15, pady=10)
        
        # Treeview container
        tree_container = tk.Frame(list_section, bg='#ffffff')
        tree_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create treeview for tasks with custom style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', 
                       background='#ffffff',
                       foreground='#2c3e50',
                       fieldbackground='#ffffff',
                       font=('Segoe UI', 10),
                       rowheight=35)
        style.configure('Treeview.Heading',
                       background='#34495e',
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        style.map('Treeview',
                 background=[('selected', '#3498db')],
                 foreground=[('selected', 'white')])
        
        columns = ('ID', 'Status', 'Task', 'Created')
        self.task_tree = ttk.Treeview(tree_container, columns=columns, show='headings', height=12, selectmode='extended')
        
        # Configure columns with proper widths - all centered
        self.task_tree.heading('ID', text='ID')
        self.task_tree.heading('Status', text='Status')
        self.task_tree.heading('Task', text='Task Description')
        self.task_tree.heading('Created', text='Created At')
        
        self.task_tree.column('ID', width=80, anchor='center', minwidth=80)
        self.task_tree.column('Status', width=150, anchor='center', minwidth=150)
        self.task_tree.column('Task', width=450, anchor='center', minwidth=250)
        self.task_tree.column('Created', width=200, anchor='center', minwidth=180)
        
        # Scrollbar for task list
        scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        self.task_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # allow double-click to edit
        self.task_tree.bind('<Double-1>', lambda e: self.on_tree_double_click(e))
        
        # Bind Delete key for quick deletion
        self.task_tree.bind('<Delete>', lambda e: self.delete_task())
        self.root.bind('<Delete>', lambda e: self.delete_task() if self.task_tree.focus() else None)
        
        # Bind keyboard shortcuts for pending
        self.task_tree.bind('<Control-p>', lambda e: self.mark_task_pending())
        self.root.bind('<Control-p>', lambda e: self.mark_task_pending() if self.task_tree.focus() else None)
        
        # Bind keyboard shortcuts for mark done
        self.task_tree.bind('<Control-d>', lambda e: self.mark_task_done())
        self.root.bind('<Control-d>', lambda e: self.mark_task_done() if self.task_tree.focus() else None)
        
        # Bind keyboard shortcuts for filters
        self.root.bind('<Control-Shift-d>', lambda e: self.filter_done())
        self.root.bind('<Control-Shift-p>', lambda e: self.filter_pending())
        self.root.bind('<Control-Shift-a>', lambda e: self.show_all_tasks())
        
        # Bind keyboard shortcut for edit
        self.task_tree.bind('<Control-e>', lambda e: self.edit_task())
        self.root.bind('<Control-e>', lambda e: self.edit_task() if self.task_tree.focus() else None)
        self.task_tree.bind('<F2>', lambda e: self.edit_task())  # F2 is a common edit shortcut
        
        # Task Actions section - Place it right below the task list
        action_section = tk.Frame(main_container, bg='#ffffff', relief='flat', bd=0)
        action_section.pack(fill='x', pady=10)  # Reduced padding
        
        # Task Actions header
        action_header = tk.Frame(action_section, bg='#95a5a6', height=40)
        action_header.pack(fill='x')
        action_header.pack_propagate(False)
        
        tk.Label(
            action_header,
            text="⚙️ Task Actions",
            font=("Segoe UI", 12, "bold"),
            bg='#95a5a6',
            fg='white'
        ).pack(side='left', padx=15, pady=10)
        
        # Action buttons in a single row
        button_container = tk.Frame(action_section, bg='#ffffff')
        button_container.pack(fill='x', padx=20, pady=10)  # Reduced padding
        
        # Common button style
        btn_style = {
            'font': ("Segoe UI", 10, "bold"),
            'relief': 'flat',
            'cursor': 'hand2',
            'pady': 8,
            'padx': 15
        }
        
        # All buttons in a single row
        tk.Button(
            button_container,
            text="✏️ Edit",
            command=self.edit_task,
            bg='#3498db',
            fg='white',
            **btn_style
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_container,
            text="✅ Done",
            command=self.mark_task_done,
            bg='#27ae60',
            fg='white',
            **btn_style
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_container,
            text="⏳ Pending",
            command=self.mark_task_pending,
            bg='#f39c12',
            fg='white',
            **btn_style
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_container,
            text="🗑️ Delete",
            command=self.delete_task,
            bg='#e74c3c',
            fg='white',
            **btn_style
        ).pack(side='left', padx=5)
        
        # Separator
        tk.Label(
            button_container,
            text="|",
            bg='#ffffff',
            fg='#95a5a6',
            font=("Segoe UI", 12)
        ).pack(side='left', padx=15)
        
        # Filter buttons
        tk.Button(
            button_container,
            text="✅ Show Done",
            command=self.filter_done,
            bg='#9b59b6',
            fg='white',
            **btn_style
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_container,
            text="⏳ Show Pending",
            command=self.filter_pending,
            bg='#f39c12',
            fg='white',
            **btn_style
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_container,
            text="👀 Show All",
            command=self.show_all_tasks,
            bg='#34495e',
            fg='white',
            **btn_style
        ).pack(side='left', padx=5)
        
        # Statistics section
        stats_section = tk.Frame(main_container, bg='#ffffff', relief='flat', bd=0)
        stats_section.pack(fill='x')
        
        stats_header = tk.Frame(stats_section, bg='#16a085', height=40)
        stats_header.pack(fill='x')
        stats_header.pack_propagate(False)
        
        tk.Label(
            stats_header,
            text="📊 Statistics",
            font=("Segoe UI", 12, "bold"),
            bg='#16a085',
            fg='white'
        ).pack(side='left', padx=15, pady=10)
        
        stats_content = tk.Frame(stats_section, bg='#ffffff')
        stats_content.pack(fill='x', padx=20, pady=15)
        
        self.stats_label = tk.Label(
            stats_content,
            text="",
            font=("Segoe UI", 11),
            bg='#ffffff',
            fg='#2c3e50',
            anchor='w'
        )
        self.stats_label.pack(fill='x')
        
        # Bottom action bar (anchored to window bottom) - duplicates main controls for easier access
        bottom_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        bottom_frame.pack(side='bottom', fill='x')
        bottom_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Create inner frame for buttons
        button_frame = tk.Frame(bottom_frame, bg='#2c3e50')
        button_frame.pack(expand=True, pady=10)
        
        # Common button style
        btn_style = {
            'font': ("Segoe UI", 9, "bold"),
            'relief': 'flat',
            'cursor': 'hand2',
            'pady': 5,
            'padx': 10
        }
        
        # Left side action buttons
        left_frame = tk.Frame(button_frame, bg='#2c3e50')
        left_frame.pack(side='left', padx=20)
        
        tk.Button(left_frame, text="✏️ Edit", command=self.edit_task,
                 bg='#3498db', fg='white', **btn_style).pack(side='left', padx=2)
        
        tk.Button(left_frame, text="✅ Done", command=self.mark_task_done,
                 bg='#27ae60', fg='white', **btn_style).pack(side='left', padx=2)
        
        tk.Button(left_frame, text="⏳ Pending", command=self.mark_task_pending,
                 bg='#f39c12', fg='white', **btn_style).pack(side='left', padx=2)
        
        tk.Button(left_frame, text="🗑️ Delete", command=self.delete_task,
                 bg='#e74c3c', fg='white', **btn_style).pack(side='left', padx=2)
        
        # Separator
        tk.Label(button_frame, text="|", bg='#2c3e50', fg='#95a5a6').pack(side='left', padx=10)
        
        # Right side filter buttons
        right_frame = tk.Frame(button_frame, bg='#2c3e50')
        right_frame.pack(side='left')
        
        tk.Button(right_frame, text="✅ Done", command=self.filter_done,
                 bg='#9b59b6', fg='white', **btn_style).pack(side='left', padx=2)
        
        tk.Button(right_frame, text="⏳ Pending", command=self.filter_pending,
                 bg='#f39c12', fg='white', **btn_style).pack(side='left', padx=2)
        
        tk.Button(right_frame, text="👀 All", command=self.show_all_tasks,
                 bg='#34495e', fg='white', **btn_style).pack(side='left', padx=2)
        
        # Update statistics
        self.update_statistics()
    
    def add_task(self):
        """Add a new task."""
        task_name = self.task_entry.get().strip()
        if not task_name:
            messagebox.showwarning("Warning", "Please enter a task name!")
            return
        
        # Generate unique ID
        max_id = max([task['id'] for task in self.tasks], default=0)
        
        task = {
            'id': max_id + 1,
            'name': task_name,
            'status': 'Not Done',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        # Reset filter to show all tasks when adding new task
        self.current_filter = None
        self.refresh_task_list(None)
        self.update_statistics()
        
        messagebox.showinfo("Success", f"Task '{task_name}' added successfully!")
    
    def refresh_task_list(self, filter_status=None):
        """Refresh the task list display."""
        # Update current filter if a new filter is provided
        if filter_status is not None:
            self.current_filter = filter_status
        
        # Use current filter for display
        active_filter = self.current_filter
        
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Add tasks to treeview
        for task in self.tasks:
            if active_filter is None or task['status'] == active_filter:
                status_icon = "✅ Done" if task['status'] == 'Done' else "⏳ Pending"
                self.task_tree.insert('', 'end', values=(
                    task['id'],
                    status_icon,
                    task['name'],
                    task['created_at']
                ))
    
    def edit_task(self):
        """Edit selected task."""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to edit!")
            return
        if len(selection) > 1:
            messagebox.showwarning("Warning", "Please select only one task to edit!")
            return
        
        item = self.task_tree.item(selection[0])
        task_id = int(item['values'][0])
        current_task_name = item['values'][2]
        
        # Find the task
        task = None
        for t in self.tasks:
            if t['id'] == task_id:
                task = t
                break
        
        if not task:
            messagebox.showerror("Error", "Task not found!")
            return
        
        # Create edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("500x200")
        edit_window.configure(bg='#ecf0f1')
        edit_window.resizable(False, False)
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Center the edit window
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (200 // 2)
        edit_window.geometry(f"500x200+{x}+{y}")
        
        # Edit form
        form_frame = tk.Frame(edit_window, bg='#ecf0f1')
        form_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        tk.Label(
            form_frame,
            text="Edit Task:",
            font=("Segoe UI", 12, "bold"),
            bg='#ecf0f1',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 10))
        
        task_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            bg='white',
            fg='#2c3e50',
            relief='flat',
            insertbackground='#2c3e50',
            bd=5
        )
        task_entry.pack(fill='x', ipady=10, pady=(0, 20))
        task_entry.insert(0, current_task_name)
        task_entry.select_range(0, tk.END)
        task_entry.focus_set()
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='#ecf0f1')
        button_frame.pack(fill='x')
        
        def save_edit():
            new_name = task_entry.get().strip()
            if not new_name:
                messagebox.showwarning("Warning", "Task name cannot be empty!")
                return
            
            task['name'] = new_name
            self.save_tasks()
            # Refresh with current filter
            self.refresh_task_list(self.current_filter)
            self.update_statistics()
            edit_window.destroy()
            messagebox.showinfo("Success", "Task updated successfully!")
        
        save_btn = tk.Button(
            button_frame,
            text="Save",
            command=save_edit,
            bg='#3498db',
            fg='white',
            font=("Segoe UI", 10, "bold"),
            activebackground='#2980b9',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=8
        )
        save_btn.pack(side='right', padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=edit_window.destroy,
            bg='#95a5a6',
            fg='white',
            font=("Segoe UI", 10, "bold"),
            activebackground='#7f8c8d',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=8
        )
        cancel_btn.pack(side='right')
        
        task_entry.bind('<Return>', lambda e: save_edit())
    
    def mark_task_done(self):
        """Mark selected task as done."""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to mark as done!")
            return
        
        item = self.task_tree.item(selection[0])
        task_id = int(item['values'][0])
        
        for task in self.tasks:
            if task['id'] == task_id:
                if task['status'] == 'Done':
                    messagebox.showinfo("Info", "Task is already marked as done!")
                else:
                    task['status'] = 'Done'
                    self.save_tasks()
                    # Refresh with current filter
                    self.refresh_task_list(self.current_filter)
                    self.update_statistics()
                    messagebox.showinfo("Success", f"Task '{task['name']}' marked as done!")
                return
    
    def mark_task_pending(self):
        """Mark selected task as pending."""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to mark as pending!")
            return
        
        item = self.task_tree.item(selection[0])
        task_id = int(item['values'][0])
        
        for task in self.tasks:
            if task['id'] == task_id:
                if task['status'] == 'Not Done':
                    messagebox.showinfo("Info", "Task is already marked as pending!")
                else:
                    task['status'] = 'Not Done'
                    self.save_tasks()
                    # Refresh with current filter
                    self.refresh_task_list(self.current_filter)
                    self.update_statistics()
                    messagebox.showinfo("Success", f"Task '{task['name']}' marked as pending!")
                return
    
    def delete_task(self):
        """Delete selected task(s)."""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select at least one task to delete!")
            return
        
        task_ids = []
        task_names = []
        for sel in selection:
            item = self.task_tree.item(sel)
            task_ids.append(int(item['values'][0]))
            task_names.append(item['values'][2])
        
        count = len(task_ids)
        names_preview = ", ".join(task_names[:5]) + (", ..." if len(task_names) > 5 else "")
        result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {count} task(s)?\n{names_preview}")
        if result:
            # Remove tasks by id
            id_set = set(task_ids)
            self.tasks = [task for task in self.tasks if task['id'] not in id_set]
            
            # Reassign IDs
            for i, task in enumerate(self.tasks, 1):
                task['id'] = i
            
            self.save_tasks()
            # Refresh with current filter
            self.refresh_task_list(self.current_filter)
            self.update_statistics()
            messagebox.showinfo("Success", f"Deleted {count} task(s) successfully!")
    
    def filter_done(self):
        """Show only completed tasks."""
        self.current_filter = 'Done'
        self.refresh_task_list('Done')
    
    def filter_pending(self):
        """Show only pending tasks."""
        self.current_filter = 'Not Done'
        self.refresh_task_list('Not Done')
    
    def show_all_tasks(self):
        """Show all tasks."""
        self.current_filter = None
        self.refresh_task_list(None)
    
    def update_statistics(self):
        """Update statistics display."""
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task['status'] == 'Done'])
        pending_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        stats_text = (f"📊 Total Tasks: {total_tasks}  |  "
                     f"✅ Completed: {completed_tasks}  |  "
                     f"⏳ Pending: {pending_tasks}  |  "
                     f"📈 Completion Rate: {completion_rate:.1f}%")
        self.stats_label.config(text=stats_text)
    
    def logout(self):
        """Handle user logout."""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.save_tasks()
            self.root.destroy()
            # Restart application with login window
            main()
    
    def on_closing(self):
        """Handle application closing."""
        self.save_tasks()
        self.root.destroy()
    
    def on_tree_double_click(self, event):
        """Open edit dialog on double-click (single item required)."""
        # allow the event to set selection; then call edit if single
        sel = self.task_tree.selection()
        if len(sel) == 1:
            self.edit_task()
        elif len(sel) > 1:
            messagebox.showwarning("Warning", "Double-clicked multiple items — select only one to edit.")


def main():
    # Create login window
    login_root = tk.Tk()
    login_window = LoginWindow(login_root)
    login_root.mainloop()
    
    # Get logged-in user
    username = login_window.get_current_user()
    
    # Launch main application
    if username:
        root = tk.Tk()
        app = TodoGUIApp(root, username)
        root.mainloop()


if __name__ == "__main__":
    main()

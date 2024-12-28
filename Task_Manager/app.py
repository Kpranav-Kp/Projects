import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.sql import func
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize Flask app
app = Flask(__name__)

# Configure the app for SQLAlchemy
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'final.db')  # Database location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Session(app)

# Initialize the database
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    progress = db.Column(db.String(20), nullable=False, default="Not Completed")
    deadline = db.Column(db.DateTime, nullable=False)
    start = db.Column(db.DateTime, nullable=False, default=func.now())
    priority = db.Column(db.String(10), nullable=True, default="NONE")
    finish = db.Column(db.DateTime, nullable=True)
    submission = db.Column(db.String(20), nullable=True)

    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

# Index Route
@app.route("/")
def index():
    # If a user is logged in
    if "user_id" in session:
        user_id = session["user_id"]
        
        # Fetch user details
        user = User.query.get(user_id)
        if not user:
            return redirect("/login")

        username = user.username
        
        # Fetch all tasks for the user
        tasks = Task.query.filter_by(user_id=user_id, progress="Not Completed").all()
        
        # Fetch all task details
        details = Task.query.filter_by(user_id=user_id).all()
        
        # Count tasks based on progress
        current_tasks = Task.query.filter_by(user_id=user_id, progress="Not Completed").count()
        completed_tasks = Task.query.filter_by(user_id=user_id, progress="Completed").count()
        successful_tasks = Task.query.filter_by(user_id=user_id, progress="Completed", submission="On Time").count()
        
        # Fetch the next upcoming task
        upcoming_task = (
            Task.query.filter_by(user_id=user_id, progress="Not Completed")
            .order_by(Task.deadline)
            .first()
        )
        upcoming = upcoming_task.name if upcoming_task else "NONE"
        
        # Fetch the highest priority task
        priority_task = Task.query.filter_by(user_id=user_id, priority="TOP").first()
        priority = priority_task.name if priority_task else "NONE"
        
        # Calculate success percentage
        success = round((successful_tasks / completed_tasks) * 100, 2) if completed_tasks > 0 else 0.0
        
        # Render the index page with context
        return render_template(
            "index.html",
            details=details,
            current=current_tasks,
            completed=completed_tasks,
            successful=success,
            username=username,
            upcoming=upcoming,
            tasks=tasks,
            priority=priority,
        )
    
    # If no user is logged in, redirect to login
    return redirect("/login")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear any existing session
    session.clear()

    if request.method == "POST":
        # Form inputs
        email = request.form.get("email")
        password = request.form.get("password")

        # Input Validation
        if not email:
            return render_template("login.html", error="Email is required.")
        if not password:
            return render_template("login.html", error="Password is required.")

        # Query database for email
        user = User.query.filter_by(email=email).first()

        # Ensure email exists and password is correct
        if not user or not check_password_hash(user.password, password):
            return render_template("login.html", error="Invalid email and/or password.")

        # Log user in
        session["user_id"] = user.id

        flash("Login Successful!")
        return redirect("/")
    else:
        return render_template("login.html")


# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Form inputs
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Input validation
        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.")
        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match.")

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("register.html", error="Email is already registered.")

        # Hash the password and create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Log in the user after successful registration
        session["user_id"] = new_user.id
        flash("Registration successful!")
        return redirect("/")
    else:
        return render_template("register.html")

# Route to create a task
@app.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect("/login")  # Redirect to login if not logged in

    if request.method == "POST":
        # Form inputs
        name = request.form.get("name")
        deadline = request.form.get("deadline")

        # Input validation
        if not name:
            return render_template("create.html", error="Task name is required.")
        if not deadline:
            return render_template("create.html", error="Deadline is required.")

        # Check for duplicate task names for the user
        existing_task = Task.query.filter_by(user_id=session["user_id"], name=name).first()
        if existing_task:
            return render_template("create.html", error="Task already exists.")

        # Parse and validate the deadline
        try:
            deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
            if deadline < datetime.now():
                return render_template("create.html", error="Deadline cannot be in the past.")
        except ValueError:
            return render_template("create.html", error="Invalid date format.")

        # Add the task to the database
        new_task = Task(user_id=session["user_id"], name=name, deadline=deadline)
        db.session.add(new_task)
        db.session.commit()

        flash("Task created successfully!")
        return redirect("/")  # Redirect to the home page

    return render_template("create.html")

@app.route("/complete", methods=["GET", "POST"])
def complete():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    if request.method == "POST":
        # Form input
        task_name = request.form.get("task_name")

        # Input Validation
        if not task_name:
            return render_template("complete.html", error="Select the task to mark as completed")

        # Find the task
        task = Task.query.filter_by(user_id=user_id, name=task_name, progress="Not Completed").first()
        if not task:
            return render_template("complete.html", error="Task not found or already completed.")

        # Update task progress and set finish timestamp
        task.progress = "Completed"
        task.priority = "NONE"
        task.finish = datetime.now()

        # Compare finish time and deadline to set submission status
        if task.finish <= task.deadline:
            task.submission = "On Time"
        else:
            task.submission = "Late"

        # Commit changes
        db.session.commit()

        flash("Task marked as completed successfully!")
        return redirect("/")
    else:
        # Display all tasks which are not completed
        tasks = Task.query.filter_by(user_id=user_id, progress="Not Completed").all()
        return render_template("complete.html", tasks=tasks)


@app.route("/reschedule", methods=["GET", "POST"])
def reschedule():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    tasks = Task.query.filter_by(user_id=user_id, progress="Not Completed").all()

    if request.method == "POST":
        # Form Input
        name = request.form.get("task_name")
        new_deadline = request.form.get("new_deadline")

        # Input Validation
        if not name or not new_deadline:
            return render_template("reschedule.html", tasks=tasks, error="All fields are required.")

        # Parse the new deadline
        try:
            new_deadline = datetime.strptime(new_deadline, "%Y-%m-%dT%H:%M")
            if new_deadline <= datetime.now():
                return render_template("reschedule.html", tasks=tasks, error="Deadline cannot be in the past.")
        except ValueError:
            return render_template("reschedule.html", tasks=tasks, error="Invalid date format.")

        # Find the task
        task = Task.query.filter_by(user_id=user_id, name=name, progress="Not Completed").first()
        if not task:
            return render_template("reschedule.html", tasks=tasks, error="Task not found.")

        # Validate new deadline
        if task.deadline >= new_deadline:
            return render_template("reschedule.html", tasks=tasks, error="New deadline must be later than the old deadline.")

        # Update task deadline
        task.deadline = new_deadline
        db.session.commit()

        flash("Task rescheduled successfully!")
        return redirect("/")
    else:
        return render_template("reschedule.html", tasks=tasks)


@app.route("/prioritize", methods=["GET", "POST"])
def prioritize():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    if request.method == "POST":
        # Form Input
        name = request.form.get("task_name")

        # Input Validation
        if not name:
            return render_template("prioritize.html", error="Select a task to prioritize.")

        # Find the task
        task = Task.query.filter_by(user_id=user_id, name=name, progress="Not Completed").first()
        if not task:
            return render_template("prioritize.html", error="Task not found or already completed.")

        # Check if there's already a top-priority task
        top_task = Task.query.filter_by(user_id=user_id, priority="TOP", progress="Not Completed").first()
        if top_task:
            flash("Complete your top-priority task first.")
            return redirect("/")

        # Set the task as top priority
        task.priority = "TOP"
        db.session.commit()

        flash("Task prioritized successfully!")
        return redirect("/")
    else:
        # Fetch the tasks which are not completed
        tasks = Task.query.filter_by(user_id=user_id, progress="Not Completed").all()
        return render_template("prioritize.html", tasks=tasks)

@app.route("/logout")
def logout():
    # Clear the session
    session.clear()

    # Redirect to login page
    # flash("Logged out successfully!")
    return redirect("/login")

# Initialize the database
with app.app_context():
    db.create_all()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

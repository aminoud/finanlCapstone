#=====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import datetime
import os

#====Login Section====
# Open user.txt and read in the data
def login():
    while True:
        # Ask for username and password
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        # Check if username and password are valid
        with open("user.txt", "r") as file:
            for line in file:
                line = line.strip().split(", ")
                if line[0] == username and line[1] == password:
                    return username
            # If username and password are not valid, ask again
            print("Incorrect username or password, try again")

# Create a function that add a user
def reg_user():
    while True:
        new_username = input("Enter a new username: ")
        new_password = input("Enter a new password: ")
        confirm_password = input("Confirm your password: ")
        if new_password == confirm_password:
            # Check if the username entered don't exist already
            with open("user.txt", "r") as file:
                users = [line.strip().split(", ")[0] for line in file]
                if new_username in users:
                    print("Username already exists, try a different one")
                else:
                    # Append new user data to user.txt
                    with open("user.txt", "a") as file:
                        file.write(f"{new_username}, {new_password}\n")
                        print("User successfully registered")
                        menu(username)
        else:
            print("Passwords don't match, try again")

# Create a function that add a task to a user
def add_task(username):
    assignee = input("Enter the username of the person the task is assigned to: ")
    title = input("Enter the title of the task: ")
    description = input("Enter a description of the task: ")
    due_date = input("Enter the due date of the task in the following format: 2021 Jan 21: ")
    action = input("Enter Yes if the task is complete or No: ")
    date_assigned = datetime.now().strftime("%Y-%m-%d")
    # Append the new task to tasks.txt
    with open("tasks.txt", "a+") as file:
        file.write(f"\n{assignee}, {title}, {description}, {date_assigned}, {due_date}, {action}")
        print("Task successfully added, please note that changes will only be applied when exiting")
        menu(username)

# Create a function that displays all the tasks
def view_all():
    tasks = []
# Write task to task.txt
    with open("tasks.txt", "r+") as file:
        for line in file:
            line = line.strip().split(", ")
            tasks.append(line)
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {', '.join(task)}")
        menu(username)

# Create a function that displays the tasks of the current user
def view_mine(username):
    tasks = []
    with open("tasks.txt", "r") as file:
        for line in file:
            line = line.strip().split(", ")
            if line[0] == username:
                tasks.append(line)
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {', '.join(task)}")
    # Create a loop that ask the user if he wants to edit a task
    while True:
        task_num = int(input("Enter the task number you want to edit or -1 to return to the main menu: "))
        if task_num == -1:
            menu(username)
        if task_num > len(tasks):
            print("Invalid task number, try again")
        else:
            action = input("Enter 'Yes' to mark the task completed or 'No': ")
            nam = input("Enter the new name or pass: ")
            with open("tasks.txt", "r") as file:
                lines = file.readlines()
                line = lines[task_num +1].strip().split(", ")
                line[-1] = action
                if nam.lower() != "pass":
                    line[0] = nam
                lines[task_num + 1] = ", ".join(line) + "\n"

            with open("tasks.txt", "w") as file:
                file.writelines(lines)
                print("Task successfully completed")
                menu(username)

# Create the menu function
def menu(username):
    # Get the user's choice
    while True:
        print('\nPlease select one of the following options:')
        print('r- Register a new user')
        print('a- Add a task')
        print('va- View all tasks')
        print('vm- View only tasks assigned to me')
        # Only show this option if the admin is logged in
        if username.lower() == 'admin':
            print('ds- Statistics')
        print('e- Exit')
        # Ask the user to make a choice
        choice = str(input("\nEnter your choice: "))
        if choice == "a":
            add_task(username)
        # Ceck if it is the admin that is logged in to allow him to add users
        if username.lower() == 'admin':
            if choice == "r":
                reg_user()
        else:
            if choice == "r":
                print("Only the admin can rgister user")
                menu(username)
        if choice == "va":
            view_all()
        if choice == "vm":
            view_mine(username)
        if choice == "e":
            exit()
        if choice == "ds":
            generate_reports()
            display_statistics()
        else:
            print("Invalid choice, try again")

# Create a function that create the statistical reports
def generate_reports():
    task_dict = process_task_file('tasks.txt')
    process_overview_file('task_overview.txt', task_dict)
    t_overview()

# Create a function that calculate a statstical overview of tasks
def t_overview():
    global total_tasks
    total_tasks = 0
    total_users = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0
    today = datetime.now().strftime("%d %b %Y")
    # Dictionary to store the statistics for each user
    stats = {}
    task_assigned_to = {}

    # Read from tasks.txt the data
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()
        for task in tasks:
            task = task.strip().split(", ")
            due_date = datetime.strptime(task[-3], "%d %b %Y")
            done_date = datetime.strptime(task[-2], "%d %b %Y")
            # Calculate the number of completed tasks, and the number of those that are overdue
            if task[-1] == "Yes":
                completed_tasks += 1
            if due_date > done_date:
                overdue_tasks += 1
            total_tasks += 1
        uncompleted_tasks = total_tasks - completed_tasks
        # calculate percentage of completed tasks
        if total_tasks > 0:
            percent_completed = (completed_tasks / total_tasks) * 100
            percent_overdue = (overdue_tasks / total_tasks) * 100
        # Avoid the division per zero
        else:
            percent_completed = 0
            percent_overdue = 0

        # Write the calculated data in task_overview.txt
        with open("task_overview.txt", "w") as file:
            file.write(f"Total number of tasks: {total_tasks}\n")
            file.write(f"Total number of completed tasks: {completed_tasks}\n")
            file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
            file.write(f"Total number of tasks that are overdue: {overdue_tasks}\n")
            file.write(f"Percentage of tasks that are incomplete: {100 - percent_completed}\n")
            file.write(f"Percentage of tasks that are overdue: {percent_overdue}\n")

# Create a function that treat task_overview.txt data
def process_task_file(filename):
    with open(filename, 'r') as f:
        tasks = [line.strip().split(',') for line in f.readlines()]
    task_dict = {}
    for task in tasks:
        user = task[0]
        if user not in task_dict:
            task_dict[user] = [0, 0, 0, 0]
        task_dict[user][0] += 1
        if task[5].strip() == 'Yes':
            task_dict[user][1] += 1
        if task[4].strip() < task[3].strip():
            task_dict[user][2] += 1
    return task_dict

# Create a function that calculate a statstical overview for each user
def process_overview_file(filename, task_dict):
    with open(filename, 'r') as f:
        lines = [line.strip().split(':') for line in f.readlines()]
        total_tasks = int(lines[0][1])
        completed_tasks = int(lines[1][1])
        uncompleted_tasks = int(lines[2][1])
        overdue_tasks = int(lines[3][1])
    with open("user_overview.txt", "w") as reset:
        reset.write("")
    for user, tasks in task_dict.items():
        assigned_tasks = tasks[0]
        completed_tasks = tasks[1]
        overdue_tasks = tasks[2]
        still_to_complete = assigned_tasks - completed_tasks
        percentage_assigned = (assigned_tasks / total_tasks) * 100
        percentage_completed = (completed_tasks / assigned_tasks) * 100 if assigned_tasks else 0
        percentage_still_to_complete = (still_to_complete / assigned_tasks) * 100 if assigned_tasks else 0
        percentage_overdue = (overdue_tasks / assigned_tasks) * 100 if assigned_tasks else 0

        # Append to user_overview.txt the data of the user treated by the loop
        with open("user_overview.txt", "a+") as file:
            file.write("User: "+ str(user) +"\n")
            file.write("Total number of tasks assigned:" + str(assigned_tasks) + "\n")
            file.write("Percentage assigned: {:.2f}".format(percentage_assigned) + "\n")
            file.write("Percentage completed: {:.2f}".format(percentage_completed) + "\n")
            file.write("Percentage still to complete: {:.2f}".format(percentage_still_to_complete) + "\n")
            file.write("Percentage overdue: {:.2f}".format(percentage_overdue) + "\n")
            file.write("\n")

# Create a function that display the data in task_overview.txt and user_overview.txt and create them if they don't exist
def display_statistics():
    if not os.path.exists("task_overview.txt"):
        generate_reports()
    with open("task_overview.txt", "r") as file:
        print(file.read())

    if not os.path.exists("user_overview.txt"):
        generate_reports()
    with open("user_overview.txt", "r") as f:
        print(f.read())

# Start the program by asking credantials then show menu
while True:
    username = login()
    menu(username)

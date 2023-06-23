'''
based on learning from Hyperion.dev
Capstone task set in T17
A program to output information about recorded tasks,
and to transfer this information backwards and forwards between 
text documents.
'''

#the following are sources of research of this task:
# https://www.w3schools.com/python/python_sets.asp for sets not having duplicates
#https://www.geeksforgeeks.org/python-initialize-a-dictionary-with-only-keys-from-a-list/ for setting keys
#https://stackoverflow.com/questions/7680729/how-do-you-split-a-string-to-create-nested-list?rq=3 for deconstructing tasks into listed lists
#https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python current date
#Google search results page used to add '0' to arguments of exit() so as to not record and error message
#on exiting


# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date
import time

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#the program begins with four refactored taks in order to increase the readibility of the codebase
def reg_user():

        # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

        # Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

        '''Add a new user to the user.txt file'''
    user_name_loop = True

    while user_name_loop == True:
            
        # - Request input of a new username
        new_username = input("New Username: ")

        if new_username in username_password.keys():
            print("User already exists, please choose another username: ")

        else:
            user_name_loop = False

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
            
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")



def add_task():

    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
    loop = True
    while loop == True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        loop = False
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")




def view_all():

    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
            


def view_mine():

    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    '''
    loop = True
    while loop == True:

        specific_task = int(input("Please input the number of the task you would like to view (if you input -1, you will return to the main menu): "))
        if specific_task == -1:
            break
        else:
            loop = False
            for t in task_list:
                task_number = 1

                if (t['username'] == curr_user):
                    disp_str = f"Task: \t\t {t['title']}\n"
                    disp_str += f"Assigned to: \t {t['username']}\n"
                    disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Task Description: \n {t['description']}\n"
                    print(f"""Here are the details of all your tasks: {disp_str} Task number: {task_number}""")
                    #conditional bocks to separate out the requested task and give options for ammendations
                    if task_number == specific_task:
                        print(f"\n\n\nThis is the specific task you wanted to look at. The task number is {task_number} and the details are {disp_str}")
                        completed_task = input("Would you like to mark this task as complete? Yes, or no: ")
                        if completed_task.upper() == 'YES':
                            complete = True
                        edit_decision = input("Would you like to edit this task? Yes, or no: ")
                        if edit_decision.upper() == 'YES' and complete == False:
                            edit_part = int(input("Would you like to edit 1) the username\n 2) the due date of the task?: "))
                            if edit_part == 1:
                                t['username'] = input("Please input the new username: ")
                            else:
                                t['due_date'] = input("Please input the new due date: ")
                        else: 
                            print("You have decided not to edit the task or the task is already complete.")
                    else:
                        print(f"""This (task number: {specific_task}) is not a task number for this username.""")
                task_number += 1
            if specific_task == -1:
                continue
        
            


# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()                

    elif menu == 'gr' and curr_user == 'admin':
        with open("task_overview.txt", "w") as task_file:
            task_overview_list_to_write = []
            number_tasks = 0
            number_complete = 0
            number_incomplete = 0
            overdue_tasks = 0
            for t in task_list:
                if t['completed'] == True:
                    number_complete += 1
                if ['completed'] == True and (t['due_date'] < date.now()):
                    overdue_tasks += 1 
                number_tasks += 1
            percentage_incomplete = (number_complete/number_tasks) * 100
            percentage_overdue = (overdue_tasks/number_tasks) * 100
            number_incomplete = number_tasks - number_complete
            task_overview_list_to_write = f"""The total number of tasks is : {number_tasks}. The number of complete tasks is {number_complete}.
            The number of incomplete tasks is {number_incomplete}. The number of overdue tasks is {overdue_tasks}. The percentage
            of incomplete tasks is {percentage_incomplete}. The percentage of overdue task is {percentage_overdue}."""
            task_file.write(task_overview_list_to_write)
        print("Task successfully added.")

        with open("tasks.txt", "r+") as task_list:
            task_data = task_list.read()

            number_tasks = 0
            total_users = 0
            overall_number_complete = 0
            overall_number_incomplete = 0
            overall_overdue_tasks = 0
            user_name_set = set(())
            username_dict = {}
            username_complete_dict = {}
            username_task_overdue_dict = {}

            #splitting the file-read tasks into, firstly, each overall task, then into
            #the components of the tasks
            task_components = [[x for x in tt.split(';')] for tt in task_data.split('\n')]

            for t in task_components:
                user_name_set.add([t][0][0])
                number_tasks += 1


            #setting up keys and zeroing tasks per username
            for i in user_name_set:
                username_dict[i] = 0
            #setting up keys and zeroing completed tasks per username
            for i in user_name_set:
                username_complete_dict[i] = 0
            #setting up keys and zeroing overdue tasks per username
            for i in user_name_set:
                username_task_overdue_dict[i] = 0


            #loop through the segmented tasks to find specific component, and then update dictionaries
            #set up to track these components by username
            for k in task_components:
                for x in username_dict:
                    if ([k][0][0]) == x:
                        username_dict[x] += 1
                    date2 = (str(date.today())).replace('-', '')
                    if (([k][0][0]) == x) and ((([k][0][3]).replace('-', '')) < date2):
                        username_task_overdue_dict[x] += 1
                    if ([k][0][5]).upper() == 'YES':
                        username_complete_dict[x] += 1

            #loop through the dictionaries for information to be
            #added to task_overview.txt
            for keys in username_complete_dict:
                overall_number_complete += username_complete_dict[keys]
            for keys in username_task_overdue_dict:
                overall_overdue_tasks += username_task_overdue_dict[keys]

            #request username to be used to find details for user_overview.txt
            sought_username = input("Please input the username you are interested in: ")
            
            #use the dictionaries to find information by user and task component
            #then use details to calculate percentages
            total_tasks_assigned_user = username_dict.get(sought_username)
            number_complete_task_for_user = username_complete_dict.get(sought_username)
            number_overdue_task_for_user = username_task_overdue_dict.get(sought_username)
            overall_percentage_incomplete = (overall_number_complete/number_tasks) * 100
            overall_percentage_overdue = (overall_overdue_tasks/number_tasks) * 100
            overall_number_incomplete = number_tasks - overall_number_complete
            percentage_tasks_to_user = total_tasks_assigned_user/number_tasks * 100
            percentage_tasks_complete = number_complete_task_for_user/total_tasks_assigned_user * 100
            percentage_incomplete = 100 - percentage_tasks_complete
            percentage_overdue_incomplete = number_overdue_task_for_user/(total_tasks_assigned_user - number_complete_task_for_user) * 100
            number_usernames = len(user_name_set)


            #set up strings for arguments for write methods
            user_overview_to_append = f"""\nThe total number of tasks is : {number_tasks}. 
            The total numbers of differing usernames is {number_usernames}.
            The number of tasks assigned to {sought_username} is {total_tasks_assigned_user}.
            The percentage of tasks {sought_username} has out of the total number of tasks is {percentage_tasks_to_user}.
            The percentage of the tasks completed by {sought_username} is {percentage_tasks_complete} per cent.
            The percentage of tasks still needing to be completed is {percentage_incomplete} per cent.
            The percentage of tasks that {sought_username} has let run overdue, out of those that are incomplete, 
            is {percentage_overdue_incomplete} per cent."""

            with open("task_overview.txt", "w") as task_file:

                task_overview_list_to_write = f"""\nThe total number of tasks is : {number_tasks}. 
                The number of complete tasks is {overall_number_complete}.
                The number of incomplete tasks is {overall_number_incomplete}. 
                The number of overdue tasks is {overall_overdue_tasks}. 
                The percentage of incomplete tasks is {overall_percentage_incomplete}. 
                The percentage of overdue task is {overall_percentage_overdue}."""
                task_file.write(task_overview_list_to_write)
            print("\n\n\nThis is the overall overview of the tasks: ", task_overview_list_to_write, "Tasks' overview successfully added to task_overview.txt.")



            with open("user_overview.txt", "w+") as user_overview_file:
                user_overview_file.write(user_overview_to_append)
                print(f"""\n\n\nThe information specific to username '{sought_username}' is:\n\n""", user_overview_to_append, "\n\n\nInformation successfully added to user_overview.txt.")



    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit(0)

    else:
        print("You have made a wrong choice, Please Try again")

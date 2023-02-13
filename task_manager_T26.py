"""
A task manager programme that interacts with a tasks.txt file and a users.txt file, allowing the user to log in, 
and interact with tasks and users in various ways. Admin users can add new users and generate statistics on the task 
and user info, while ordinary users can add tasks, view tasks and modify tasks in a limited way.
"""

#=====importing libraries=========

import datetime
from datetime import datetime
from datetime import date

#=====global variables===========

today = date.today()
# Sets a date format for the due date
date_format = "%d %b %Y"

# Flag variable updated in the get_reports() function and checked in the get_stats() function to determine whether user reports have already been createdd 
created_reports = False
# Flag variable updated in the view_mine(), reg_user() and add_task() functions and checked in the get_stats() function to determine whether the user reports need updating so that all changes made this session are captured
data_edited = False

#=====setting colours=======

black = "\u001b[30;1m"
red = "\u001b[31;1m"
green = "\u001b[32;1m"
yellow =  "\u001b[33m"
blue = "\u001b[34;1m"
magenta = "\u001b[35;1m"
cyan = "\u001b[36;1m"  
white = "\u001b[37;1m"
reset = "\u001b[0m"
bold = "\u001b[1m"
underline = "\u001b[4m"
reversed = "\u001b[7m"

#=====functions=======

# Gets password and username input from the user
def login():
    while True:
        username = input("\nEnter your username:\n")
        password = input("Enter your password:\n")

        # Checks whether the username is a key in the dictionary and the password matches the associated value
        # and if successful prints a welcome message then exits the loop
        if username in logins.keys() and password == logins[username]:
            print(f"\nHello, {cyan}{username}{reset}. You have logged in successfully.")
            break

        # If either username or password is incorrect, or password belong to the username, starts the loop again.
        else:
            print(f"\n{red}Those login details aren't valid. Please try again.{reset}")
            continue
    return username

# Opens the 'tasks.txt' file and creates a dictionary of tasks with each line as a list of component items and with an index number (starting from 1) as the key
def create_task_data():  
    with open("tasks.txt","r") as f: 
        task_data = f.readlines()
        # Splits each line at the comma and adds the contents to a list
        split_data = [ line.split(", ") for line in task_data]
        # Creates a dictionary which holds all the lists of task elements, with an incrementing number as the key
        saved_task_data = {i:line for i,line in enumerate(split_data,1)}
        return saved_task_data

# Allows user to register a new user and updates 'user.txt' file (admin only)
def reg_user():
    # Checks if the user is admin and if so, asks them to enter a new username, password, and to repeat the password 
    if username == "admin":
        while True: 
            new_user = input("\nEnter a new username:\n")
        
            # Checks whether the username matches any existing usernames in the file
            if new_user not in logins.keys():
                new_pass = input("Enter a new password:\n")
                pass_conf = input("Re-enter your password to confirm it:\n")

                # If the two instances of the password match, the username and password are added to 'users.txt' and the logins dictionary, and a confirmation message displayed
                if new_pass == pass_conf:
                    # Adds the user to the logins dictionary
                    logins[new_user] = new_pass
                    with open("user.txt","a") as f:
                        f.write(f"\n{new_user}, {new_pass}")
                        # Flag variable used in the get_stats() function to check whether reports need updating 
                        data_edited = True
                        print(f"\nUser {green}'{new_user}'{reset} has been created.")
                        break
                # If the two instances of the password don't match, an error message is displayed
                # The user is then returned to the menu
                else:
                    print(f"{red}Sorry, the passwords don't match. Please try again.{reset}")
                    continue
            else:     
                print(f"{red}Sorry, that username is already taken. Please try again.{reset}\n")
                continue
    
    # If the user is not an admin, it displays an error message and returns to the menu        
    else:
        print(f"{red}Sorry, this option is restricted to admin only\n{reset}")

# Allows user to add a new task to 'tasks.txt'
def add_task():
    while True:
        # Asks for the user who the task will be assigned to
        task_user = input("\nEnter the name of the person to whom the task will be assigned:\n")
        # If the user doesn't already exist in the logins{} dictionary, prints an error message and loops
        if task_user not in logins.keys():
            print(f"\n{red}The task must be assigned to an existing user. Please check the name or register a new user before assigning.{reset}")
            continue
        else:
            break

    # Gets name and description of task    
    task_name = input("\nEnter the name of the task:\n")
    task_desc = input("\nEnter a description of the task:\n")

    # Uses the datetime library and 'today' variable imported at the top of the page to set the date in a human-friendly format
    task_assigned = today.strftime("%d %b %Y")

    # Asks for the due date to be input
    while True:
        task_due = input("\nWhat is the due date of the task? Please use the format '1 Jan 2023':\n")
        try: 
            task_date_obj = datetime.strptime(task_due, date_format).date()            
            break
         # Checks whether due date is in the right format, otherwise it prints an error message and asks again until the correct format is used
        except: 
            print(f"\n{red}Sorry, that date format is not recognised. Please use the format '1 Jan 2023'. Note months should be the first 3 letters only.{reset}")
            continue 
    
    # Sets the task to incomplete as a default
    task_complete = "No"
    
    # Flag variable used in the get_stats() function to check whether reports need updating 
    data_edited = True

    # Opens the 'tasks.txt' file with 'append' access and writes each of the above elements to a new task_elements
    with open("tasks.txt","a") as f:
        f.write(f"\n{task_user}, {task_name}, {task_desc}, {task_assigned}, {task_due}, {task_complete}")    
    return print(f"\nThank you. {green}'{task_name}'{reset} has been added succesfully.")

# Creates or updates (as required) and displays the reports on user and task data (admin only)
def display_stats():
    #Sub-function to print out the reports in a specific, readable format
    def display_reports():
        # Reads user report from file
        with open('task_overview.txt','r') as f:
            task_report = f.read()   
     
        # Reads user report from file
        with open('user_overview.txt','r') as f:
            user_report = f.read()
    
        # Gives each report a heading and assigns it to a variable
        task_overview_report = f"\n"+ ("*"*10)+" Task Overview Statistics "+("*"*10)+f"\n{task_report}"
        user_overview_report = f"\n"+ ("*"*10)+" User Overview Statistics "+("*"*10)+f"\n{user_report}"

        # Returns the headed reports when function called
        print(task_overview_report + user_overview_report)

    # Checks that the user is admin and gives a restriction message if not
    if username == "admin":
        # Checks the two flag variables, and if the data has been edited, or reports have not been created this session, it generates and prints new reports
        if data_edited == True or created_reports == False:
            gen_reports()
            display_reports()
        # Checks the two flag variables, and if data has not been edited and the reports have already been created, it displays the existing reports
        elif data_edited == False and created_reports == True:
            display_reports()  

    else: 
        print("Sorry, this option is restricted to admin only.")            

# Displays all task information for all tasks in a readable format    
def view_all():  
    # Opens the 'tasks.txt' file and reads each line, splitting it at each ', '
    with open("tasks.txt","r") as f:
        for count, task in enumerate(f,1):
            task_elements = task.split(", ")
            # Builds up some formatted display text showing each piece of task information for each task, and adding an index number to correspond with the display choices in view_mine()
            task_text = f"\n{yellow}---------------[{count}]---------------{reset}\n"
            task_text += f"Assigned to:\t{task_elements[0]}\n"
            task_text += f"Task:\t\t{task_elements[1]}\n"
            task_text += f"Description:\t{task_elements[2]}\n"
            task_text += f"Assigned date:\t{task_elements[3]}\n"
            task_text += f"Due date:\t{task_elements[4]}\n"
            task_text += f"Is completed:\t{task_elements[5]}\n"
            print(task_text)
    return

# Displays all the data for tasks which are assigned to the user, and allows them to edit task owner, due date and completeness  
def view_mine():

    # Updates the saved_task_data dictionary (in case it has been edited this session)
    saved_task_data = create_task_data()

    # Creates a list to hold the indexes of the current user's tasks, in order to prevent them from selecting another user's tasks to update
    my_tasks_index = []

    # Sets a Boolean flag variable which will be updated to True in the loop below if there are tasks belonging to the user in the task dictionary
    has_tasks = False

    # Loops through the items in the tasks dictionary
    for key in saved_task_data:
        # Displays the data only for the logged-in user          
        if saved_task_data[key][0] == username:
            # Changes flag variable to True
            has_tasks = True
            # Adds the numbers for the logged-in user's tasks to the my_tasks_index list in order to validate the selection further down
            my_task_number = key
            my_tasks_index.append(my_task_number)
            # Builds up some formatted display text showing each piece of task information for each task of that user
            task_text = f"\n{yellow}---------------[{key}]---------------{reset}\n"
            task_text += f"Assigned to:\t{saved_task_data[key][0]}\n"
            task_text += f"Task:\t\t{saved_task_data[key][1]}\n"
            task_text += f"Description:\t{saved_task_data[key][2]}\n"
            task_text += f"Assigned date:\t{saved_task_data[key][3]}\n"
            task_text += f"Due date:\t{saved_task_data[key][4]}\n"
            task_text += f"Is completed:\t{saved_task_data[key][5]}\n"
            print(task_text)
    
    # Checks flag variable after loop runs, to make sure the user has at least one task - otherwise, exits the function back to main menu
    if has_tasks == False: 
        print(f"\n{red}Sorry, you have no tasks assigned{reset}")
        return   

    # ---- TASK SELECTION MENU LOOP ---- #
    # Asks the user to select a task by entering its number, or to exit by typing '-1'
    while True:
        # Gets the input of the task number selected
        vm_task_choice = int(input(f"\n{yellow} To update a task, select a task number, or enter {bold}-1{reset}{yellow} to exit to main menu:{reset} "))

        # If -1 is entered, exits the function and returns to the main menu 
        if vm_task_choice == -1:
            return
        
        # If the number entered does not match the number of a task belonging to the user, an error message is displayed and input is requested again
        elif vm_task_choice not in my_tasks_index: 
            print(f"\n{red}You have selected an invalid option. You can only select a task that is assigned to you. Please try again{reset}")
            continue     

        else:
            print(f"\nYou have selected {cyan}Task {vm_task_choice}, '{saved_task_data[vm_task_choice][1]}'{reset}")           
        
        # ---- TASK EDIT MENU LOOP ---- # 
        # Displays a menu offering options to choose to edit the user assigned, the due date or the completeness of the selected task
        while True:
            edit_menu = f"\n{yellow}-------[ {white}SELECT AN OPTION{yellow}]----------\n"
            edit_menu += f"1 - Edit task: reassign to a different user\n"
            edit_menu += f"2 - Edit task: change the due date\n"
            edit_menu += f"3 - Mark as completed\n"
            edit_menu += f"4 - Go back\n"
            edit_menu += f"-------------------------------{reset}\n"
            
            # Gets user input for the menu option
            edit_menu_choice = input(edit_menu)
            
            # Checks that the input is an integer; otherwise, displays and error message and asks again
            try:
                int(edit_menu_choice)
            except ValueError:
                print(f"\n{red}Sorry, that input is invalid. Please select a number from the menu items.")
                continue

            edit_menu_choice = int(edit_menu_choice)
            # Checks that the user has entered a valid number in the range and shows the menu again if not
            if edit_menu_choice <= 0 or edit_menu_choice >= 5:
                print(f"\n{red}You have selected an invalid option. You can only choose from the menu items. Try again{reset}")
                continue 
              
            # Asks user to enter the new assignee for this task and updates the saved_task_data dictionary accordindly
            elif edit_menu_choice == 1:
                new_task_owner = input("\nWho would you like to assign the task to? ")
                # Checks if the new assignee is in the users register dictionary, and prints an error message if not
                if new_task_owner not in logins.keys():
                    print(f"\{red}Sorry, that user is not registered.The task must be assigned to an existing user. Please check the name or register a new user before assigning.{red}")
                    continue
                else:                    
                    saved_task_data[vm_task_choice][0] = new_task_owner
                    # Sets this flag variable to True in order to determine whether the user reports need updating in the generate reports module
                    data_edited = True
                    # Combines all the elements of split_edit_data and replaces the task_choice with the new line
                    print(f"\n{cyan}Task {vm_task_choice}, '{saved_task_data[vm_task_choice][1]}'{reset}, has been reassigned to {cyan}{saved_task_data[vm_task_choice][0]}.{reset}")
                    
            elif edit_menu_choice == 2:
                # Asks for the bew due date to be input, and checks whether it is in the right format, otherwise it prints an error message and asks again until the correct format is used
                while True:
                    new_due_date = input(f"\nEnter the new due date for Task {vm_task_choice}, '{saved_task_data[vm_task_choice][1]}', using the format '1 Jan 2023': ")
                    try: 
                        new_due_date_obj = datetime.strptime(new_due_date, date_format).date()
                        saved_task_data[vm_task_choice][-2] = new_due_date
                        # Sets this flag variable to True in order to determine whether the user reports need updating in the generate reports module
                        data_edited = True
                        print("\nThe due date has been amended.")
                        break                 
                    except: 
                        print(f"{red}Sorry, that date format is not recognised. Please use the format '1 Jan 2023'. Note months should be the first 3 letters only.{reset}")
                        continue                
            
            # If the task is already set as complete and the user has selected either option 1 or 2, prints an error message and goes back to menu
            elif (edit_menu_choice == 1 or edit_menu_choice) == 2 and (saved_task_data[vm_task_choice][-1].lower() == "no" or saved_task_data[vm_task_choice][-1].lower() == "no\n"):
                print(f"{red}Sorry, you can't edit a completed task.{reset}")  
                continue

            # If the task is already set as complete and the user has selected option 3, prints an error message and goes back to menu
            elif edit_menu_choice == 3 and (saved_task_data[vm_task_choice][-1].lower() == "yes" or saved_task_data[vm_task_choice][-1].lower() == "yes\n"):
                print(f"{red}Sorry, this task is already complete.{reset}")  
                continue

            # If the task is not marked as complete and the user has selected option 3, marks the task as complete and prints a confirmation message
            elif edit_menu_choice == 3 and (saved_task_data[vm_task_choice][-1].lower() != "yes" or saved_task_data[vm_task_choice][-1].lower() != "yes\n"):
                saved_task_data[vm_task_choice][-1] == "Yes\n"
                # Sets this flag variable to True in order to determine whether the user reports need updating in the gen_reports() function
                data_edited = True
                print(f"\n{cyan}Task {vm_task_choice}, '{saved_task_data[vm_task_choice][1]}'{reset}, has been marked as complete.")

            # If option 4 is selected, exits back to higher menu
            elif edit_menu_choice == 4:
                break
    
        # Update saved_task_data      
        # Creates a list to hold the values from the saved_task_data dictionary
        task_write_list = []
        # Iterates through each value in the dictionary, joining the separate task elements into a string and adding that string to the task_write_list list
        for v in saved_task_data.values():
            task_write_list.append(", ".join(v))

        # Opens the 'tasks'txt' file and writes each item in task_write_list to it, then prints a confirmation message
        with open('tasks.txt','w') as f:         
            for i in task_write_list:
                f.write(i)
        
        return saved_task_data           
  
# Reads through the 'task.txt' and 'user.txt' files, calculates statistics and returns two reports: (i) tasks as a whole and (ii) each user's tasks
def gen_reports():
    #  --- TASK REPORTS ---
    # Opens 'tasks.txt' file, reads data and closes file
    f = open("tasks.txt","r") 
    task_data = f.readlines()
    f.close()

    # Gets the total number of tasks
    total_tasks = len(task_data)

    # Creates dictionaries to hold information on how many tasks are assigned to users, how many are complete and incomplete.
    # The keys are the user names
    assigned_tasks = {line.split(", ")[0]: 0 for line in task_data}
    complete_tasks = {line.split(", ")[0]: 0 for line in task_data}
    incomplete_tasks = {line.split(", ")[0]: 0 for line in task_data}

    # Increments the values in each dictionary according to the criteria
    for line in task_data:
        split_data = line.split(", ")
        # In the assigned_tasks dictionary, increases the count by one for each task assigned to the user
        assigned_tasks[split_data[0]] += 1
        # In the complete_tasks dictionary, increases the count by one for each complete task assigned to the user
        if split_data[-1].lower().strip("\n") == "yes":
            complete_tasks[split_data[0]] += 1
        # In the incomplete_tasks dictionary, increases the count by one for each incomplete task assigned to the user
        if split_data[-1].lower().strip("\n") == "no":
            incomplete_tasks[split_data[0]] += 1

    # Stores the total tasks assigned, total complete tasks and total incomplete tasks in variables
    total_assigned = sum(assigned_tasks.values())
    total_complete = sum(complete_tasks.values())
    total_incomplete = sum(incomplete_tasks.values())

    # Creates a dictionary for checking overdue tasks
    overdue_tasks = {}

    # Adds the usernames to the overdue_tasks dictionary
    for line in task_data: 
        split_data = line.split(", ")
        overdue_tasks[split_data[0]] = 0
        # For each task, converts the due date to a date object following the format pattern above
        due_date = datetime.strptime(split_data[-2], date_format)
        due_date = datetime.date(due_date)
        # Checks if the due date is older than today, and if the task is not completed, and adds a count for overdue, incomplete tasks to the dictionary
        if due_date < today and split_data[-1] == "No\n":
            overdue_tasks[split_data[0]] += 1

    # Stores the number of overdue tasks, the percentage of all tasks incomplete, and the percentage of all tasks complete as variables       
    total_overdue = sum(overdue_tasks.values())
    percent_incomplete = round((total_incomplete/total_tasks)*100)
    percent_overdue = round((total_overdue/total_tasks)*100)

    # Uses the variables above to write a task report to the 'task_overview.txt' file
    with open('task_overview.txt','w') as f:
        f.write(f"Total number of tasks:\t\t\t{total_tasks}\n")
        f.write(f"Total complete tasks:\t\t\t{total_complete}\n")
        f.write(f"Total incomplete tasks:\t\t\t{total_incomplete}\n")
        f.write(f"Total overdue tasks:\t\t\t{total_overdue}\n")
        f.write(f"Percentage of tasks incomplete:\t\t{percent_incomplete}%\n")
        f.write(f"Percentage of tasks overdue:\t\t{percent_overdue}%\n")

    # --- USER REPORTS ---

    # Opens 'users.txt' file, reads data and closes file
    f = open("user.txt","r") 
    user_data = f.readlines()
    f.close()

    # Gets the total number of users
    total_users = len(user_data)

    # Creates a list of users in the user file 
    users = [key for key in logins.keys()]

    # Creates a set of dictionaries for use in the calculations 
    users_tasks = {}
    user_comp_tasks = {}
    user_incomp_tasks = {}
    user_overdue_tasks = {}

    # Creates the keys for the dictionaries as the users in the user file
    for i in user_data:
        (key,val) = i.split()
        key = key.strip(',')
        user_comp_tasks[key] = 0
        user_incomp_tasks[key] = 0
        users_tasks[key] = 0
        user_overdue_tasks[key] = 0

    # Populates the users_tasks dictionary values with the number of tasks assigned to each user
    # Excludes users with no tasks assigned to them
    for item in users_tasks.keys():
        if item in assigned_tasks.keys():
            users_tasks[item] = assigned_tasks[item]

    # Populates the user_comp_tasks dictionary with the number of completed tasks assigned to each user 
    for item in user_comp_tasks.keys():
        if item in complete_tasks.keys():
            user_comp_tasks[item] = complete_tasks[item]

    # Populates the user_incomp_tasks dictionary with the number of incomplete tasks assigned to each user
    for item in user_incomp_tasks.keys():
        if item in incomplete_tasks.keys():
            user_incomp_tasks[item] = incomplete_tasks[item]

    # Populates the user_overdue_tasks dictionary with the number of overdue tasks assigned to each user
    for item in user_overdue_tasks.keys():
        if item in overdue_tasks.keys():
            user_incomp_tasks[item] = incomplete_tasks[item]
    
    # Sub-function to calculate and return the percentage of total tasks assigned to user. 
    # NB This and following sub-functions have to be nested like this, because they call variables only used inside the view_mine() function
    def user_percent_of_tasks(i):
        percent = round((users_tasks[i]/total_tasks)*100)
        return percent

    # Sub-function to calculate the percentage of assigned tasks complete by user, avoiding div by zero error
    def user_percent_complete(i):
        if users_tasks[i] != 0:
            percent = round((user_comp_tasks[i]/users_tasks[i])*100)
            return percent
        else: 
            return 0

    # Sub-function to calculate the percentage of assigned tasks incomplete by user, avoiding div by zero error
    def user_percent_incomplete(i):
        if users_tasks[i] != 0:
            percent = round((user_incomp_tasks[i]/users_tasks[i])*100)
            return percent
        else: 
            return 0    

    # Sub-function to calculate the percentage of assigned tasks overdue by user, avoiding div by zero error
    def user_percent_overdue(i):
        if users_tasks[i] != 0:
            percent = round((overdue_tasks[i]/users_tasks[i])*100)
            return percent
        else: 
            return 0    

    # Writes user report to 'user_overview.txt' file and closes file
    with open('user_overview.txt','w') as f:
        f.write(f"Total number of users:\t\t{total_users}\n")
        f.write(f"Total number of tasks assigned:\t{total_tasks}\n")
        # For each user, performs calculations on tasks and calls percentage functions
        for i in users:
                f.write(f"\nUser: {i.upper()}\n")
                f.write(f"Number of tasks assigned:\t\t\t{users_tasks[i]}\n")  
                f.write(f"Percent of total tasks assigned:\t\t{user_percent_of_tasks(i)}%\n")  
                f.write(f"Percent of assigned tasks completed:\t\t{user_percent_complete(i)}%\n")  
                f.write(f"Percent of assigned tasks not completed:\t{user_percent_incomplete(i)}%\n")
                f.write(f"Percent of assigned tasks overdue:\t\t{user_percent_overdue(i)}%\n")
    
    # Sets flag variable to True, which signals that reports already exist when the user select the 'statistics' menu option
    created_reports == True

    # Displays a confirmation message
    print(f'''\nYour reports have been generated. 
To view them, open the files {cyan}task_overview.txt{reset} and {cyan}user_overview.txt{reset} or select {bold}Display Reports{reset} from the main menu.''')

# Presents two menu versions to the user, one for admins containing an additional option 's', and one for non-admins.
def main_menu():    
    while True:
        # Menu for admins. This includes the 'Display statistics' option. 
        if username == "admin":
            # Shows admin main menu options and gets selection, converted to lower case
            menu = input(f'''\n{yellow}{("-"*15)}[ {white}MAIN MENU{yellow} ]{("-"*15)}

r\t- Register a user (admin only)
ds\t- Display task and user statistics (admin only)
gr\t- Generate reports (admin only)
a\t- Add a task
va\t- View all tasks
vm\t- View my tasks
e\t- Exit
{("-"*43)}{reset}

Enter your choice here: ''').lower()
        
        # Shows non-admin main menu options and gets selection, converted to lower case
        else:
            menu = input(f'''\n{yellow}{("-"*15)}[ {white}MAIN MENU{yellow} ]{("-"*15)}
a\t- Add a task
va\t- View all tasks
vm\t- View my tasks
e\t- Exit
{("-"*43)}{reset}

Enter your choice here: ''').lower()
        # If the user selects 'r', allows them to register a new user (admin only)
        if menu == 'r':
            reg_user()
            
        # If the user selects 'ds', displays reports on the task and user statistics (admin only)
        elif menu == 'ds':
            display_stats()

        # If the user selects 'gr', creates reports on the task and user statistics (admin only)
        elif menu == 'gr':
            gen_reports()

        # If the user chooses 'a', this asks them to enter the task owner, title, description and due date. It adds the current date and defaults completeness to 'No'         
        elif menu == 'a':
            add_task()
            
        # If the user chooses 'va', this displays all the task information for all tasks in a readable format    
        elif menu == 'va':
            view_all()
    
        # If the user chooses 'vm', this displays all the task information only for tasks assigned to them, in a readable format
        # Then allows them to select their tasks and edit name, due date or completeness   Whe    
        elif menu == 'vm':
            view_mine()
           
        # When the user chooses 'e', prints a goodbye message and escapes the programme
        elif menu == 'e':
            print("\nYour session has ended. Goodbye\n")
            exit()

        else:
            print(f"\n{red}That selection is invalid. Please try again.{reset}")

#====Login and Main Menu====
# Creates a dictionary to hold the usernames and passwords in linked pairs
logins = {}

# Reads the file contents into the dictionary, splitting each line in two and assigning the first word to a 
# key and the second to a value. It also strips the comma from the first word.
with open("user.txt","r") as f:
    for user_info in f:
       (key, val) = user_info.split()
       key = key.strip(',')
       logins[key] = val

# Calls the login function (getting and validating input of username and password) and stores the returned username for use in other functions
username = login()

# Shows the main menu of options for the user
main_menu()
    
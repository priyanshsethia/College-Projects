"""
Created on Tuesday, October 5, 2021

@author : Priyansh Sethia
"""

# Import modules to use 'clear' & 'sleep' function
from os import system, name
from time import sleep

# Declaration on a list
contact = ["Ram", 989898854, "Shyam", 679487484, "Mohan", 894874783, "Ramesh", 4579821324, "Shubham", 4579813254]

# Function to clear the console.
def clear():                                                
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# A simple '-' layout.       
def layout():
    print("-"*35)
    
# A simple '=' layout.    
def layout1():
    print("="*35)
    
# A welcome page layout.
def welcome():
    clear()
    print("===================================")
    print("|                                 |")
    print("|          W E L C O M E          |")
    print("|                                 |")
    print("|                to               |")
    print("|                                 |")
    print("|         \" Contact Book \"        |")
    print("|                                 |")
    print("|---------------------------------|")
    print("|                                 |")
    print("|            Built by :           |")
    print("|         ----------------        |")
    print("|          Priyansh Sethia        |")
    print("|                                 |")
    print("|                                 |")
    print("===================================")
    sleep(3)

# Function to show all the contacts.
def Show_all_contact():
    print("Name\t\t Number")
    print()
    for a in range(0, len(contact), 2):
        name = contact[a]
        number = contact[a+1]
        print(name, "\t\t", number)
    print()
        
# Function to show contacts in different manner.      
def Show_Contacts():
    clear()
    while(True):                                            # Layout of show contacts.
        layout1()
        print(("-"*10),"Show contacts", ("-"*10))
        layout1()
        print()
        print("Please select any option :")
        print()
        print("1. Show all contacts")
        print("2. Show only contact name")
        print("3. Show only contact number")
        print("4. Back to Contact Book Menu")
        print()

        select = int(input("Enter Option No. : "))

        # Show all contacts.
        if select == 1:                                     
            clear()
            Show_all_contact()

        # Show only contact names.    
        elif select == 2:                                   
            clear()
            print("Contact Names : ")
            print()
            for a in range(0, len(contact), 2):
                print(contact[a])
            print()
            
        # Show only contact numbers.  
        elif select == 3:                                   
            clear()
            print("Contact Number : ")
            print()
            for a in range(0, len(contact), 2):
                print(contact[a+1])
            print()
            
        # Back to main menu.    
        elif select == 4:                                   
            clear()
            break
        
        # Error prevention code.
        elif select <= 0 or select >= 5:                    
            clear()
            layout()
            print("Message : Invalid input, please enter again.")
            layout()
            print()
            
# Function to add contact.      
def Add_Contact():
    clear()
    layout1()
    print(("-"*11),"Add Contact", ("-"*11))
    layout1()
    print()
    
    name = input("Enter Name : ")
    number = int(input("Enter Number : "))
    contact.append(name)
    contact.append(number)
    clear()
    print("Message : Contact added successfully.")
    print()

# Function to remove contact.    
def Remove_Contact():
    clear()
    layout1()
    print(("-"*9),"Remove Contact", ("-"*9))
    layout1()
    print()

    Show_all_contact()
    print("-"*45)
    
    element = input("Enter contact name or number to remove : ")

    # To remove contact through number.
    if element.isdigit():
        element=int(element)
        inx = contact.index(element)
        contact.pop(inx)
        contact.pop((inx-1))

    # To remove contact through name.
    else:
        inx = contact.index(element)
        contact.pop(inx)
        contact.pop(inx)
    clear()
    print("Message : Contact removed successfully.")
    print()

# Function to search contact with both 'name' & 'number'.
def Search_Contact():
    clear()
    layout1()
    print(("-"*9),"Search Contact", ("-"*9))
    layout1()
    print()
    
    element = input("Enter contact name or number to search : ")

    # To search contact through number.
    if element.isdigit():
        element=int(element)
        for search in range(0,len(contact)):
            if contact[search] == element:
                clear()
                print(contact[search-1], contact[search])
                print()
                break
            else:
                clear()
                print("Match not found.")
                print()

    # To search contact through number.       
    else:
        for search in range(0,len(contact)):
            if contact[search] == element:
                clear()
                print(contact[search], contact[search+1])
                print()
                break
            else:
                clear()
                print("Match not found.")
                print()

# Function to sort contact list based on names in both ascending & descending order.
def Sort_Contact():

    # Create a list('name_list') to contain only names.
    name_list = []                                      
    for a in range(0, len(contact), 2):
        name_list.append(contact[a])
    
    clear()
    layout1()
    print(("-"*10),"Sort Contacts", ("-"*10))
    layout1()
    print()
    print("Please select any option :")
    print()
    print("1. Ascending Order")
    print("2. Descending Order")
    print()

    select = int(input("Enter Option No. : "))

    # String sort algorithm (ascending oreder.)
    if select == 1:                                     
        for i in range (0, len(name_list)):             
            for j in range(i + 1, len(name_list)):
                if(name_list[i] > name_list[j]):
                    temp = name_list[i]
                    name_list[i] = name_list[j]
                    name_list[j] = temp
                    
    # String sort algorithm (descending oreder).
    elif select == 2:                                   
        for i in range (0, len(name_list)):            
            for j in range(i + 1, len(name_list)):
                if(name_list[i] < name_list[j]):
                    temp = name_list[i]
                    name_list[i] = name_list[j]
                    name_list[j] = temp

    # Create a list('number_list') to contain only numbers.
    number_list = []
    for a in range(0, len(name_list)):
        for b in range(0, len(contact)):
            if name_list[a] == contact[b]:
                c = contact[b+1]
                number_list.append(c)

    # Create a list('sort_list') to join both name & numbers in a row to sort them.
    sort_list = []

    for d in range(0, len(name_list)):
        sort_list.append(name_list[d])
        sort_list.append(number_list[d])
    
    clear()
    print("Soring of Contacts : ")
    print()
    print(sort_list)
    print()

# Main Menu
def Main_menu():
    welcome()
    clear()
    while(True):

        # Layout of main menu.
        layout1()
        print(("-"*10),"Contact Book", ("-"*10))
        layout1()
        print()
        print("Please select any option :")
        print()
        print("1. Show contacts")
        print("2. Add Contact")
        print("3. Remove Contact")
        print("4. Search Contact")
        print("5. Sort Contact")
        print("6. Exit")
        print()

        # Selection code.
        select = int(input("Enter Option No. : "))

        # Show contacts.
        if select == 1:
            clear()
            Show_Contacts()

        # Add contact.    
        elif select == 2:
            Add_Contact()

        # Remove contact.
        elif select == 3:
            Remove_Contact()

        # Search contact.
        elif select == 4:
            Search_Contact()

        # Sort contacts.
        elif select == 5:
            Sort_Contact()

        # Exit from the program.
        elif select == 6:
            print("Exiting...")
            break

        # Error prevention code.
        elif select <= 0 or select >= 7:
            clear()
            layout()
            print("Message : Invalid input, please enter again.")
            layout()
            print()

            
# Calling Main_menu()
Main_menu()

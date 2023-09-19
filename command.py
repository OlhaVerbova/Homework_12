from classes import AddressBook, Birthday
from classes import Record
from classes import Phone

global command_word
addressBook = AddressBook()
addressBook.give_store_data()




#decorator
def input_error(function):
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            return 'Invalid name'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return "Invalid input format."
        except TypeError:
            return 'Invalid command'
    return inner

# main functions
def hello():
    return "How can I help you?"

def show_all():
    result_list = addressBook.return_all_records()
    format_list = "|{:^30s}|{:^40s}|{:^10s}|\n".format("Name", "Phone", "Birthday")
    format_list += "-" * 82 + "\n"

    for dictionary in result_list:
        name = dictionary["Name"]
        phone = dictionary["Phone"]
        birthday = dictionary["Birthday"]

        format_list += "|{:^30s}|{:^40s}|{:^10s}|\n".format(name, phone, birthday)

    return format_list


def say_good_bye():
    return "Good bye!"

@input_error
def add_new_telephone_contact(text):    
    text_list = text.split()
    already_enter_contacts = addressBook.get_keys_from_all_records() 
    
    if text_list[1] in already_enter_contacts:
        return f"{text_list[1]} is already in our book"
    else:
        if len(text_list) == 4:
            name =text_list[1].title()           
            phone = Phone(text_list[2])
            birthday = Birthday(text_list[3])
            record = Record(name, phone, birthday)            
            addressBook.add_record(record)

        if len(text_list) == 3:
            name =text_list[1].title()           
            phone = Phone(text_list[2])
            record = Record(name, phone)
            addressBook.add_record(record)          
    
        if len(text_list) == 2:
            name =text_list[1].title()              
            record = Record(name)  
            addressBook.add_record(record) 
    addressBook.save_contacts()           

def add_new_phone_to_contact(text):
    text_list = text.split()
    name_to_find = text_list[2].title()  
    if name_to_find in addressBook.data.keys(): 
        existing_record = addressBook.data[name_to_find]
        existing_record.add_phone(Phone(text_list[3]))
    else:
        return f"We dont have {text_list[2]} in our addressBook, please, try again"  
    addressBook.save_contacts() 

def add_new_birthday_to_contact(text):
    text_list = text.split()
    name_to_find = text_list[2].title()  
    if name_to_find in addressBook.data.keys(): 
        existing_record = addressBook.data[name_to_find]
        existing_record.add_birthday(Birthday(text_list[3]))
    else:
        return f"We dont have {text_list[2]} in our addressBook, please, try again"  
    addressBook.save_contacts() 

def days_to_birthday(text, address_Book): 
    text_list = text.split()     
    name = text_list[3].title()

    if name in address_Book.data.keys():
        existing_record = address_Book.data[name]
        if existing_record.birth_day:
            birthday_value = existing_record.birth_day[0].value 
            days_until_birthday = existing_record.day_to_next_birthday(birthday_value)
            return f"{days_until_birthday} days before {name}'s birthday"
        else:
            return f"{name} does not have a birthday in the address book."
    else:
        return f"We don't have {name} in our address book, please try again."

def delete_phone(text):
    text_list = text.split()
    name_to_find = text_list[2].title()
    if name_to_find in addressBook.data:
        existing_record = addressBook.data[name_to_find]
        existing_record.remove_phone(Phone(text_list[3]))        
    else:
        return f"We dont have {text_list[2]} in our addressBook, please, try again"    
    addressBook.save_contacts() 

    
@input_error
def change_phone_number(text):
    text_list = text.split()
    name_to_find = text_list[1].title()
    if name_to_find in addressBook.data.keys():
        existing_record = addressBook.data[name_to_find]
        existing_record.change_phone(Phone(text_list[2]),Phone(text_list[3]))
    addressBook.save_contacts() 


@input_error
def show_name_contact(text):
    text_list = text.split()
    all_records = addressBook.return_all_records()
    for dictionary in all_records:
        for key, value in dictionary.items():
            if text_list[1].title() in value:
                return dictionary.get("Name", "Sorry, but i don`t find this contact, please, try again")

def show_contact_info(text):
    text_list = text.split()
    all_records = addressBook.return_all_records()
    for dictionary in all_records:
        for key, value in dictionary.items():
            if text_list[2].title() in key:                
                return f"Contact {dictionary.get('Name')} has phone(s): {dictionary.get('Phone')}, birthday: {dictionary.get('Birthday', '-')}"
#HW12 here:
def search_in_name_phone(text):
    text_list = text.split()
    all_records = addressBook.return_all_records()
    
    user_enter = text_list[1].title()
    result = []

    for i in all_records:
        name = i.get("Name")
        phone = i.get("Phone")

        if user_enter in name or user_enter in phone:
            result.append(f"contact {name} has phone(s): {phone}")

    if result:
        return "\n".join(result)
    else:
        return "I didn't find a match."
            
    
            
def text_helper():
    help_text = "Help on how to enter commands correctly\n"
    help_text += "show all    --> show you all records\n"
    help_text += "add (name)    --> record contact\n"
    help_text += "add (name phone)    --> record name + phone\n"
    help_text += "add (name phone birthday)    --> record name + phone + birthday\n"
    help_text += "change (name old_phone new_phone)    --> changes changes the old phone number to a new one for a contact\n"
    help_text += "add phone (name, phone)    --> add phone to contact (name)\n"
    help_text += "add birthday (name, birthday)    --> add birthday to contact (name)\n"
    help_text += "days to birthday (name)    --> show days to birthday to contact (name)\n"
    help_text += "delete phone (name phone)    --> delete phone for a contact\n"
    help_text += "phone (phone)    --> show you contact`s owner\n"
    help_text += "show contact (name )    --> show you contact`s phone(s)\n"
    help_text += "search (name or phone)    --> show you contact`s name and phone(s)\n"
    help_text += "close/good bye/exit    -->  will end the session\n"    
    return help_text
   
def bot_operation(text):
    match text:
        case "hello":
            result = hello()   
                     
        case "close":
            result = say_good_bye()  

        case "good bye":
            result = say_good_bye()  

        case "exit":
            result = say_good_bye()   

        case "show all":
            result = show_all()           
            
        case "change":
            result = change_phone_number(command_word)
            
        case "phone":
            result = show_name_contact(command_word)

        case "add phone": 
            result = add_new_phone_to_contact(command_word)

        case "add":
            result = add_new_telephone_contact(command_word)

        case "delete phone":
            result = delete_phone(command_word)

        case "show contact":
            result = show_contact_info(command_word)
        
        case "help":
            result = text_helper()
        
        case "add birthday":
            result = add_new_birthday_to_contact(command_word)
        
        case "days to birthday":
            result = days_to_birthday(command_word, addressBook)
        
        case "search":
            result = search_in_name_phone(command_word) 
            
    return result
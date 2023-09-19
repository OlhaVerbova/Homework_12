from collections import UserDict
import re
from datetime import datetime
import pickle

class AddressBook(UserDict):     

    file_name = 'addressBook.bin'

    def add_record(self, record):
        self.data[record.name.value] = record      
    
    def return_all_records(self):
        all_records = []
        for name, record in self.data.items():
            temp = {}
            phones = ', '.join(phone.value for phone in record.phones if phone.value)
            birth_day = ', '.join(birthday.value for birthday in record.birth_day) if record.birth_day else ""
            temp.update({"Name": name, "Phone": phones, "Birthday": birth_day})
            all_records.append(temp)
        return all_records        
        
    
    def get_keys_from_all_records(self):
        all_records = self.return_all_records()  
        keys = [list(i.keys())[0] for i in all_records]
        return keys
    
    def iterator(self, N = 1):
        for key, value in self.data.items():
            result = list(self.data.values())

            for i in range(0, len(result), N):
                yield key, result[i:i + N]

    #HW12 here:
    def save_contacts(self):
        with open(self.file_name, 'wb') as fh:
            pickle.dump(self.data, fh)
        

    def give_store_data(self):
        try:
            with open(self.file_name, 'rb') as fh:
                self.data = pickle.load(fh)
        except:
            return "Error during data loading"


class Field:
    def __init__(self, value):
        self.value = value      

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value      


class Name(Field):    
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value 


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        new_phone = (
            str(new_value).strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if len(new_phone) == 10:
            result = '+38' + str(new_phone)
        elif len(new_phone) == 12:
            result = '+' + str(new_phone)
        else:
            result = False
        self._value = result 
        return result
    
    
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
    
    def __str__(self):       
        return self._value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        birth_str = str(new_value)
        find_num = re.findall("\d+", birth_str)        
        find_day = int(find_num[0])
        find_month = int(find_num[1])
        find_year = int(find_num[2])
        birth_day = datetime(year=find_year,month=find_month,day=find_day)
        now_day = datetime.now()
        if birth_day < now_day:        
            self._value = birth_str  

class Record:
    def __init__(self, name, phone=None, birthday = None):
         self.name = Name(value=name)
         self.phones = []
         self.birth_day = []
         
         if phone:
            self.phone = Phone(value=phone)
            self.phones.append(phone) 
        
         if birthday:
            self.birthday = Birthday(value=birthday)
            self.birth_day.append(birthday) 

    def add_phone(self, new_phone):
        self.phones.append(new_phone)
    
    def add_birthday(self, new_birthday):
        self.birth_day = [new_birthday]

    def remove_phone(self, phone):
        for index, values in enumerate(self.phones):
            if values.value == phone.value:
                self.phones.pop(index)

    def change_phone(self, phone, new_phone):       
        for index, values in enumerate(self.phones):
            if values.value == phone.value:
                self.phones[index] = new_phone
                print(f"Phone '{phone.value}' changed to '{new_phone.value}'.")
                return
        print(f"Phone '{phone.value}' not found.")    
    
    def day_to_next_birthday(self, birth):
        find_num = re.findall("\d+", birth)
        find_day = int(find_num[0])
        find_month = int(find_num[1])             
        
        now_day = datetime.now()        
        replase_date = datetime(year=now_day.year,month=find_month,day=find_day)
        
        if now_day < replase_date:
            result_day = replase_date - now_day
        else:
            replase_date = datetime(year=now_day.year + 1,month=find_month,day=find_day)
            result_day = replase_date - now_day
        return result_day.days






    
 

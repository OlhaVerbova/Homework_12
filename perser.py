command_words = ["hello","add","change","phone","show all",
                 "good bye", "close","exit", "add phone", "delete phone", 
                 "show contact", "help", "add birthday", "days to birthday", "search"]

def command_recognizer(command_text: str):
    
    triger_list = []
    
    for word in command_words:
        if word in command_text:
            triger_list.append(word)
    return triger_list
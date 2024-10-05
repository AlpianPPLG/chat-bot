import random

def random_string():
    random_list = [
        "Please try typing something more descriptive.",        
        "Would you mind trying to repeat that?",
        "I can't answer that yet, please try asking something else."    
    ]

    list_count = len(random_list)
    random_item = random.randrange(list_count)

    return random_list[random_item]

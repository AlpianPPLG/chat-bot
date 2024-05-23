import random


def random_string():
    random_list = [
        "Silakan coba menulis sesuatu yang lebih deskriptif.",        
        "Apakah kamu keberatan mencoba mengulanginya?",
        "Saya belum bisa menjawabnya, silakan coba tanyakan hal lain."    
    ]

    list_count = len(random_list)
    random_item = random.randrange(list_count)

    return random_list[random_item]

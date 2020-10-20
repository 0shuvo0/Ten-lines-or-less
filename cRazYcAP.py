import random

def crazyCap(text):
    output = ""
    for char in text:
        output += char.upper() if random.random() > 0.5 else char.lower()
    return output

print(crazyCap("Hello world"))

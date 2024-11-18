"""
This file is just for testing purpose
"""

abc = input("what your age")

if abc.isdigit():
    print(f"{int(abc)} This is a valid age of you")

else:
    print("You need to write numbers not alphabets")
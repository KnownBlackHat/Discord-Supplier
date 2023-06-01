import os

with open("list.txt", "r") as file:
    for line in file.readlines():
        os.system(f"python supplier.py {line}")

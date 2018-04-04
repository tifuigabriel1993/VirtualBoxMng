import uuid
import time
from commands import deploy
from commands import halt
from commands import find_all_machines

import virtualbox


machines_dict = find_all_machines()

def show_machine_menu():
    menu_index = 1
    for machine_name in machines_dict.items():
        print("{}. {}".format(menu_index, machine_name[0]))
        menu_index += 1

show_machine_menu()

is_machine_selected = False
selected_machine = None

while not is_machine_selected:
    machine_name = input("Select machine name: ")
    if machine_name in machines_dict:
        is_machine_selected = True
        selected_machine = machines_dict[machine_name]
    else:
        print("Machine name doesn't exist")

machine_name = input("Insert machine name: ")
deploy(selected_machine, machine_name, 1, [])
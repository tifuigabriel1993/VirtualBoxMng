from vboxapi import VirtualBoxManager
from configuration import vm_configuration as vm_configurator
from configuration.vm_configuration import ResourceConstants
from configuration.util import copy_and_rename
import subprocess
import shutil

vb_manager = VirtualBoxManager(None, None)
vbox = vb_manager.getVirtualBox()

SHARED_FOLDER_HOME = "H:/"
SERVICE_TEMPLATE_FILE = "vmconfig_template.service"
CONFIG_FILE_PATTERN = "{}-config.service"
SCRIPT_TAG = "__script__here__"

def find_all_machines():
    vboxVMList = vb_manager.getArray(vbox, 'machines')
    machines = {}
    for machine in vboxVMList:
       machines[machine.name] = machine
    return machines

def deploy(fromMachine, new_machine_name, mode, options):
    new_machine = vbox.createMachine("", new_machine_name, [], "", "forceOverwrite=1")
    fromMachine.cloneTo(new_machine, mode, options)
    vbox.registerMachine(new_machine)

    session = vb_manager.mgr.getSessionObject(vbox)
    vm_configurator.config_machine(session, new_machine)
    sharedfolder_path = create_sharedfolder(new_machine_name)

    machine_service_name = CONFIG_FILE_PATTERN.format(new_machine_name)
    copy_and_rename("configuration/", SERVICE_TEMPLATE_FILE, machine_service_name)

    config_dict = vm_configurator.get_machine_def_configuration(fromMachine.name)
    service_local_path = create_systemd(config_dict, "configuration/" + machine_service_name)

    shutil.copy(service_local_path, sharedfolder_path)

def create_sharedfolder(machine_name):
    machine_shared_folder = SHARED_FOLDER_HOME + machine_name
    shared_folder_name = "{}-configuration".format(machine_name)

    subprocess.call(['C:\Program Files\Oracle\VirtualBox\VBoxManage.exe',
                     'sharedfolder',
                     'add',
                     machine_name,
                     '-name',
                     shared_folder_name,
                     '-hostpath',
                     machine_shared_folder
                     ])

    return machine_shared_folder

def create_systemd(config_dict, service_file):
    apps = config_dict[ResourceConstants.SYSTEM][ResourceConstants.APS]

    apps_param = ""
    for app in apps:
        apps_param = app + " "


    f = open(service_file, 'r')
    filedata = f.read()
    f.close()

    script_path_template = "/service/vmconfig.sh {}"
    service_content = filedata.replace(SCRIPT_TAG, script_path_template.format(apps_param))

    f = open(service_file, 'w')
    f.write(service_content)
    f.close()

    return service_file;

def halt(machine_name):
    subprocess.call(['C:\Program Files\Oracle\VirtualBox\VBoxManage.exe',
                     'controlvm',
                     machine_name,
                     'pause'
                     ])

def start(machine_name):
    subprocess.call(['C:\Program Files\Oracle\VirtualBox\VBoxManage.exe',
                     'controlvm',
                     machine_name,
                     'resume'
                     ])

def destroy(machine_name):
    subprocess.call(['C:\Program Files\Oracle\VirtualBox\VBoxManage.exe',
                     'unregistervm',
                     machine_name,
                     ])


if __name__ == "__main__":
    machine_service_name = CONFIG_FILE_PATTERN.format("test_new")
    copy_and_rename("configuration/", SERVICE_TEMPLATE_FILE, machine_service_name)

    config_dict = vm_configurator.get_machine_configuration("centos")
    path = create_systemd(config_dict, "configuration/" + machine_service_name)

    shutil.copy(path, "H:/shared_folders/test")

    print(path)

import vboxapi
import yaml
from configuration.util import MachineLocker
from configuration.util import ResourceConstants

vbm = vboxapi.VirtualBoxManager(None, None)

default_machine_config = "default"
resources_config = "resources"

def config_machine(vb_session, machine, settings_file_path = None):
    config_path = "configuration/vm_config.yml"
    if settings_file_path != None:
        config_path = settings_file_path

    in_stream = open(config_path, "r")
    vm_configs_dict = yaml.load(in_stream)

    machine_config = get_machine_configuration(machine.name, vm_configs_dict)
    resources_config = machine_config[ResourceConstants.RESOURCES]
    with MachineLocker(vb_session, machine, vbm.constants.LockType_Write) as vb_session:
        vb_session.machine.memorySize = resources_config[ResourceConstants.RAM]
        vb_session.machine.CPUCount = resources_config[ResourceConstants.CPU]
        vb_session.machine.saveSettings()

def get_machine_configuration(machine, vm_configs_dict):
    try:
        machine_config = vm_configs_dict[machine]
    except KeyError as ke:
        machine_config = vm_configs_dict[default_machine_config]
    return machine_config

def get_machine_def_configuration(machine):
    config_path = "configuration/vm_config.yml"
    in_stream = open(config_path, "r")
    vm_configs_dict = yaml.load(in_stream)
    try:
        machine_config = vm_configs_dict[machine]
    except KeyError as ke:
        machine_config = vm_configs_dict[default_machine_config]
    return machine_config
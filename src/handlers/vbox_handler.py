from time import sleep
import os
import sys
import random
import shelve
import logging

import tarfile
import tempfile

import virtualbox
from src.utils.utils import extract_resource_group, get_image, extract_iso, extract_metadata
from src.grpc_connector.client_pb2 import ResourceGroupProto, Network, MetadataEntry, VDU, PoP


def start_and_wait_vm(name):
    vbox = virtualbox.VirtualBox()
    session = virtualbox.Session()

    machine = vbox.find_machine(name)
    if machine is not None:
        progress = machine.launch_vm_process(session, "headless", "")
        while progress.percent < 100 or not progress.completed:
            logging.debug(progress.percent)
            sleep(1)

        # Wait for machine to stop
        while machine.state not in [virtualbox.library.MachineState.saved, virtualbox.library.MachineState.aborted,
                                    virtualbox.library.MachineState.powered_off]:
            sleep(5)
            logging.debug("Machine still running")
        while session.state != virtualbox.library.SessionState.unlocked:
            sleep(2)
            logging.debug("Waiting for machine to be unlocked")
            logging.debug(session.state)
        delete_vm(machine.name)


def start_vm(name):
    vbox = virtualbox.VirtualBox()
    session = virtualbox.Session()
    machine = vbox.find_machine(name)
    if machine is not None:
        progress = machine.launch_vm_process(session, "headless", "")
        while progress.percent < 100 or not progress.completed:
            logging.debug(" Starting vm: " + str(progress.percent))
            sleep(1)
        logging.debug("Machine " + machine.name + " started")


def stop_vm(name):
    vbox = virtualbox.VirtualBox()
    machine = vbox.find_machine(name)
    session = machine.create_session()
    progress = session.console.power_down()
    while progress.percent < 100 or not progress.completed:
        logging.debug("Powering down: " + str(progress.percent))
        sleep(1)


def delete_vms(package_name):
    vms = _get_vms_from_db(package_name)
    for vm in vms:
        delete_vm(vm)


def delete_vm(name):
    vbox = virtualbox.VirtualBox()
    machine = vbox.find_machine(name)
    if machine.session_state != virtualbox.library.SessionState.unlocked:
        if machine.state not in [virtualbox.library.MachineState.saved, virtualbox.library.MachineState.aborted,
                                 virtualbox.library.MachineState.powered_off]:
            stop_vm(name)
            while machine.session_state != virtualbox.library.SessionState.unlocked:
                sleep(2)
                logging.debug("Waiting for machine to be unlocked")
                logging.debug(machine.session_state)
        else:
            raise ValueError("Cant delete machine " + name + " because there is a running session!")

    machine.unregister(virtualbox.library.CleanupMode.detach_all_return_none)
    machine.delete_config(media=[])


def list_vms():
    vbox = virtualbox.VirtualBox()
    return [vm.name for vm in vbox.machines]


def get_file(machine):
    vbox = virtualbox.VirtualBox()
    machine = vbox.find_machine(machine)
    session = machine.create_session()

    # TODO: UPDATE
    gs = session.console.guest.create_session("user", "pass")
    gs.copy_from("from", "to")
    gs.close()


def execute_command(machine, command):
    vbox = virtualbox.VirtualBox()
    vm = vbox.find_machine(machine)
    session = vm.create_session()
    # TODO: UPDATE
    gs = session.console.guest.create_session("user", "pass")
    process, stdout, stderr = gs.execute(command)


def get_ip(machine):
    vbox = virtualbox.VirtualBox()
    vm = vbox.find_machine(machine)
    res = vm.enumerate_guest_properties('/VirtualBox/GuestInfo/Net/0/V4/IP')
    ip = res[1][0]
    return ip


def get_metadata(machine):
    vbox = virtualbox.VirtualBox()
    vm = vbox.find_machine(machine)
    metadata = []
    types, values, timestamps, flags = vm.enumerate_guest_properties("")
    for t, v in zip(types, values):
        metadata.append(MetadataEntry(key=t, value=v))
    return metadata


def create_from_appliance(appliance_path, iso_path, network_name, root_dir):
    vbox = virtualbox.VirtualBox()
    appliance = vbox.create_appliance()
    logging.debug(root_dir + "/" + appliance_path)
    appliance.read(root_dir + "/" + appliance_path)

    progress = appliance.import_machines()
    while progress.percent < 100 or not progress.completed:
        logging.debug("Importing appliance: " + str(progress.percent))
        sleep(1)

    ports = []
    for machine in appliance.machines:
        session = vbox.find_machine(machine).create_session()
        m = session.machine
        m.memory_size = 5000
        medium = vbox.open_medium(location=root_dir + "/" + iso_path,
                                  device_type=virtualbox.library.DeviceType.dvd,
                                  access_mode=virtualbox.library.AccessMode.read_write, force_new_uuid=True)
        m.attach_device(name="IDE", controller_port=0, device=0,
                        type_p=virtualbox.library.DeviceType.dvd, medium=medium)

        sp = m.get_serial_port(0)
        sp.enabled = True

        if network_name.lower() == "nat":
            network = m.get_network_adapter(0)
            network.attachment_type = virtualbox.library.NetworkAttachmentType.nat
            network.enabled = True
            port = random.randint(50060, 50100)
            network.nat_engine.add_redirect("ssh", virtualbox.library.NATProtocol.tcp, "", port, "", 22)
            ports.append(port)
        else:
            raise ValueError("Only NAT networking is supported at the moment!")

        m.save_settings()
        session.unlock_machine()

    return appliance.machines, ports


def import_appliance_from_package(tar, root_dir):
    pops = []
    networks = []
    vdus = []

    temp = tempfile.NamedTemporaryFile(delete=True)
    temp.write(tar)
    package = tarfile.open(temp.name, "r")

    metadata = extract_metadata(package)
    rg_name = ""
    if "name" in metadata:
        rg_name = metadata["name"]
    else:
        rg_name = str(random.randint(100, 999))

    rg = extract_resource_group(package)
    overall_machines = []
    for vdu in rg["vdus"]:

        image_path = vdu["imageName"]
        local_image_path = get_image(image_path, vdu["name"])
        vm_name = vdu["name"]
        net_name = vdu["netName"]
        net = Network(name=net_name, cidr="", poPName="vbox", networkId=net_name)
        networks.append(net)


        iso_path = extract_iso(package, vm_name=vm_name)
        machines, ports = create_from_appliance(appliance_path=local_image_path, iso_path=iso_path,
                                                network_name=net_name, root_dir=root_dir)
        for machine, port in zip(machines, ports):
            start_vm(machine)
            ip = "localhost"
            metadata = get_metadata(machine)
            metadata.append(MetadataEntry(key="port", value=str(port)))
            extract_auth_credentials(machine, vdu["metadata"])
            vdu = VDU(name=machine, imageName=net_name, netName=net_name, computeId=machine, ip=ip,
                      metadata=metadata)
            vdus.append(vdu)
        overall_machines.extend(machines)
    _save_to_db(rg_name, overall_machines)
    return ResourceGroupProto(name=rg_name, pops=pops, networks=networks, vdus=vdus)


def _save_to_db(name, value):
    db = shelve.open('packages.db')
    db[str(name)] = value
    db.close()


def _get_vms_from_db(package_name):
    db = shelve.open('packages.db')

    value = None
    if package_name in db:
        value = db[package_name]
    db.close()

    return value


def extract_auth_credentials(name, metadata):
    db = shelve.open('auths.db')

    auth = {}
    for kvp in metadata:
        auth[kvp["key"]] = kvp["value"]

    db[name + "_credentials"] = auth
    db.close()

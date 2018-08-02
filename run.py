import sys
import time
import atexit
import logging
from logging import handlers
import os

import grpc
import src.grpc_connector.client_pb2_grpc as client_pb2_grpc
from concurrent import futures

import src.grpc_connector.client_pb2 as client_pb2
from src.utils import epm_utils as utils
from src.utils import utils as u
from src.handlers import vbox_handler
from src.handlers import ssh_client

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

root_dir = os.path.dirname(os.path.abspath(__file__))


class VirtualBoxHandlerService(client_pb2_grpc.OperationHandlerServicer):
    def Create(self, request, context):
        rg = vbox_handler.import_appliance_from_package(request.file, root_dir)
        return rg

    def Remove(self, request, context):
        package_name = request.resource_id
        vbox_handler.delete_vms(package_name)
        return client_pb2.Empty()

    def Start(self, request, context):
        name = request.vdu.name
        vbox_handler.start_vm(name)
        return client_pb2.Empty()

    def Stop(self, request, context):
        name = request.vdu.name
        vbox_handler.stop_vm(name)
        return client_pb2.Empty()

    def ExecuteCommand(self, request, context):
        instance_id = request.vdu.name
        port = u.get_port_from_vdu(request.vdu)
        if port == None:
            raise ValueError("VDU metadata does not contain a port")
        command = request.property[0]

        ssh_exec = ssh_client.SSHExecutor(vm_name=instance_id, port=port)

        logging.info("Executing command " + command)
        output = ssh_exec.execute_command(command)
        return client_pb2.StringResponse(response=output)

    def DownloadFile(self, request, context):
        instance_id = request.vdu.name
        port = u.get_port_from_vdu(request.vdu)
        if port == None:
            raise ValueError("VDU metadata does not contain a port")
        ssh_exec = ssh_client.SSHExecutor(vm_name=instance_id, port=port)
        path = request.property[0]
        logging.info("Downloading file " + path)
        output = ssh_exec.download_file_from_container(path)
        return client_pb2.FileMessage(file=output)

    def UploadFile(self, request, context):
        instance_id = request.vdu.name
        port = u.get_port_from_vdu(request.vdu)
        if port == None:
            raise ValueError("VDU metadata does not contain a port")
        ssh_exec = ssh_client.SSHExecutor(vm_name=instance_id, port=port)
        type = request.property[0]
        if (type == "withPath"):
            remotePath = request.property[4]
            hostPath = request.property[3]
            logging.info("Uploading a file " + hostPath + " to " + remotePath)
            ssh_exec.upload_file_from_path(hostPath=hostPath, remotePath=remotePath)
            return client_pb2.Empty()
        else:
            path = request.property[0]
            logging.info("Uploading a file to " + path)
            file = request.file
            ssh_exec.upload_file(path, file)
            return client_pb2.Empty()

def serve(port="50054"):
    logging.info("Starting server...")
    logging.info("Listening on port: " + port)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    client_pb2_grpc.add_OperationHandlerServicer_to_server(
        VirtualBoxHandlerService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


adapter_id = ""
epm_ip = ""


@atexit.register
def stop():
    logging.info("Exiting")
    if adapter_id != "" and epm_ip != "":
        logging.info("DELETING ADAPTER")
        utils.unregister_adapter(epm_ip, adapter_id)


if __name__ == '__main__':
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)
    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(format)
    log.addHandler(ch)

    fh = handlers.RotatingFileHandler("epm-adapter-vbox.log", maxBytes=(1048576 * 5), backupCount=7)
    fh.setFormatter(format)
    log.addHandler(fh)
    logging.info("\n")

    if "--register-adapter" in sys.argv:
        if len(sys.argv) == 4:
            logging.info("Trying to register pop to EPM container...")
            adapter_id = utils.register_adapter(ip=sys.argv[2], vbox_ip=sys.argv[3])
            epm_ip = sys.argv[2]
        else:
            ip = "elastest-epm"
            virtualbox_ip = "elastest-epm-adapter-virtualbox"
            adapter_id = utils.register_adapter(ip=ip, vbox_ip=virtualbox_ip)
            epm_ip = ip
    serve()

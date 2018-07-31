import grpc
import src.grpc_connector.client_pb2_grpc as client_pb2_grpc
import src.grpc_connector.client_pb2 as client_pb2
import time
import requests
import json
import logging

max_timeout = 10


def register_adapter(ip, vbox_ip):
    channel = grpc.insecure_channel(ip + ":50050")
    stub = client_pb2_grpc.AdapterHandlerStub(channel)
    endpoint = vbox_ip + ":50054"
    adapter = client_pb2.AdapterProto(type="virtualbox", endpoint=endpoint)

    i = 0
    while i < 10:
        pop_vbox = {"name": "vbox-" + vbox_ip,
                       "interfaceEndpoint": vbox_ip,
                       "interfaceInfo":[{"key": "type","value": "virtualbox"}]}

        headers = {"accept": "application/json","content-type": "application/json"}
        try:
            identifier = stub.RegisterAdapter(adapter)
            r = requests.post('http://' + ip + ':8180/v1/pop', data=json.dumps(pop_vbox), headers=headers)
            logging.info("Adapter registered")
            logging.info(str(r.status_code) + " " + r.reason)
            return identifier.resource_id
        except:
            logging.info("Still not connected")
        time.sleep(11)
        i += 1
    return ""


def unregister_adapter(ip, id):
    channel = grpc.insecure_channel(ip + ":50050")
    stub = client_pb2_grpc.AdapterHandlerStub(channel)
    identifier = client_pb2.ResourceIdentifier(resource_id=id)
    stub.DeleteAdapter(identifier)

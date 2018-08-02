import json
import validators
import urllib3
import codecs
import yaml
import os

from src.grpc_connector.client_pb2 import VDU

def extract_resource_group(tar):
    rg = None
    for member in tar.getmembers():
        if ".json" in member.name:
            rg = tar.extractfile(member.name)
    if rg is None:
        return None
    reader = codecs.getreader("utf-8")
    return json.load(reader(rg))


def extract_iso(tar, vm_name):
    if not os.path.isdir("isos"):
        os.mkdir("isos")
    path = ""
    for member in tar.getmembers():
        if ".iso" in member.name:
            path = "isos/" + vm_name + ".iso"
            f = open(path, "wb")
            f.write(tar.extractfile(member.name).read())
            f.close()
    return path


def get_image(image_path, name):
    if validators.url(image_path):
        if not os.path.isdir("images"):
            os.mkdir("images")

        http = urllib3.PoolManager()
        r = http.request('GET', image_path, preload_content=False)
        download_path = "images/" + name + ".ova"

        # Download image
        chunk_size = 1024
        with open(download_path, 'wb') as out:
            while True:
                data = r.read(chunk_size)
                if not data:
                    break
                out.write(data)

        # Return local image path
        return download_path
    else:
        return image_path


def extract_metadata(tar):
    metadata = None
    for member in tar.getmembers():
        if member.name.lower() == "metadata.yaml" or member.name.lower() == "metadata.yml":
            metadata = tar.extractfile(member.name)
    if metadata is None:
        return None
    return yaml.load(metadata.read())


def get_port_from_vdu(vdu):

    port = None
    metadata = vdu.metadata
    for kvp in metadata:
        if kvp.key == "port":
            port = int(kvp.value)
    return port
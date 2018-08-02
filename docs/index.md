# Elastest Platform Manager Virtualbox adapter

## Important

Before using the adapter even in a seperate docker container you need to install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Supported VM types
Currently the virtualbox adapter supports only importing appliances in **.ova** of **.ovf** format. 
It is designed for creating Virtual Machines with cloud images.

## Supported Networking
Currently the virtualbox adapter supports only the NAT networking options from virtualbox. 
For supporting SSH-ing into the created machine the default SSH port of the machine is mapped to a random port on the
host between 50060 and 50100. The port is then sent back when the machine is created.

## Creating the Virtualbox Package

The virtualbox package should follow the following structure:

- metadata.yaml
- resourcegroup.json
- iso/seed.iso 
- images/ (OPTIONAL)

### Metadata

This is an example **Metadata** file:
```yaml
name: example-name
type: docker-compose
pop: pop-name # OPTIONAL: specify the name of the pop for deploying the package
```

### Resource Group and Images

This is an example of the Resource Group: 
```json
{
  "name": "testGroup1",
  "vdus": [
    {
      "name": "testVM",
      "imageName": "https://cloud-images.ubuntu.com/releases/16.04/release/ubuntu-16.04-server-cloudimg-amd64.ova",
      "netName": "nat",
      "poPName": "virtualbox",
      "metadata": [
        {
          "key": "username",
          "value": "ubuntu"
        },
        {
          "key": "password",
          "value": "passw0rd"
        }
      ]
    }
  ],
  "networks": [
    {
      "name":"nat  ",
      "poPName":"virtualbox"
    }
  ]
}
```

There are two options for specifying the appliance that will be imported:
1) Specifying a link - in the imageName of the VDU you can specify the link to the appliance, this will then be downloaded
and used when importing the appliance into virtualbox
2) Add it to the tar in the images folder - then you also have to specify its correct name in the imageName variable, so that
the adapter knows it should import it.


In the metadata options you should specify the credentials needed for ssh-ing into the machine after it is created.
This is done to enable the runtime operations.

### ISO

The seed.iso is used to provide data about the user on boot up. Here is an example of how it can look:

- meta-data
- user-data

meta-data example:

```yaml
local-hostname: localhost
```

user-data example:

```yaml
#cloud-config
password: passw0rd
chpasswd: { expire: False }
ssh_pwauth: True

# add each entry to ~/.ssh/authorized_keys for the configured user or the
# first user defined in the user definition directive.
ssh_authorized_keys:
  - ssh-rsa <PRIVATE KEY>
```

Once created the two files can be archived in the **.iso** format on Ubuntu as follows: 

```bash
genisoimage  -output seed.iso -volid cidata -joliet -rock user-data meta-data
```


## Local setup

### Windows setup

```bash

cd /path/Oracle/VirtualBox/sdk/install

python vboxapisetup.py install

git clone https://github.com/mjdorma/pyvbox

cd pyvbox 

python setup.py install

pip install pywin32

```

### Ubuntu setup

1. Install VirtualBox :  https://www.virtualbox.org/wiki/Downloads (Tested with vbox 5.2.12 and SDK 5.2.10)

2. [Download SDK](http://download.virtualbox.org/virtualbox/5.2.10/)

```bash

export VBOX_INSTALL_PATH=/usr/lib/virtualbox
export VBOX_SDK_PATH=/usr/lib/virtualbox/sdk
export PYTHONPATH=/usr/lib/virtualbox/sdk/bindings/xpcom/python

python -E vboxapisetup.py install

pip install pyvbox

```

### Run

```bash
python -m run --register-adapter <EPM_IP> <ADAPTER_IP>
```

## Docker setup

```yaml
docker build -t epm-adapter-vbox . 
docker run -p 50054:50054 --privileged -v /dev/:/dev/ epm-adapter-vbox
```
## Windows setup

```bash

cd /path/Oracle/VirtualBox/sdk/install

python vboxapisetup.py install

git clone https://github.com/mjdorma/pyvbox

cd pyvbox 

python setup.py install

pip install pywin32

```

## Ubuntu setup

1. Install VirtualBox :  https://www.virtualbox.org/wiki/Downloads (Tested with vbox 5.2.12 and SDK 5.2.10)

2. [Download SDK](http://download.virtualbox.org/virtualbox/5.2.10/)

```bash

export VBOX_INSTALL_PATH=/usr/lib/virtualbox
export VBOX_SDK_PATH=/usr/lib/virtualbox/sdk
export PYTHONPATH=/usr/lib/virtualbox/sdk/bindings/xpcom/python

python -E vboxapisetup.py install

pip install pyvbox

```

## Examples

https://gist.github.com/mjdorma
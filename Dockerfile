FROM python:3.5.2

RUN apt-get update && apt-get install -y build-essential autoconf libtool unzip software-properties-common

RUN pip install grpcio grpcio-tools pyyaml

RUN  add-apt-repository "deb http://download.virtualbox.org/virtualbox/debian `lsb_release -cs` contrib" && \
wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | apt-key add - &&\
wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | apt-key add - &&\
apt-get update && apt-get install -y virtualbox-5.2


RUN wget http://download.virtualbox.org/virtualbox/5.2.10/VirtualBoxSDK-5.2.10-122088.zip && unzip VirtualBoxSDK-5.2.10-122088.zip

RUN cd sdk/installer && export VBOX_INSTALL_PATH=/usr/lib/virtualbox && export VBOX_SDK_PATH=/usr/lib/virtualbox/sdk && export PYTHONPATH=/usr/lib/virtualbox/sdk/bindings/xpcom/python && python -E vboxapisetup.py install

RUN pip install pyvbox

ADD . virtualbox-adapter

WORKDIR virtualbox-adapter

ENTRYPOINT python run.py
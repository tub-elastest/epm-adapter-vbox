import paramiko
import tempfile
import shelve

class SSHExecutor():
    def __init__(self,
                 vm_name,
                 port):
        self.port = port
        self.vm_name = vm_name

    def _get_client(self):
        temp = tempfile.NamedTemporaryFile(delete=True)
        username, password, passphrase = self._get_auth_credentials()
        key, keypath = self._get_key_from_db()
        path = keypath
        if key is not None:
            temp.write(key)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if path is not None:
            client.connect("localhost", port=self.port, username=username, password=password, key_filename=path, passphrase=passphrase)
        else:
            client.connect("localhost", port=self.port, username=username, password=password)
        temp.close()
        return client

    def execute_command(self, command):

        client = self._get_client()
        stdin, stdout, stderr = client.exec_command(command)
        output = ""
        for line in stdout:
            output += ' ' + line.strip('\n') + " "
        client.close()
        return output

    def download_file_from_container(self, path):
        f = tempfile.NamedTemporaryFile()

        client = self._get_client()
        sftp = client.open_sftp()
        sftp.getfo(path, f)
        sftp.close()
        client.close()
        f.seek(0)

        output = f.read()
        f.close()

        return output

    def upload_file(self, path, bytes):
        f = tempfile.NamedTemporaryFile()
        f.write(bytes)
        f.seek(0)

        client = self._get_client()
        sftp = client.open_sftp()
        sftp.putfo(f, remotepath=path)
        sftp.close()
        client.close()
        f.close()

    def upload_file_from_path(self, hostPath, remotePath):
        client = self._get_client()
        sftp = client.open_sftp()
        sftp.put(hostPath, remotePath)
        sftp.close()
        client.close()

    def _get_key_from_db(self):
        db = shelve.open('auths.db')

        key = None
        keypath = None

        if self.vm_name + "_key" in db:
            key = db[self.vm_name + "_key"]
        if self.vm_name + "_key" in db:
            keypath = db[self.vm_name + "_key"]
        db.close()

        return key, keypath

    def _get_auth_credentials(self):
        db = shelve.open('auths.db')

        username = ""
        password = ""
        passphrase = ""

        cred_key = self.vm_name + "_credentials"
        if cred_key in db:
            auth = db[cred_key]

            if "username" in auth:
                username = auth["username"]
            if "password" in auth:
                password = auth["password"]
            if "passphrase" in auth:
                passphrase = auth["passphrase"]

        return username, password, passphrase
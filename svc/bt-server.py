from dataclasses import dataclass
from subprocess import Popen, PIPE
from time import sleep
from multiprocessing import Process
from sys import argv, stderr

class MacAddress:

    _str_val: str = ""
    _parsed_val: int = 0

    def __init__(self, value: str):
        self._str_val = value
        components = self._str_val.split(":")
        # 17 is 2 * 6 + 5 (aa:bb:cc:dd:ee:ff)
        if len(value) != 17 or len(components) != 6:
            raise ValueError("malformed data")
        res = 0
        for component in components:
            val = int(component, 0x10)
            res = (res << 8) | val

        self._parsed_val = res

    def __hash__(self):
        return self._parsed_val

    def __repr__(self):
        return self._str_val


@dataclass
class Device:
    name: str = ""
    mac_address: str = ""

    def parse(line: str):
        components = line.strip().split(" ")
        if len(components) != 3 or components[0] != "Device":
            return None

        try:
            addr = MacAddress(components[1])
        except ValueError:
            return None

        return Device(name=components[2], mac_address=addr)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.mac_address)

def list_clients() -> set[Device]:
    # $ bluetoothctl devices connected
    # Device AA:BB:CC:DD:EE:FF MY-DEVICE-NAME
    cmd = "bluetoothctl devices Connected".strip().split()
    # cmd = "bluetoothctl devices".strip().split()
    proc = Popen(cmd, stdout=PIPE)

    out, err = proc.communicate()

    res = set()

    lines = out.decode('utf-8').split("\n")
    for line in lines:
        dev = Device.parse(line)
        if dev is None:
            continue
        res.add(dev)

    return res

def send_file(client: Device, file: str):
    print(f"sending to {client}")
    cmd = f"bt-obex -p {client.mac_address} {file}".strip().split()
    proc = Popen(cmd)

    return proc.wait()


def main(file: str):
    current_clients = set()

    while True:
        print("fetching new clients")
        clients = list_clients()
        new_clients = clients - current_clients
        current_clients.clear()
        current_clients.update(clients)
        procs = []
        for client in new_clients:
            procs.append(Process(target=send_file, args=(client, file)))
            procs[-1].start()

        for proc in procs:
            proc.join()

        if len(new_clients) == 0:
            print("Waiting ...")
            sleep(10)

if __name__ == "__main__":

    if len(argv) != 2:
        print("Usage: bt-server <file>", file=stderr)
        exit(1)

    file = argv[1]

    print("Starting serving file", file)
    main(file)

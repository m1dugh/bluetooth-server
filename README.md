## Installing

The following files must be installed

`svc/bt-server.service` as a service file.
`svc/bt-server-init` in the path of the service file
`svc/bt-server.py` in `/opt/bt-server/server.py`
`svc/bt-agent.service` as a service file.

Once done, the service must be enabled.

Some packages must be installed for the program to work.

- `bt-obex` through `bluez-tools`

## Troubleshot

The following packages must be reinstalled in case the bluetooth is not
working properly

```
apt reinstall -y bluez bluez-firmware pi-bluetooth
```

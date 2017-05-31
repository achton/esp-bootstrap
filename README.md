# esp-bootstrap

Bootstrap files for an ESP8266 running MicroPython

### Features

##### Automatic execution of 'user' app:
- Automatically calls `app.main()` on boot. 
- Application you create for running on the ESP8266 should be placed in a file `app.py` on the device


##### Updater service:
- ESP8266 will listen for updates to the 'userspace' application, `app.py`, and when one is received it will write the new application (currently written to device as `app.py`) and automatically run it. 
- Updates can be sent to the device, over a TCP connection, using the [esp-updater project](https://github.com/craftyguy/esp-updater)
  - If the esp-updater project is not used, updates should be sent to the device in the form `<32byte sha256><data>`, to the port specified in `main.py`. The first 32 bytes of the data received is presumed to be the sha256 checksum of the following data. If this checksum fails, no updates are applied.
- The old application (`app.py`), if one exists, is backed up on the device. At some point I'll add a way to restore the backup.
- **NOTE**: This is ***NOT*** secure. The app file is checksummed, but there is ***NO*** encryption or authentication. Only use this project on a secure & trusted network.


##### Wifi Connect:
- Will automatically connect to a configured Wifi network on boot
- Credentials separately in secrets.py and loaded by boot.py. See Installation below for details


### Installation

Prerequisites:
- You need an ESP8266 device. This has been tested on the Wemos D1 Mini & Adafruit Huzzah.
- The ESP8266 must be running MicroPython. 

Copy `boot.py` and `main.py` to the device's flash. I recommend using [mpfshell](https://github.com/wendlers/mpfshell) to do this.

Create a `secrets.py` file in the following format, and copy to the device's flash:
```
WIFI_SSID = "<put SSID here>"
WIFI_PASSPHRASE = "<put super secret passphrase here>"
```

Place your application file, named as `app.py`, on the device's flash. This application must implement a `main()` method.

Upon first boot, if `app.py` does not yet exist, the device will boot to repl. You can use the host-side `esp_updater.py` application ([found here](https://github.com/craftyguy/esp-updater)) to send updates to `app.py` to the ESP8266.

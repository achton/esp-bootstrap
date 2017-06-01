# Copyright(c) 2017 by craftyguy "Clayton Craft" <clayton@craftyguy.net>
# Distributed under GPLv3+ (see COPYING) WITHOUT ANY WARRANTY.

import config
import esp
import secrets

if config.SILENT:
    esp.osdebug(None)

def do_connect():
    import network
    s_if = network.WLAN(network.STA_IF)
    a_if = network.WLAN(network.AP_IF)
    if a_if.active():
        a_if.active(False)
    if not s_if.isconnected():
        s_if.active(True)
        s_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSPHRASE)
        while not s_if.isconnected():
            pass
    if not config.SILENT:
        print("Wifi connected: ", s_if.ifconfig())


do_connect()

import main

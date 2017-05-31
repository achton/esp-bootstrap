# Copyright(c) 2017 by craftyguy "Clayton Craft" <clayton@craftyguy.net>
# Distributed under GPLv3+ (see COPYING) WITHOUT ANY WARRANTY.

from micropython import alloc_emergency_exception_buf
from machine import reset
import os
import socket
import uhashlib

###### Constants ######
# This parameter allows setting a call back function for a listening socket
SO_REGISTER_HANDLER = const(20)
# chunk size (arbitrarily chosen) for reading from socket
CHUNK_SIZE = const(200)
# sha256 checksum is 32 bytes
CHECKSUM_SIZE = const(32)
LISTEN_PORT = const(1337)
APP_FILENAME = "app.py"
APP_BAK_FILENAME = "app.bak"
TMP_FILENAME = 'app.tmp'

alloc_emergency_exception_buf(100)


# Call back function for listening socket
def sock_cb(s):
    client, addr = s.accept()
    try:
        # read checksum from sender
        checksum_orig = client.read(CHECKSUM_SIZE)
        #print("Checksum received:")
        #print_hex(checksum_orig)
        with open(TMP_FILENAME, 'w') as f:
            chunk = client.read(CHUNK_SIZE)
            while len(chunk) > 0:
                f.write(chunk.decode())
                chunk = client.read(CHUNK_SIZE)
    except Exception as e:
        print("exception: {0}".format(e))
    finally:
        client.close()

    checksum = chksum_file(TMP_FILENAME)
    #print("Checksum:")
    #print_hex(checksum)
    if checksum != checksum_orig:
        print("Checksum: FAILED")
        print("User app NOT updated")
        return
    print("Checksum: OK")
    # Back up old application if it exists
    for f in os.listdir():
        if f == APP_FILENAME:
            os.rename(APP_FILENAME, APP_BAK_FILENAME)
    # "apply" backup and reset system
    os.rename(TMP_FILENAME, APP_FILENAME)
    reset()


# Calculate checksum of file using SHA256, return checksum as byte array
def chksum_file(f):
    hashr = uhashlib.sha256()
    with open(f, 'rb') as t:
        chunk = t.read(CHUNK_SIZE)
        while len(chunk) > 0:
            hashr.update(chunk)
            chunk = t.read(CHUNK_SIZE)
    return hashr.digest()


# Print byte array as string of hex characters
def print_hex(bytez):
    print(''.join('%02X' % b for b in bytez))


# Set up socket and listen for updates. Here a callback is
# specified to "listen in the background"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', LISTEN_PORT))
sock.listen(0)
sock.setsockopt(socket.SOL_SOCKET, SO_REGISTER_HANDLER, sock_cb)


# Try to call app.main() directly. This is how the 'main' application
# written to run on the esp8266 is executed.
try:
    import app
    app.main()
except Exception as e:
    print("Oops, app.py failed for some reason: {0}".format(e))

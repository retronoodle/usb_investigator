import usb.core
import usb.backend.libusb1
import os
import sys

print('PyUSB version:', usb.__version__)
print('Python executable:', sys.executable)
print('Current working directory:', os.getcwd())
print('libusb-1.0.dll present:', os.path.exists('libusb-1.0.dll'))

print('\nBackend test:')
try:
    backend = usb.backend.libusb1.get_backend()
    if backend:
        print('+ libusb1 backend available')
        print('Backend:', backend)
    else:
        print('- libusb1 backend NOT available')
except Exception as e:
    print('- libusb1 backend error:', e)

print('\nSearching for USB devices:')
try:
    dev = usb.core.find()
    if dev is None:
        print('No USB device found (this is normal if no devices are accessible)')
    else:
        print('Found USB device:', dev)
except Exception as e:
    print('Error finding USB devices:', e)
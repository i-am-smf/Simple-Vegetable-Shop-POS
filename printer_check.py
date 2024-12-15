import os
import re

def list_usb_devices():
    devices = []
    try:
        # Run `wmic` command to get USB devices
        result = os.popen("wmic path Win32_PnPEntity where \"PNPClass='Printer'\" get Caption,DeviceID").read()
        lines = result.strip().split("\n")
        
        # Parse output for Vendor ID and Product ID (if available)
        for line in lines[1:]:
            if line.strip():
                devices.append(line.strip())
    except Exception as e:
        print(f"Error: {e}")
    return devices

# List and print USB devices
usb_devices = list_usb_devices()
if usb_devices:
    print("Connected USB Printers:")
    for device in usb_devices:
        print(f"{device}")
else:
    print("No USB printers found.")

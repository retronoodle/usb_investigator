import sys
import os

# Add current directory to DLL search path for libusb-1.0.dll (Windows)
if os.name == 'nt' and hasattr(os, 'add_dll_directory'):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.add_dll_directory(current_dir)
    except OSError:
        pass  # Directory might already be in PATH

from usb_utils import enumerate_usb_devices

def print_main_menu(devices):
    print("\n=== USB Investigator Main Menu ===")
    if not devices:
        print("No USB devices found.")
    else:
        print("Connected USB Devices:")
        for idx, dev in enumerate(devices, 1):
            name = f"{dev['manufacturer'] or 'Unknown'} - {dev['product'] or 'Unknown Product'}"
            print(f"  {idx}. {name} (VID: {dev['vendor_id']}, PID: {dev['product_id']})")
    print("\nOptions:")
    print("  [number] - Select device")
    print("  r - Refresh device list")
    print("  q - Quit")

def print_device_menu(dev):
    print("\n=== Device Interface Menu ===")
    print(f"Manufacturer: {dev['manufacturer']}")
    print(f"Product: {dev['product']}")
    print(f"Serial Number: {dev['serial_number']}")
    print(f"Vendor ID: {dev['vendor_id']}")
    print(f"Product ID: {dev['product_id']}")
    print("\nCapabilities: (placeholder)")
    print("- Communication methods will be listed here in Phase 4")
    print("\nOptions:")
    print("  b - Back to main menu")
    print("  q - Quit")

def device_interface_menu(dev):
    while True:
        print_device_menu(dev)
        choice = input("\nEnter your choice: ").strip().lower()
        if choice == 'b':
            return  # Go back to main menu
        elif choice == 'q':
            print("Exiting USB Investigator. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid input. Please try again.")

def main():
    while True:
        devices = enumerate_usb_devices()
        print_main_menu(devices)
        choice = input("\nEnter your choice: ").strip().lower()
        if choice == 'q':
            print("Exiting USB Investigator. Goodbye!")
            sys.exit(0)
        elif choice == 'r':
            continue  # Refresh device list
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(devices):
                device_interface_menu(devices[idx])
            else:
                print("Invalid device number. Please try again.")
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main() 
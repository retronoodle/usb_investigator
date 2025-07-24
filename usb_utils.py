import usb.core
import usb.util
from db import add_device


def enumerate_usb_devices():
    """
    Enumerate all connected USB devices.
    Returns a list of dicts with vendor_id, product_id, manufacturer, product, and serial_number.
    """
    devices = []
    try:
        for dev in usb.core.find(find_all=True):
            try:
                manufacturer = usb.util.get_string(dev, dev.iManufacturer) if dev.iManufacturer else None
            except Exception:
                manufacturer = None
            try:
                product = usb.util.get_string(dev, dev.iProduct) if dev.iProduct else None
            except Exception:
                product = None
            try:
                serial_number = usb.util.get_string(dev, dev.iSerialNumber) if dev.iSerialNumber else None
            except Exception:
                serial_number = None
            
            devices.append({
                'vendor_id': hex(dev.idVendor),
                'product_id': hex(dev.idProduct),
                'manufacturer': manufacturer,
                'product': product,
                'serial_number': serial_number
            })
    except usb.core.NoBackendError:
        print("Error: No USB backend available. Please install libusb.")
    except usb.core.USBError as e:
        print(f"USB Error: {e}. Try running as administrator.")
    except Exception as e:
        print(f"Unexpected error enumerating USB devices: {e}")
    return devices


def get_unique_device_key(device):
    """
    Generate a unique key for a device based on vendor_id, product_id, and serial_number.
    """
    return f"{device['vendor_id']}:{device['product_id']}:{device.get('serial_number') or 'no_serial'}"

def store_usb_devices_in_db():
    """
    Enumerate USB devices and store them in the database, avoiding duplicates.
    """
    from db import get_all_devices
    
    devices = enumerate_usb_devices()
    if not devices:
        print("No USB devices found or unable to access USB devices.")
        return
    
    # Get existing devices to avoid duplicates
    existing_devices = get_all_devices()
    existing_keys = set()
    for existing in existing_devices:
        key = f"{existing[4]}:{existing[5]}:{existing[3] or 'no_serial'}"
        existing_keys.add(key)
    
    new_devices_count = 0
    for dev in devices:
        device_key = get_unique_device_key(dev)
        if device_key not in existing_keys:
            add_device(
                dev.get('manufacturer'),
                dev.get('product'),
                dev.get('serial_number'),
                dev.get('vendor_id'),
                dev.get('product_id')
            )
            new_devices_count += 1
    
    print(f"Found {len(devices)} USB devices, added {new_devices_count} new devices to database.")


def monitor_usb_events():
    """
    Monitor USB device connection/disconnection events and update the database.
    """
    try:
        from usb_monitor import USBMonitor
    except ImportError:
        print("usb-monitor is not installed. Please install it to use event monitoring.")
        return

    def on_event(event):
        print(f"USB event: {event}")
        store_usb_devices_in_db()

    monitor = USBMonitor()
    monitor.set_event_callback(on_event)
    print("Monitoring USB events. Press Ctrl+C to stop.")
    monitor.run() 
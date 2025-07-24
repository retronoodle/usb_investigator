#!/usr/bin/env python3
"""
Test script to verify Phase 1 and Phase 2 implementation.
"""

from db import init_db, get_all_devices
from usb_utils import enumerate_usb_devices, store_usb_devices_in_db

def test_database():
    """Test database initialization and basic operations."""
    print("Testing database initialization...")
    try:
        init_db()
        print("[OK] Database initialized successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Database initialization failed: {e}")
        return False

def test_usb_enumeration():
    """Test USB device enumeration."""
    print("Testing USB device enumeration...")
    try:
        devices = enumerate_usb_devices()
        print(f"[OK] USB enumeration successful, found {len(devices)} devices")
        
        # Display found devices
        if devices:
            print("Found devices:")
            for i, dev in enumerate(devices):
                print(f"  {i+1}. {dev['manufacturer'] or 'Unknown'} - {dev['product'] or 'Unknown Product'}")
                print(f"     VID: {dev['vendor_id']}, PID: {dev['product_id']}")
                if dev['serial_number']:
                    print(f"     Serial: {dev['serial_number']}")
        else:
            print("  No USB devices found or unable to access USB devices")
        return True
    except Exception as e:
        print(f"[FAIL] USB enumeration failed: {e}")
        return False

def test_database_storage():
    """Test storing USB devices in database."""
    print("Testing database storage...")
    try:
        store_usb_devices_in_db()
        
        # Check what's in the database
        devices = get_all_devices()
        print(f"[OK] Database storage successful, {len(devices)} devices in database")
        
        if devices:
            print("Devices in database:")
            for dev in devices:
                print(f"  ID: {dev[0]}, {dev[1] or 'Unknown'} - {dev[2] or 'Unknown Product'}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Database storage failed: {e}")
        return False

def main():
    """Run all tests."""
    print("USB Investigator - Phase 1 & 2 Implementation Test")
    print("=" * 50)
    
    tests = [
        test_database,
        test_usb_enumeration,
        test_database_storage
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("[OK] All tests passed! Phase 1 & 2 implementation is working correctly.")
    else:
        print("[FAIL] Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
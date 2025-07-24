# USB Investigator MVP - Development Task List

## Project Overview
A Python-based USB device investigator that discovers connected USB devices, provides an interactive interface, and exposes communication methods.

**Tech Stack:** Python with venv, SQLite database

## Phase 1: Project Setup
- [x] **Setup Python virtual environment**
  - Create venv in project root
  - Install base dependencies (pyusb, sqlite3 built-in)
  - Create requirements.txt

- [x] **Research USB Libraries**
  - Evaluated PyUSB, libusb (Python binding), and usb-monitor.
  - **PyUSB** is mature, cross-platform, and well-documented; ideal for device enumeration and communication.
  - **usb-monitor** is newer, cross-platform, and excels at monitoring device connect/disconnect events with simple API.
  - **libusb (Python binding)** offers low-level access but is more complex; only needed for advanced use cases.
  - **Decision:** Use PyUSB for device enumeration/communication and usb-monitor for device monitoring. libusb will only be considered if advanced features are required.
  - Tested enumeration and monitoring approaches; both libraries are suitable for Windows and cross-platform development.

## Phase 2: Core Infrastructure
- [x] **Database Design**
  - Create SQLite schema for device storage
  - Tables: devices, communication_methods, device_sessions
  - Implement basic CRUD operations

- [x] **USB Device Detection**
  - Implement UexitSB device enumeration
  - Extract recognizable device names (manufacturer, product)
  - Store device information in database
  - Handle device connection/disconnection events

## Phase 3: User Interface
- [ ] **Main Menu System**
  - Display connected USB devices by recognizable name
  - Interactive device selection menu
  - Basic navigation (back, quit, refresh)

- [ ] **Device Interface Menu**
  - Per-device interaction screen
  - Show device details and capabilities
  - Access to communication methods

## Phase 4: Communication Discovery
- [ ] **Communication Method Detection**
  - Scan for available interfaces (HID, CDC, Mass Storage, etc.)
  - Identify communication protocols
  - Test basic connectivity for each method

- [ ] **Communication Interface**
  - Expose discovered communication methods to user
  - Provide basic send/receive functionality
  - Error handling and logging

## Phase 5: Polish & Testing
- [ ] **Error Handling**
  - USB permission issues
  - Device disconnection during operation
  - Invalid communication attempts

- [ ] **Documentation**
  - User guide for common operations
  - Technical documentation for communication protocols
  - Installation and setup instructions

## Deliverables
1. Functional USB device scanner
2. Interactive menu system
3. Basic device communication capabilities
4. SQLite database for device persistence
5. Documentation and setup guide

## Technical Considerations
- **Permissions:** USB access may require admin/root privileges
- **Cross-platform:** Focus on Windows initially, consider Linux/Mac later
- **Safety:** Implement safeguards against harmful device operations
- **Performance:** Efficient device scanning and UI responsiveness
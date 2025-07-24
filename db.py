import sqlite3
from typing import Any, List, Tuple, Optional

DB_NAME = 'usb_investigator.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Devices table
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manufacturer TEXT,
            product TEXT,
            serial_number TEXT,
            vendor_id TEXT,
            product_id TEXT,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Communication methods table
    c.execute('''
        CREATE TABLE IF NOT EXISTS communication_methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER,
            method_type TEXT,
            description TEXT,
            FOREIGN KEY(device_id) REFERENCES devices(id)
        )
    ''')
    # Device sessions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS device_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER,
            session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_end TIMESTAMP,
            notes TEXT,
            FOREIGN KEY(device_id) REFERENCES devices(id)
        )
    ''')
    conn.commit()
    conn.close()

# --- CRUD Stubs ---
# Devices

def add_device(manufacturer: str, product: str, serial_number: str, vendor_id: str, product_id: str) -> int:
    if not vendor_id or not product_id:
        raise ValueError("vendor_id and product_id are required")
    
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO devices (manufacturer, product, serial_number, vendor_id, product_id) VALUES (?, ?, ?, ?, ?)",
        (manufacturer, product, serial_number, vendor_id, product_id)
    )
    conn.commit()
    device_id = c.lastrowid
    conn.close()
    return device_id

def get_device(device_id: int) -> Optional[Tuple]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
    result = c.fetchone()
    conn.close()
    return result

def update_device(device_id: int, **kwargs) -> None:
    if not kwargs:
        return
    conn = get_connection()
    c = conn.cursor()
    fields = ', '.join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values())
    values.append(device_id)
    c.execute(f"UPDATE devices SET {fields} WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_device(device_id: int) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM devices WHERE id = ?", (device_id,))
    conn.commit()
    conn.close()

# Communication Methods

def add_communication_method(device_id: int, method_type: str, description: str) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO communication_methods (device_id, method_type, description) VALUES (?, ?, ?)",
        (device_id, method_type, description)
    )
    conn.commit()
    method_id = c.lastrowid
    conn.close()
    return method_id

def get_communication_methods(device_id: int) -> List[Tuple]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM communication_methods WHERE device_id = ?", (device_id,))
    results = c.fetchall()
    conn.close()
    return results

def update_communication_method(method_id: int, **kwargs) -> None:
    if not kwargs:
        return
    conn = get_connection()
    c = conn.cursor()
    fields = ', '.join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values())
    values.append(method_id)
    c.execute(f"UPDATE communication_methods SET {fields} WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_communication_method(method_id: int) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM communication_methods WHERE id = ?", (method_id,))
    conn.commit()
    conn.close()

# Device Sessions

def add_device_session(device_id: int, notes: str = "") -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO device_sessions (device_id, notes) VALUES (?, ?)",
        (device_id, notes)
    )
    conn.commit()
    session_id = c.lastrowid
    conn.close()
    return session_id

def end_device_session(session_id: int) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE device_sessions SET session_end = CURRENT_TIMESTAMP WHERE id = ?",
        (session_id,)
    )
    conn.commit()
    conn.close()

def get_device_sessions(device_id: int) -> List[Tuple]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM device_sessions WHERE device_id = ?", (device_id,))
    results = c.fetchall()
    conn.close()
    return results

def delete_device_session(session_id: int) -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM device_sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

def get_all_devices() -> List[Tuple]:
    """Get all devices from the database."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM devices")
    results = c.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    init_db() 
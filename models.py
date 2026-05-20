import sqlite3
from database import connect_db


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_id TEXT UNIQUE,
        sender TEXT,
        receiver TEXT,
        status TEXT,
        location TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipment_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_id TEXT,
        status TEXT,
        location TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # لو الداتابيز قديمة ومفيهاش updated_at
    cursor.execute("PRAGMA table_info(shipments)")
    columns = [column[1] for column in cursor.fetchall()]

    if "updated_at" not in columns:
        cursor.execute("ALTER TABLE shipments ADD COLUMN updated_at TEXT")

    conn.commit()
    conn.close()


def add_history(tracking_id, status, location):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO shipment_history (tracking_id, status, location)
    VALUES (?, ?, ?)
    """, (tracking_id, status, location))

    conn.commit()
    conn.close()


def add_shipment(tracking_id, sender, receiver, status, location):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO shipments
        (tracking_id, sender, receiver, status, location, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (tracking_id, sender, receiver, status, location))

        conn.commit()
        conn.close()

        add_history(tracking_id, status, location)
        return True

    except sqlite3.IntegrityError:
        conn.close()
        return False


def get_shipment(tracking_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM shipments
    WHERE tracking_id = ?
    """, (tracking_id,))

    shipment = cursor.fetchone()
    conn.close()

    return shipment


def update_shipment(tracking_id, status, location):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE shipments
    SET status = ?, location = ?, updated_at = CURRENT_TIMESTAMP
    WHERE tracking_id = ?
    """, (status, location, tracking_id))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    if updated:
        add_history(tracking_id, status, location)

    return updated


def delete_shipment(tracking_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM shipments
    WHERE tracking_id = ?
    """, (tracking_id,))

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    return deleted


def get_tracking_history(tracking_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT status, location, updated_at
    FROM shipment_history
    WHERE tracking_id = ?
    ORDER BY id ASC
    """, (tracking_id,))

    history = cursor.fetchall()
    conn.close()

    return history


def get_dashboard_counts():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM shipments")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS delivered FROM shipments WHERE status = 'Delivered'")
    delivered = cursor.fetchone()["delivered"]

    cursor.execute("SELECT COUNT(*) AS in_transit FROM shipments WHERE status = 'In Transit'")
    in_transit = cursor.fetchone()["in_transit"]

    cursor.execute("SELECT COUNT(*) AS pending FROM shipments WHERE status != 'Delivered'")
    pending = cursor.fetchone()["pending"]

    conn.close()

    return {
        "total": total,
        "delivered": delivered,
        "in_transit": in_transit,
        "pending": pending
    }
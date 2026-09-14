import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# 1. Update view to incorporate ADJUSTMENT (+ or -)
cursor.execute("DROP VIEW IF EXISTS view_current_stock;")
cursor.execute("""
    CREATE VIEW view_current_stock AS
    SELECT 
        i.item_id,
        i.name,
        i.unit_price,
        i.reorder_level,
        COALESCE(SUM(
            CASE 
                WHEN t.movement_type = 'IN' THEN t.quantity
                WHEN t.movement_type = 'OUT' THEN -t.quantity
                WHEN t.movement_type = 'ADJUSTMENT' THEN t.quantity
                ELSE 0 
            END
        ), 0) AS current_stock
    FROM items i
    LEFT JOIN transactions t ON i.item_id = t.item_id
    GROUP BY i.item_id;
""")
conn.commit()
conn.close()
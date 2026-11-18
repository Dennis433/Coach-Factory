from app import create_app, db
from sqlalchemy import text, inspect

app = create_app()

def migrate():
    with app.app_context():
        inspector = inspect(db.engine)

        # ── Order table columns ──
        order_columns = [col['name'] for col in inspector.get_columns('order')]
        order_cols = {
            'tx_hash': "VARCHAR(200) DEFAULT ''",
            'items': "TEXT DEFAULT ''",
            'full_name': "VARCHAR(120) DEFAULT ''",
            'phone': "VARCHAR(40) DEFAULT ''",
            'address': "TEXT DEFAULT ''",
            'city': "VARCHAR(100) DEFAULT ''",
            'state': "VARCHAR(100) DEFAULT ''",
            'zip_code': "VARCHAR(20) DEFAULT ''",
            'country': "VARCHAR(100) DEFAULT ''",
        }
        with db.engine.connect() as conn:
            for col, ddl in order_cols.items():
                if col not in order_columns:
                    conn.execute(text(f'ALTER TABLE "order" ADD COLUMN {col} {ddl}'))
                    conn.commit()
                    print(f'Added {col} column to order')

        # ── Product table columns ──
        product_columns = [col['name'] for col in inspector.get_columns('product')]
        with db.engine.connect() as conn:
            if 'images' not in product_columns:
                conn.execute(text("ALTER TABLE product ADD COLUMN images TEXT DEFAULT ''"))
                conn.commit()
                print('Added images column to product')

        print('Migration complete!')

migrate()

if __name__ == '__main__':
    app.run(debug=True)
from app import create_app, db
from app.models import User, Product, Order
from sqlalchemy import text, inspect

app = create_app()

def migrate():
    with app.app_context():
        inspector = inspect(db.engine)

        # ── Order table columns ──
        order_columns = [col['name'] for col in
                         inspector.get_columns('order')]

        with db.engine.connect() as conn:
            if 'tx_hash' not in order_columns:
                conn.execute(text(
                    'ALTER TABLE "order" ADD COLUMN '
                    'tx_hash VARCHAR(200) DEFAULT \'\''))
                conn.commit()
                print('Added tx_hash column')

            if 'items' not in order_columns:
                conn.execute(text(
                    'ALTER TABLE "order" ADD COLUMN '
                    'items TEXT DEFAULT \'\''))
                conn.commit()
                print('Added items column')

        # ── Product table columns ──
        product_columns = [col['name'] for col in
                           inspector.get_columns('product')]

        with db.engine.connect() as conn:
            if 'images' not in product_columns:
                conn.execute(text(
                    'ALTER TABLE product ADD COLUMN '
                    'images TEXT DEFAULT \'\''))
                conn.commit()
                print('Added images column')

        print('Migration complete!')

if __name__ == '__main__':
    migrate()
    app.run(debug=True)
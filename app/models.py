from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    images = db.Column(db.Text, default='')

    def get_images(self):
        if self.images:
            return self.images.split(',')
        return []

    def first_image(self):
        imgs = self.get_images()
        return imgs[0] if imgs else ''
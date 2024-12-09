from models import db
from app import app

if __name__ == "__main__":
    with app.app_context():
        try:
            print("Initializing the database...")
            db.drop_all()
            db.create_all()
            print("Database initialization complete!")
        except Exception as e:
            print(f"Error initializing the database: {e}")

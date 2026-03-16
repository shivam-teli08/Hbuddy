from src import create_app
from src.services.bootstrap_service import initialize_database


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        initialize_database()
        print("Database initialized successfully.")

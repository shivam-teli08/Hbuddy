import os

from src import create_app
from src.services.bootstrap_service import initialize_database


app = create_app()

with app.app_context():
    initialize_database()
    print("Database initialized successfully.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

import firebase_admin
from firebase_admin import credentials

def init_firebase():
    # In a real app, you would load serviceAccountKey.json
    # For local development without a key, you can initialize a mock app
    # Or expect the environment variable GOOGLE_APPLICATION_CREDENTIALS
    try:
        firebase_admin.get_app()
    except ValueError:
        # We will not initialize with credentials here to allow mock/dev testing easily.
        # In production, pass credentials.Certificate('path/to/serviceAccountKey.json')
        firebase_admin.initialize_app()

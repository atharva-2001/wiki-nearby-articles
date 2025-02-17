import logging
from wikinearbyarticles import app

logging.basicConfig(level=logging.INFO)

@app.before_request
def log_request_info():
    logging.info('Headers: %s', request.headers)
    logging.info('Body: %s', request.get_data())

def main() -> None:
    """Run the Flask application."""
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.run(debug=False)

if __name__ == "__main__":
    main()
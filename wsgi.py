import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from server import app
except ImportError as e:
    print(f"Error importing server: {e}")
    # Fallback
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return "Server import failed"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

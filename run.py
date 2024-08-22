import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.routes import app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
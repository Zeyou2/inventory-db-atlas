import sys
import os
from src.connect import Mongo_Manager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.routes import app
# from src.connect import Mongo_Manager

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # Mongo_Manager("inventory").reset_inv()
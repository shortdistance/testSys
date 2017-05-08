# -*- coding: utf-8 -*-

from scripts import create_app
from scripts.config import HOST, PORT

# import sys
# import os.path

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

app = create_app()

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True)

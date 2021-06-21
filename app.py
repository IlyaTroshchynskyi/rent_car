# -*- coding: utf-8 -*-
""" The entry point WSGI application object.
"""

from rentcars import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

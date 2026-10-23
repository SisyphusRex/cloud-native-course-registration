# Outside sources
## Flask api structure
https://www.datascienceblog.net/post/programming/flask-api-development/
flask_app/
│   requirements.txt 
│   app.ini
│   wsgi.py
│
└───src/
│   │   app.py
│   │   api_spec.py
│   │
│   │───blueprints/
│       │   blueprint_x.py
│       │   blueprint_y.py
│       │   swagger.py
│
└───test/
    │   conftest.py
    │   test_endpoints.py
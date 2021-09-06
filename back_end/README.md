# Flask-Backend for Terrific-Tiger Chat

This folder contains the backend structure for the Terrific-Tiger Chat. <br>
The server runs on Flask, a microframework based on Python.<br>
+ [Flask Documentation](http://flask.pocoo.org/docs/1.0/)

![Python Flask Logo](http://flask.pocoo.org/static/logo/flask.png)

Furthermore, some extensions have been used: <br>
+ Flask-RESTPlus is an extension for Flask that adds support for quickly building REST APIs.
+ [Flask RestPlus Documentation](https://flask-restplus.readthedocs.io/en/stable/index.html)
+ Flask-Login provides user session management for Flask.
+ [Flask-Login Documentation](https://flask-login.readthedocs.io/en/latest/)

### Docker Image
For creating the Docker Image, please run the above docker-compose.yml file. <br>
After the Images have been created, run them as the following in a container: <br>

```shell
    docker-compose build
    docker run -p 5000:5000 terrific-tiger_back-end
```

Finally open http://0.0.0.0:5000/api/ in your browser. <br>

(More is yet to come)


FROM python:3

WORKDIR /back_end
COPY . back_end

RUN pip install flask
RUN pip install flask_login
RUN pip install flask_pymongo
RUN pip install flask_cors
RUN pip install flask_bcrypt
RUN pip install flask_jwt_extended
RUN pip install flask-restplus

EXPOSE 5000

CMD ["python", "back_end/app.py"]

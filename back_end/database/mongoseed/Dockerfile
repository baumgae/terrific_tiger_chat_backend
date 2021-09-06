FROM mongo

COPY /data/chat.json test/chat.json
COPY /data/user.json test/user.json

CMD use terrific_tiger_db
CMD mongoimport --host 127.0.0.1 --port 27017 --db terrific_tiger_db --collection chat --type json --file test/chat.json --jsonArray
CMD mongoimport --host 127.0.0.1 --port 27017 --db terrific_tiger_db --collection user --type json --file test/user.json --jsonArray
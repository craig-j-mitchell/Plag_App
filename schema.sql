DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastname TEXT NOT NULL ,
    firstname TEXT NOT NULL,
    currentgrade TEXT NOT NULL
);
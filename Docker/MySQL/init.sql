
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    uid varchar(255) PRIMARY KEY,
    user_name varchar(255) UNIQUE NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL
);

CREATE TABLE teamLists (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    year varchar(255) NOT NULL,
    season varchar(255) NOT NULL,
    team varchar(255) NOT NULL,
    github varchar(255) NOT NULL
);

CREATE TABLE channels (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    name varchar(255) UNIQUE NOT NULL,
    abstract varchar(255)
);

CREATE TABLE messages (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    cid integer REFERENCES channels(id) ON DELETE CASCADE,
    message text,
    created_at timestamp not null default current_timestamp
);

INSERT INTO users(uid, user_name, email, password)VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','テスト','test@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578');
INSERT INTO channels(id, uid, name, abstract)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8','ぼっち部屋','テストさんの孤独な部屋です');
INSERT INTO messages(id, uid, cid, message)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', '誰かかまってください、、');
INSERT INTO teamLists(id, uid, year, season, team, github)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '2023', '春', 'A', 'https://github.com/RT-F-HACKATHON/teamF_app');

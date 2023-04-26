CREATE DATABASE IF NOT EXISTS toxicitycalc;
USE toxicitycalc;

DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE if EXISTS ScoreHistory CASCADE

CREATE TABLE users (
    username VARCHAR(50) UNIQUE NOT NULL,
    results VARCHAR(200) NOT NULL
);
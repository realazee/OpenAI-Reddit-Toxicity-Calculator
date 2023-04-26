CREATE DATABASE IF NOT EXISTS toxicitycalc;
USE toxicitycalc;

DROP TABLE IF EXISTS searchedUsers CASCADE;

CREATE TABLE searchedUsers (
    user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    results VARCHAR(200) NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id)
);
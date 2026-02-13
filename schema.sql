CREATE DATABASE IF NOT EXISTS stock_app;

USE stock_app;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE portfolio (
   id INT AUTO_INCREMENT PRIMARY KEY,
   user_id INT,
   symbol VARCHAR(50),
   quantity INT,
   price FLOAT,
   FOREIGN KEY (user_id) REFERENCES users(id)
 );
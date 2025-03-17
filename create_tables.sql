-- Drop existing tables if they exist
DROP TABLE IF EXISTS blogs;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS users;

-- Create Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    created_date DATETIME NULL
);

-- Create Contacts table
CREATE TABLE contacts (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50) NOT NULL,
    phone_num VARCHAR(12) NOT NULL,
    type VARCHAR(30) NOT NULL,
    message VARCHAR(120) NOT NULL,
    created_date DATETIME NULL
);

-- Create Blogs table
CREATE TABLE blogs (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    slug VARCHAR(30) NOT NULL,
    type VARCHAR(30) NOT NULL,
    content VARCHAR(400) NOT NULL,
    img_file VARCHAR(50) NOT NULL,
    img_binary LONGBLOB NOT NULL,  -- Store images in binary format
    created_date DATETIME NULL,
    modified_date DATETIME NULL
);

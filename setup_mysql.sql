-- Connect to MySQL server as root
-- (assuming you have the necessary permissions)

-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS store_mgmt_db;

-- Create the user if it does not exist
CREATE USER IF NOT EXISTS 'store_mgmt_user'@'localhost' IDENTIFIED BY 'store_mgmt_pwd';

-- Grant all privileges on store_mgmt_db to store_mgmt_user
GRANT ALL PRIVILEGES ON store_mgmt_db.* TO 'store_mgmt_user'@'localhost';

-- Grant SELECT privilege on performance_schema to store_mgmt_user
GRANT SELECT ON performance_schema.* TO 'store_mgmt_user'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

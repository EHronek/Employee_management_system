-- script prepares a mysql server for the project

CREATE DATABASE IF NOT EXISTS ems_dev_db;
CREATE USER IF NOT EXISTS "ems_dev"@"localhost" IDENTIFIED BY " ems_dev_pwd";
GRANT ALL PRIVILEGES ON ems_dev_db.* TO "ems_dev"@"localhost";
GRANT SELECT ON perfomance_schema.* TO "ems_dev"@"localhost";

FLUSH PRIVILEGES;
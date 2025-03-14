-- Prepares a mysql server for the project

create database if not exists ems_test_db;
create user if not exists "ems_test"@"localhost" identified by "ems_test_pwd";
grant all PRIVILEGES ON ems_test_db.* TO "ems_test"@"localhost";
grant select on perfomance_schema.* TO "ems_test"@"localhost";
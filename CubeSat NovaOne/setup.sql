CREATE DATABASE cubesat_db;
CREATE USER cubesat_user WITH PASSWORD 'cubesat_password';
GRANT ALL PRIVILEGES ON DATABASE cubesat_db TO cubesat_user;

\c cubesat_db;

GRANT ALL ON SCHEMA public TO cubesat_user;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

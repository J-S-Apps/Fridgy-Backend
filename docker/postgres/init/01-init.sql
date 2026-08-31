\getenv app_user FRIDGY_DB_USER
\getenv app_pass FRIDGY_DB_PASSWORD
\getenv app_db FRIDGY_DB_NAME

CREATE USER :"app_user" WITH LOGIN PASSWORD :'app_pass';

CREATE DATABASE :"app_db" OWNER :"app_user";
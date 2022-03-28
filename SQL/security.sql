CREATE TABLE users
(
    id serial PRIMARY KEY,
    username varchar(100) UNIQUE,
    password_hash varchar(128),
    apiuser boolean DEFAULT TRUE,
    admin boolean DEFAULT FALSE,
    edit_auth boolean DEFAULT FALSE
);
INSERT INTO users(username,password_hash,admin,edit_auth)
VALUES
    ('admin','$6$rounds=656000$8ctA8pEZ7rX.q4Uy$972h1pLRHaHaiM6.EC3ro3N4zL84tPIdkX.FnqbLoT3P.4/H5eGtlpBmefUWPPga3Whl4ESyW9oGUL2v/CCFS/',false,true,false);
-- Note: it inserts a user with username 'admin' and password 'admin', with admin role but no edit role (meaning it can manage the users and administration but cannot put new data in the database (concerning taxonomy references and statuses)

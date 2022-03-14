colSpList API
================

-   [1 Content](#content)
-   [2 Deploying the API with Heroku](#deploying-the-api-with-heroku)
    -   [2.1 Creation of the local
        database](#creation-of-the-local-database)
    -   [2.2 Deployment in heroku](#deployment-in-heroku)
    -   [2.3 Local deployment for development and
        test](#local-deployment-for-development-and-test)

------------------------------------------------------------------------

The colSpList API (<https://colsplist.herokuapp.com>) provides utilities
to determine whether species are alien/invasive, endemic and/or
threatened on the Colombian territory.

The objective of this repository is to present both the API and its use
(mostly example code in R and python).

# 1 Content

In the folder [SQL](./SQL), you will find the SQL code for initializing
the database of the API

In the folder [API](./API), all the functions used by the API, and the
definitions of classes, endpoints and routes for the API to work.

In the folder usage, you’ll find various folder containing examples on
how to use the API The folder [UsingPost](./usage/UsingPost) contains
examples concerning the Post endpoints and the API. More specifically,
you will find the scripts that I used to feed the database with dataset
concerning [exotic](./usage/UsingPost/insertExotData.md),
[threatened](./usage/UsingPost/insertThreatData.md), and
[endemic](./usage/UsingPost/insertEndemData.md)

# 2 Deploying the API with Heroku

In order to deploy the API locally and/or remotely, you will need:

1.  to install heroku. (See
    <https://devcenter.heroku.com/articles/getting-started-with-python#set-up>).
2.  git
3.  an heroku account
4.  python3
5.  postgreSQL
6.  psql

The file [runtime.txt](./API/runtime.txt) contains the python version
used for development and deployment of the API

Then, clone the repository:

    git clone https://github.com/marbotte/colSpList
    cd colSpList

## 2.1 Creation of the local database

Whether you want to deploy the API locally or on heroku, the best
solution for the database is to create one locally, and then to push it
on heroku or use it locally (in particular, there is no other simple way
to implement a base encoding of the postgres database in Unicode).

Therefore we need to create a local database called here “sp_list”.

In bash it may be done with:

``` bash
createdb sp_list
```

Create a
[pgpass](https://www.postgresql.org/docs/9.3/libpq-pgpass.html), in
order not to worry about your credentials to connect to the local
database

Then, the initialization of the database is done with:

``` bash
psql sp_list -f SQL/init.sql
```

## 2.2 Deployment in heroku

You first need to login to heroku from the CLI:

``` bash
heroku login
```

Then create the application in heroku:

``` bash
heroku create
```

Push the application, using git, to the heroku system (Note that we push
only the API folder, the rest of the repository containing files which
are unnecessary for the API and might cause errors)

``` bash
git subtree push --prefix API heroku master
```

Create the heroku database:

``` bash
heroku addons:create heroku-postgresql:hobby-dev
```

Push the local database to heroku

``` bash
heroku pg:push sp_list DATABASE_URL
```

Finally, deploy the web-based heroku system:

``` bash
heroku ps:scale web=1
heroku open
```

More explanation
[here](https://devcenter.heroku.com/articles/getting-started-with-python)

## 2.3 Local deployment for development and test

First we will manage the python environment necessary to run the API.
You do not have to use a particular python environment, but it may be
helpful if you have other python projects which may present different
requirements:

``` bash
python3 -m colSpList_env venv
source colSpList_env/bin activate
```

Install all the dependencies required by the API

``` bash
pip3 install -r API/requirements.txt
```

Export the database URL

``` bash
export DATABASE_URL=postgres://localhost/sp_list
```

Run the API locally:

``` bash
heroku local
```

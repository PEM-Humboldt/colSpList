# colSpList API


The colSpList API (<https://colsplist.herokuapp.com>) provides utilities to determine whether species are alien/invasive, endemic and/or threatened on the Colombian territory.

The objective of this repository is to present both the API and its use (mostly example code in R and python).

# Content
In the folder [SQL](./SQL), you will find the SQL code for initializing the database of the API

In the folder [API](./API), all the functions used by the API, and the definitions of classes, endpoints and routes for the API to work.

In the folder usage, you'll find various folder containing examples on how to use the API
The folder [UsingPost](./usage/UsingPost) contains examples concerning the Post endpoints and the API. More specifically, you will find the scripts that I used to feed the database with dataset concerning [exotic](./usage/UsingPost/insertExotData.md), [threatened](./usage/UsingPost/insertThreatData.md), and [endemic](./usage/UsingPost/insertEndemData.md)
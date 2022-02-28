Administration of the database from the API
================

# 1 Backup

## 1.1 Basic backup of the local database

When the API is used locally, the backup of the local database (named
sp_list) may be done by the following command in bash:

``` bash
pg_dump -Fc --no-acl --no-owner sp_list > ../../db_dumps/sp_list_local`date +%Y_%m_%d_%H%M%S%N`
```

## 1.2 Backup through Heroku

Heroku proposes a service for generating backups, which are stored in
Heroku servers

It’s done through the command:

``` bash
heroku pg:backups:capture --app colsplist
```

With the basic plan, heroku will retain 2 backups, which means that it
will expire the oldest backup to create a new one\`

In order to create regular backups on heroku servers we may use as well:

``` bash
heroku pg:backups:schedule DATABASE_URL --at "02:00 America/Bogota" --app colsplist
```

Now, in order to download the backup, we need first to know which backup
we are interested in:

``` bash
heroku pg:backups --app colsplist
```

    ## === Backups
    ## ID    Created at                 Status                               Size      Database
    ## ────  ─────────────────────────  ───────────────────────────────────  ────────  ────────
    ## a005  2022-02-28 07:03:47 +0000  Completed 2022-02-28 07:03:51 +0000  139.99KB  DATABASE
    ## a004  2022-02-27 07:03:15 +0000  Completed 2022-02-27 07:03:16 +0000  139.99KB  DATABASE
    ## a003  2022-02-26 07:04:17 +0000  Completed 2022-02-26 07:04:23 +0000  139.99KB  DATABASE
    ## a002  2022-02-25 07:02:07 +0000  Completed 2022-02-25 07:02:09 +0000  139.99KB  DATABASE
    ## b001  2022-02-24 19:15:29 +0000  Completed 2022-02-24 19:15:31 +0000  139.99KB  DATABASE
    ## 
    ## === Restores
    ## No restores found. Use heroku pg:backups:restore to restore a backup
    ## 
    ## === Copies
    ## No copies found. Use heroku pg:copy to copy a database to another

Using the ID we are interested in, we can now query an url for the
physical file on a server, and then download it as a file

``` bash
URL_DB=`heroku pg:backups:url a005 --app colsplist`
echo $URL_DB
wget -O "../../db_dumps/sp_list_heroku`date +%Y_%m_%d_%H%M%S%N`.dump" $URL_DB
```

    ## https://xfrtu.s3.amazonaws.com/f9f361b1-7d89-431a-9d54-47c7c1c3c06e/2022-02-28T07%3A03%3A47Z/6ab7f2f3-ae60-4b35-b992-99824c4b5d3d?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQKF7VQWOEOUALNOS%2F20220228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220228T225133Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=86d7220000052a8b64515f102add782b93360161d0582cb92a398f50e432748c
    ## --2022-02-28 17:51:33--  https://xfrtu.s3.amazonaws.com/f9f361b1-7d89-431a-9d54-47c7c1c3c06e/2022-02-28T07%3A03%3A47Z/6ab7f2f3-ae60-4b35-b992-99824c4b5d3d?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQKF7VQWOEOUALNOS%2F20220228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220228T225133Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=86d7220000052a8b64515f102add782b93360161d0582cb92a398f50e432748c
    ## Resolving xfrtu.s3.amazonaws.com (xfrtu.s3.amazonaws.com)... 52.217.12.164
    ## Connecting to xfrtu.s3.amazonaws.com (xfrtu.s3.amazonaws.com)|52.217.12.164|:443... connected.
    ## HTTP request sent, awaiting response... 200 OK
    ## Length: 143353 (140K) [binary/octet-stream]
    ## Saving to: ‘../../db_dumps/sp_list_heroku2022_02_28_175133200506720.dump’
    ## 
    ##      0K .......... .......... .......... .......... .......... 35%  299K 0s
    ##     50K .......... .......... .......... .......... .......... 71%  593K 0s
    ##    100K .......... .......... .......... .........            100% 73,7M=0,3s
    ## 
    ## 2022-02-28 17:51:33 (555 KB/s) - ‘../../db_dumps/sp_list_heroku2022_02_28_175133200506720.dump’ saved [143353/143353]

## 1.3 Using Cron to manage frequent backup

The most probable scenario is that we will store the database in another
service than heroku, in a server which will work under an Unix-based
system.

In order to schedule backup in this system, we might want to use the
Cron system.

In that case, the scheduling system will use a bash file, called
db_backup_sp_list.sh, and placed in the home folder:

    #! /bin/bash
    DATABASE_URL='//localhost/sp_list'
    directory_backup='~/db_backups'
    pg_dump -h $DATABASE_URL -d sp_list -Fc --no-acl --no-owner > "$directory_backup/sp_list`date+%Y_%m_%d_%H%M%S%N`"

In the cron file, we add the line:

    0   0   1   *   *   bash -x db_backup_sp_list.sh

This results in a monthly backup realized on the first of each month at
00:00

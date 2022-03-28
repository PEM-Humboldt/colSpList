#!/bin/bash
secret="$(dd if=/dev/urandom bs=3 count=12)"
heroku config:set SECRET_KEY=$secret

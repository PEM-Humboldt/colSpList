#!/bin/bash
parent_path="$(dirname "${BASH_SOURCE[0]}")"
source "$parent_path"/../colSpList_env/bin/activate
export DATABASE_URL=postgres://localhost/sp_list
secret="$(dd if=/dev/urandom bs=3 count=12)"
export SECRET_KEY=$secret

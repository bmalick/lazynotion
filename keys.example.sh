#!/bin/bash

account=$1
account_flag="sharowross"
[[ -n "$account" ]] && account_flag="$account"
echo "Using account: $account_flag"

if [ "$account_flag" = "sharowross" ]; then
    # sharowross account
    export NOTION_API_KEY="sharowross_notion_api_key"
    export NOTION_ACCOUNT_NAME=$account_flag
elif [ "$account_flag" = "bmalick" ]; then
    # bmalick account
    export NOTION_API_KEY="bmalick_notion_api_key"
    export DATABASES_PAGE="bmalick_database_root_page_id"
    export NOTION_ACCOUNT_NAME=$account_flag
else
    echo "$account is not available."
fi



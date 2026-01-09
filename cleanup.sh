#!/bin/bash

for name in $(ls .); do
    if [ -f "$name" ] && ! [[ "$name" =~ \.(py|pyw|png|md|sh)$ ]]; then
        rm -f "$name"
    elif [ -d "$name" ] && ! [[ "$name" =~ ^(src|ico)$ ]]; then
        rm -rf "$name"
    fi
done

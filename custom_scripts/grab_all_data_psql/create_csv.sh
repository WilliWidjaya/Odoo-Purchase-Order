#!/bin/bash

psql -d "$2" -c "\copy ($1) TO '$3' WITH CSV HEADER"

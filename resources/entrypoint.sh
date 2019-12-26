
#!/bin/bash

set -e

cd /usr/src/
>&2 echo "Running ./manage.py $@"
exec ./manage.py $@

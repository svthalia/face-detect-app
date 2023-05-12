> face-detect-app was a temporary website where Thalia's members could try out face detection as part of the lustrum. It is superseded now by the facedetection app in [concrexit](https://github.com/svthalia/concrexit).

# Deploying

1. Create an elastic beanstalk environment with a RDS instance running Postgres
2. Enable the environment for this git repository
3. Run `eb deploy`

Deploying a new Docker image is possible using:
`docker build -t <tag> -f Dockerbuildfile . && docker push <tag>`

Just make sure you replace all references in the configuration with the domain name you are using and the Docker image you want to use.

If you want to backup/restore your database use:
`pg_dump -h <host> -U <user> -f face-detect-dump.sql ebdb`
`psql -d ebdb -h <host> -U <user> -f face-detect-dump.sql`

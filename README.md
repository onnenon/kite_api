# Backend Things

In order to run the backend API/database for testing, ensure you have Docker and docker compose installed on your machine.

Then spin up an instance of the db and API server with:
`docker-compose up -d`

This will create a running API and database container, but will not start the API server itself. This is so that we can
view Stdout and see the debug output from the API server.

In order to run the API server, shell into the running API container with:
`docker-compose exec api bash`

Now, inside the API's command line, run the following command to start the API server:
`flask run --host=0.0.0.0`

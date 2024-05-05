To run, you need to:
- create two files with a private and a public key
  (certs/jwt-private.pem and certs/jwt-public.pem accordingly)
  ```
  mkdir certs
  cd certs
  echo > jwt-private.pem
  echo > jwt-public.pem
  cd ..
  ```
  and write the key values in them
- create a file .env(.env-non-dev for docker) and specify the value of the fields
  ```
  DB_HOST=...
  DB_PORT=...
  DB_NAME=...
  DB_USER=...
  DB_PASS=...
  ```
  and for the docker, more
  ```
  POSTGRES_DB=...
  POSTGRES_USER=...
  POSTGRES_PASSWORD=...
  ```
- launching the application
  locally
  ```
  pip install -r requirements.txt
  uvicorn main:app --reload
  ```
  docker
  ```
  docker compose build
  docker compose up
  ```
  

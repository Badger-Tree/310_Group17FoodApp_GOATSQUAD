# 310FoodApp_GOATSQUAD

navigate to localhost:8000/docs to access fastapi/swagger

docker commands: 

when first cloning the repo or if a new library is added, run: 
docker compose up --build

to start running the docker container to code where you left off: 
docker compose up

to run pytest, open a second terminal and run: 
docker exec -it goatsquad-backend pytest

to stop the container and cleanup:
docker compose down

Installation 
1. Install Docker with Docker Compose from: https://docs.docker.com/get-started/get-docker/
Versions:
Docker version 28.4.0, build d8eb465
Docker Compose version v2.39.4-desktop.1

2. Make a clone of the project repository on your local machine:
Run these commands from VSCode in your new project location:
git clone https://github.com/Badger-Tree/310_Group17FoodApp_GOATSQUAD
Cd project-location

3. Install dependencies: 
Run the following:
pip install -r requirements.txt

4.Configure environmental variable
If it doesn’t exist, create frontend/.env and add the following:
VITE_API_BASE_URL=http://127.0.0.1:8000

5.Build Dockerfile
Run the following:
Docker compose up –build

6. Access the application:
Front end: http://localhost:5173
Back end: http://localhost:8000
Admin: http://localhost:3001

7. Stop application
Run the following:
Docker compose down

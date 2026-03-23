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
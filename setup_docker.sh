docker build -t python-parser-api ./ -f Dockerfile.fastapi

docker stop python-parser-api-container

docker rm python-parser-api-container

docker run --privileged=true -d --name python-parser-api-container -p 13456:13456 python-parser-api

docker build -t python-parser-ui ./ -f Dockerfile.streamlit

docker stop python-parser-ui-container

docker rm python-parser-ui-container

docker run --privileged=true -d --name python-parser-ui-container -p 13457:13457 python-parser-ui


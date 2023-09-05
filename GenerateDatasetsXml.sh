#!/bin/bash
source .env
CMD="bash GenerateDatasetsXml.sh -verbose $@"
echo $CMD
docker run --rm -it \
  -v "${DATA_DIR}:/datasets" \
  -v "${PWD}/logs:/erddapData/logs" \
  -v ${PWD}/erddap/content:/usr/local/tomcat/content/erddap \
  axiom/docker-erddap:2.23-jdk17-openjdk \
  bash -c "cd webapps/erddap/WEB-INF/ && eval $CMD"

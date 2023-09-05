#!/bin/bash
CMD="bash GenerateDatasetsXml.sh -verbose $@"
echo $CMD
docker run --rm -it \
  -v "/data/layers:/datasets" \
  -v "$(pwd)/logs:/erddapData/logs" \
   -v $(pwd)/erddap/content:/usr/local/tomcat/content/erddap \
  axiom/docker-erddap:2.23-jdk17-openjdk \
  bash -c "cd webapps/erddap/WEB-INF/ && bash GenerateDatasetsXml.sh -verbose"

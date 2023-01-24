#!/bin/bash
CMD="bash GenerateDatasetsXml.sh -verbose $@"
echo $CMD
docker run --rm -it \
  -v "/data/layers:/datasets" \
  -v "$(pwd)/logs:/erddapData/logs" \
  axiom/docker-erddap:2.18 \
  bash -c "cd webapps/erddap/WEB-INF/ && $CMD"

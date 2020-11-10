#!/bin/bash
docker build -t 172.16.30.245:21197/thiennt/compress_image:v1 .
docker push 172.16.30.245:21197/thiennt/compress_image:v1
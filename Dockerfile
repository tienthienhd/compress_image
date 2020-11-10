FROM python:3.6-slim
MAINTAINER Tien Thien <tienthienhd@gmail.com>

# install build utilities
RUN apt-get update &&\
    apt-get install -y libgtk2.0-dev cmake

COPY requirements.txt /tmp/requirements.txt
WORKDIR /tmp
# installing python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /workspace

# Set the working directory for container
WORKDIR /workspace

#CMD ["python3", "api/app.py"]
CMD ["./script_run.sh"]
# syntax=docker/dockerfile:1

FROM python:3.10-slim-bullseye

WORKDIR /python-docker

RUN apt-get update && apt-get upgrade -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Add a new group "radix-non-root-group" with group id 1000 
RUN groupadd -g 1000 radix-non-root-group

# Add a new user "radix-non-root-user" with user id 1000 and include in group
RUN useradd -u 1000 -g radix-non-root-group radix-non-root-user

COPY . .

EXPOSE 5000
USER 1000

CMD [ "python", "app.py" ]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
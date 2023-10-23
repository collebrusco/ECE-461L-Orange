# Including lots of comments as I'm new to docker 
# and want to be clear about what each line does

# start with python runtime
FROM python:3.8

# workdir is in /app directory
WORKDIR /app

# bring in requirements file
COPY ./requirements.txt /app

# install reqs
RUN pip install --no-cache-dir -r requirements.txt

# bring directory into container
COPY . /app

# expose the port, flask uses 5000 by default, could change this
EXPOSE 80

CMD ["python", "main.py"]


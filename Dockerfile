# start from an official image
FROM python:3.6

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp/hasker
WORKDIR /opt/services/djangoapp/hasker

# install our two dependencies
COPY requirements.txt /opt/services/djangoapp/hasker
RUN pip install -r requirements.txt

# copy our project code
COPY . /opt/services/djangoapp/hasker

# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "scp", "--bind", ":8000", "hasker.wsgi:application"]

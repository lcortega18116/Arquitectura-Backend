FROM python:3.9
ENV PYTHONUNBUFFERED  1

# install FreeTDS and dependencies
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install --reinstall build-essential -y

# Add SQL Server ODBC Driver 17 for Ubuntu 18.04
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y --allow-unauthenticated msodbcsql17
RUN ACCEPT_EULA=Y apt-get install -y --allow-unauthenticated mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

WORKDIR /BackendApp
COPY requirements.txt /BackendApp/requirements.txt

#RUN pip install mysql-python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install djangorestframework
RUN pip install beautifulsoup4
RUN pip install load_dotenv

COPY . /BackendApp
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
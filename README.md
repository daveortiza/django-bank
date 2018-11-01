# django-bank
This project demonstrates simple solution based on online banking theme.
Application provides secure form to manage operations over and between credit cards. 
Included Redis storage for client cards.
Also included Adminer (docker container) for manage database.

Please visit <a href="https://bank.alexdevel.pro">https://bank.alexdevel.pro</a> (production version)

Test user:
> username: django@django.dev

> password: djangodjango


Test user credit card:
> Card number 9027578398661306

> Pincode 1366

![alt text](https://raw.githubusercontent.com/oleksii-velychko/django-bank/master/screenshot.png)


In order to start this project (after cloning) need to follow next steps:

1. To ensure HTTPS connections need a generate self-signed certificate:

    ```
    cd django-bank/docker/openssl
    mkdir certs

    openssl genrsa -des3 -out certs/rootCA.key 2048
    openssl req -x509 -new -nodes -key certs/rootCA.key -sha256 -days 365 -out certs/rootCA.pem
    openssl req -new -sha256 -nodes -out certs/server.csr -newkey rsa:2048 -keyout certs/server.key -config <( cat server.csr.cnf )
    openssl x509 -req -in certs/server.csr -CA certs/rootCA.pem -CAkey certs/rootCA.key -CAcreateserial -out certs/server.crt -days 500 -sha256 -extfile v3.ext
    ```

    Then import rootCA.pem to browser through Settings -> Manage Certficates -> Authorities tabs

2. Build and run docker containers:

    ```
    docker-compose build
    docker-compose up -d
    docker-compose ps
    ```
    
    last command will show status of running containers.
    
3. Add services names to /etc/hosts

    ```
    # VirtualHosts
    127.0.0.1       app.local postgres redis
    ```
    
4. Now install and js libraries:

    ```
    cd django/project/staticfiles
    npm install
    ```
    
5. Execute necessary Django commands:

    ```
    cd django
    python3 ./manage.py makemigrations --settings=project.local
    python3 ./manage.py migrate --settings=project.local
    python3 ./manage.py collectstatic
    ```
    
6. Run tests for banking application:

    ```
    python3 ./manage.py test banking
    ```
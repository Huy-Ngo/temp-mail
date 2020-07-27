# Temporary email

This mini-project aims to create a mail server
that generates disposable email addresses that
expire after a few minutes.

User will receive an email address that can
receive emails. Users can read mail in this address
before the expiration. The mail account will be deleted
after the expiration.

## Running

Firstly, run the flask API:

```shell script
export FLASK_ENV='development'
flask run
```

Next, run the SMTP server:

```shell script
python3 server.py
```

You can try sending to a localhost mail server with python's [smtplib][1].

## Configuration

- `SQLALCHEMY_DATABASE_URI`: URI to create database (See [SQLAlchemy doc][2])
- `ENV`: Set to `development` to use another port than 25.
- `HOST`: The IP of the host
- `HOST_PORT`: The IP and port of the host
- If there is a domain name configured for this app, set both above
 variables to be the same as domain name.
 
## Deployment instruction

The following instruction assumes that you are deploying to an Ubuntu server 
with Nginx as web server engine.

**Step 1:** Clone this project to the directory

Clone to the wanted folder. In this instruction, it's assumed to be `/var/www/`

```shell script
cd /var/www/
git clone https://github.com/Huy-Ngo/temp-mail
```

**Step 2:** Create a configuration file

Note: values in `<>` should be replaced with appropriate values.

```json
{
  "SQLALCHEMY_DATABASE_URI": "<dialect+driver://username:password@host:port/database>",
  "ENV": "production",
  "SECRET_KEY": "<a long secret key>",
  "HOST_PORT": "<domain name>",
  "HOST": "<domain name>",
  "JWT_TOKEN_LOCATION": ["headers", "cookies"],
  "JWT_ERROR_MESSAGE_KEY": "message",
  "PROPAGATE_EXCEPTIONS": true
}
```

**Step 3:** Install dependencies

Install the dependencies in a virtual environment.

```shell script
apt install nginx  # On Ubuntu or Debian-based server
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

**Step 4:** Write configuration files

You have to write the following configuration files:

- nginx configuration for port forwarding
- systemd configurations for:
    - temp-mail API/web server
    - SMTP server

nginx configuration: `/etc/nginx/sites-availables/temp-mail`
```nginx
server {
    listen 80;
    server_name 15minmail.tk www.15minmail.tk;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/temp-mail/temp-mail.sock;
    }
}
```

Make a symlink to `sites-enabled`

```shell script
ln -s /etc/nginx/sites-availables/temp-mail /etc/nginx/sites-enabled
```

Temp-mail systemd configuration: `/etc/systemd/system/temp-mail.service`

```ini
[Unit]
Description=Gunicorn instance to serve Temporary Mail API
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/temp-mail
Environment="PATH=/var/www/temp-mail/venv/bin"
ExecStart=/var/www/temp-mail/venv/bin/gunicorn --workers 3 --bind unix:temp-mail.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

SMTP mail server configuration: `/etc/systemd/system/smtp-server.service`

```ini
[Unit]
Description=Service to run SMTP server.

[Service]
Type=simple
ExecStart=/usr/bin/python3 /var/www/temp-mail/server.py

[Install]
WantedBy=multi-user.target
```

Make sure all services are running:

```shell script
systemctl restart nginx.service
systemctl restart temp-mail.service
systemctl restart smtp-server.service
```

**Step 5:** Allow nginx on ufw

```shell script
ufw allow 'Nginx Full'
```

[1]: https://docs.python.org/3/library/smtplib.html 
[2]: https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls
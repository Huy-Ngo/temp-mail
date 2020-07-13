# Temporary email

This mini-project aims to create a mail server
that generates disposable email addresses that
expire after a few minutes.

User will receive an email address that can
receive emails. Users can read mail in this address
before the expiration. The mail account will be deleted
after the expiration.

## Running test

Technically there isn't a (automatic) test for this API yet.
However, some basic functionalities can be
tested with the scripts in `test_server`.

Firstly, run the flask API:

```shell script
export FLASK_ENV='development'
flask run
```

Next, run the SMTP server:

```shell script
cd test_server
python3 server.py
```

Run `client.py` to get a new email, send a mail to this server, or read the mails.

```shell script
python3 client.py [new/send/read]
```

## Configuration

- `SQLALCHEMY_DATABASE_URI`: URI to create database
- `ENV`: Set to `development` to use another port than 25.
- `HOST`: The IP of the host
- `HOST_PORT`: The IP and port of the host
- If there is a domain name configured for this app, set both above
 variables to be the same as domain name.
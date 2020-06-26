# Test server

The scripts in this folder serve the purpose of testing.

The `server.py` file will set up an SMTP server.
The `client.py` file represent a client sending a mail to the
server with SMTP.

The client will first send a POST request to the API
and get a disposable mail address and send the email
to this address.

The server upon receiving the email from the client
will send a POST request to the API to save the mail
to the database.

There hasn't been a script for viewing email yet.

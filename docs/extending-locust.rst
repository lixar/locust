=================
Extending Locust
=================

Locust comes with a number of events that provides hooks for extending locust in different ways.

Event listeners can be registered at the module level in a locust file. Here's an example::

    from locust import events

    def my_success_handler(method, path, response_time, response, **kw):
        print "Successfully fetched: %s" % (path)

    events.request_success += my_success_handler

.. note::

    It's highly recommended that you add a wildcard keyword argument in your listeners
    (the \**kw in the code above), to prevent your code from breaking if new arguments are
    added in a future version.

.. seealso::

    To see all available event, please see :ref:`events`.



Adding Web Routes
==================

Locust uses Flask to serve the web UI and therefore it is easy to add web end-points to the web UI.
Just import the Flask app in your locustfile and set up a new route::

    from locust import web

    @web.app.route("/added_page")
    def my_added_page():
        return "Another page"

You should now be able to start locust and browse to http://127.0.0.1:8089/added_page


Enabling SSL
==================

The Locust web interface also supports SSL encrypted connections. This is especially useful
if, for instance, you're testing an API which may incidentally expose personal information
or application secrets through the web interface.

To enable SSL, you simply need to generate (or otherwise obtain) an SSL certificate and key.
A quick way to do this on systems with OpenSSL installed is to execute the following:

.. code::

    openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365

Then, simply set the Locust OpenSSL environment variables before you run it.

You can put the following lines in your Bash `.profile` or `.bashrc`.

.. code::

    export SSL_KEY=/path/to/key.pem
    export SSL_CERT=/path/to/cert.pem

Optionally, you can also set them prior to invoking locust.

.. code::

    SSL_KEY=/path/to/key.pem SSL_CERT=/path/to/cert.pem locust


Enable Authenticated Access
===========================

.. attention::

    Using this feature in no way makes the data transfered between locusts or between
    the locust master and the client secure.

Locust supports basic access authentication. This is a simply form of authentication
where a browser will prompt for a username and password if a HTTP 401 response is
returned with a special header.

The idea behind using this sort of authentication is not for securing the data transferred
between the client and locust, as that is still transmitted in plain text, however, it will
prevent unauthorized tampering via the web interface with a test. This could also be useful
if a load tester is used in a multi-developer environment where each developer could invoke
locust with their own credentials.

Enabling support for basic authentication is done by specifying two environment variables.

You can put the following lines in your Bash `.profile` or `.bashrc`.

.. code::

    export LOCUST_USER_NAME=my_user
    export LOCUST_PASSWORD=secret

Optionally, you can also set them prior to invoking locust.

.. code::

    LOCUST_USER_NAME=my_user LOCUST_PASSWORD=secret locust

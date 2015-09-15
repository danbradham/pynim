==============
NIM Python API
==============
This is an exploration of interacting directly with the NIM Database via Python. It is not ready for production and not condoned by nim-labs, but, we'll see what happens. Here we use SQLAlchemy to dynamically generate an ORM
for the NIM MySQL database. The reason I'm exploring this avenue is because the HTTP api does not yet support POST or PUT requests for most tables in the database.


Configuration
=============

::

    >>> import pynim
    >>> pynim.configure(host='ny-nim', user='root', database='n_proj')

In my case I have NIM running under the hostname ny-nim. Yours will almost certainly be different. Without a dns nameserver it will be a standard ip address on your local area network. The default user and database for NIM are *root* and *ny_proj*. Once configured we can query the database using an object-relational-model via SQLAlchemy.


Sessions
========

Now that we have configured pynim and generated a basic ORM we can query the database using an SQLAlchemy Session object.

::

    >>> from pynim import models
    >>> sess = pynim.get_session()
    >>> all_users = sess.query(models.Users).all()
    [<pynim.Users object at 0x0000000004C535F8>, ...]

For more advanced queries see the SQLAlchemy documentation.


Getting fields from a model
===========================

Great, now let's try something like modifying a users username field.

::

    >>> franklin = sess.query(models.Users).filter(
    ...     models.Users.username == 'franklin').first()
    >>> franklin.username = 'frank'

So we've modified franklin's username to frank, but we have yet to change the database. Currently this change is just queued up in our Session object. Let's commit the change.

::

    >>> sess.commit()

Now all the changes we made with the Session object have been commited to the database.

All database tables are accessible through this api in the same fashion as models.Users. The beauty is that they are all dynamically created so future changes won't break this implementation, though it may break some client code if a table or column are removed.


Plans
=====

 * Write a slim wrapper around the Dynamically generated models for common functionality.
 * Abstract session objects away from clients. The basic api should be much simpler handling the session object automatically. If the user wants the power of the session object they still have access through the pynim.get_session method.

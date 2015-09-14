==============
NIM Python API
==============
This is an exploration of the NIM HTTP API in Python. It is not ready for production, but, we'll see where it goes.


Configuration
=============

::

    >> import pynim
    >> pynim.configure(hostname='ny-nim')

In my case I have NIM running under the hostname ny-nim. Yours will almost certainly be different. Without a dns nameserver it will be a standard ip address on your local area network. Once configured we can make requests to our NIM server.


Finding Users
=============

::

    >> pynim.User.find()
    [<User>(_id=1, username=nim)...]

Here we get a list of all users available on the ny-nim server configured above.

::

    >> nim_user = pynim.User.find_one(username='nim')
    >> nim_user
    <User>(_id=1, username=nim)

Now we find the first user with username *nim*. You can query using any User attribute available through the http api.


Getting a users jobs
====================

::

    >> nim_user.get_jobs()
    [<Job>(_id=9, number=99999, jobname=TESTING, folder=TESTING)]


Getting a project path relative to a server
===========================================
*Bugs in http api here...the ?q=getPaths uri will not return job paths if the job is not yet brought online, and will return paths for another job that IS online. Additionally looking up an asset will return the path to an actual asset not a generic asset path.*

::

    >> test_server = pynim.Server.find_one(server='TEST_SERVER')
    >> test_server
    <Server>(_id=23, server=TEST_SERVER, mountpoint=/media/sf_test, root=Z:/)
    >> test_job = nim_user.get_job(jobname='TESTING')
    >> test_job.get_path('job', 'root', test_server)
    Z:/99999_TESTING

Here we use the **get_path** method of a Job object to get the jobs root path relative to the test_server. *root* is an attribute unique to pynim, it returns the path for the current platform, in this case *win*.

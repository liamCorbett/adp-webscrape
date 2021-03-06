====================
ADP website scraping
====================
A Selenium-based python script for logging into ADP Resource and downloading reports.


Usage
=====

Installation
------------
With Python 3.6 or greater installed, in a command prompt: enter ``pip install adp-webscrape``. You'll also need a recent edition of Firefox and its respective GeckoDriver_. The GeckoDriver must be added to PATH, or to the root folder of the project.

.. _GeckoDriver: https://github.com/mozilla/geckodriver/releases

Code
----
Use the following code, replacing my_username, my_password, my_download_path, and my_isi_client_id with relevant information.

- ``my_username``: Your ADP Resource username
- ``my_password``: Your ADP Resource password
- ``my_download_path``: (optional) The path that Selenium's browser will download reports to (e.g ``C:\adp-reports``). Ommiting defaults to the user's download folder.
- ``my_isi_client_id``: This can be found at the end of the url for any ezLaborManager page. Most likely, it's going to be your company name (probably spaced out by hyphens if the name is multiple words).
- ``my_report_index``: On the ezLaborManager "My Reports" page, this will be the index of the report you want to download (with the first report starting at index 0) https://i.imgur.com/Tg7kPQV.png
- ``my_file_prefix``: (optional) If you'd like to prefix the name of your files with some word so as to not mix report names, you may do so here.

.. code-block:: python

    import atexit
    from adpwebscrape import ADPResource


    resource = ADPResource('my_username', 'my_password',
                               isi_client_id='my_isi_client_id',
                               download_path=r'my_download_path') 
                               
    resource.download_my_report(my_report_index, prefix='my_file_prefix') #returns Filename

    atexit.register(resource.quit)

Other
=====

Why no official API?
--------------------
There isn't one. ADP Marketplace has an API, though it is very separate from the reports I've attempted to generate here.

Why Selenium and not regular schmegular requests?
-------------------------------------------------
Requests to ADP Resource require hidden fields whose contents seem like a pain to generate programatically. Selenium was chosen because it handles all of that at the cost of a little performance. Please let me know if you find a better way to do this.

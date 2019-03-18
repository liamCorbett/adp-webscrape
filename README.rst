====================
ADP website scraping
====================
A Selenium-based python script for logging into ADP Resource and downloading reports.


Usage
=====

Installation
------------
In a command prompt, enter ``pip install adp-webscrape``.

Code
----
Use the following code, replacing my_username, my_password, my_download_path, and my_isi_client_id with relevant information.

- ``my_username``: Your ADP Resource username
- ``my_password``: Your ADP Resource password
- ``my_download_path``: (optional) The path that Selenium's browser will download reports to (e.g ``C:\adp-reports``). Ommiting defaults to the user's download folder.
- ``my_isi_client_id``: This can be found at the end of the url for any ezLaborManager page. Most likely, it's going to be your company name (probably spaced out by hyphens if the name is multiple words).

.. code-block:: python

    from adp-webscrape import ADPResource
    
    
    adp_resource = ADPResource('my_username', 'my_password', 
                               isi_client_id='my_isi_client_id',
                               download_path=r'my_download_path') 
                               
    adp_resource.download_timecard_csv() # returns filename

Other
=====

Why no official API?
--------------------
There isn't one. ADP Marketplace has an API, though it is very separate from the reports I've attempted to generate here.

Why Selenium and not regular schmegular requests?
-------------------------------------------------
Requests to ADP Resource require hidden fields whose contents seem like a pain to generate programatically. Selenium was chosen because it handles all that for me at the cost of a little performance. Please let me know if you find a better way to do this.

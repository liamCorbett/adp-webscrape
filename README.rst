====================
ADP website scraping
====================
A Selenium-based python script for logging into ADP Resource and downloading reports.


Why no official API?
====================
There isn't one. ADP Marketplace has an API, though it is very separate from the reports I've attempted to generate here.


Why Selenium and not regular schmegular requests?
=================================================
Was a pain in the ass to generate the hidden field names and contents programatically. Selenium was chosen because it handles all that for me despite the performance hit. Please let me know if you find a better way to do this.



Oomnitza - User Synchronization via OneLogin REST API
===========================

Python package to synchronize users from OneLogin to Oomnitza via REST API.

Prerequisites
-------------
 * xmltodict ~> 0.9.0
 * requests ~> 2.3.0

Usage
-----
* Update `config.ini` with your OneLogin and Oomnitza connection settings. For Oomnitza credentials, we recommend creating an additional "user" for this task.
* Perform `./run.sh` or `python start.py`
# graphite-postgres-connections
Polls metrics from Postgres and delivers them to Graphite

graphite-postgres-connections (gr-pg-cx.py) is a Python script that polls total connection count from a list of Postgres servers using Nagios' NRPE and delivers the data to a Graphite server.


## Getting Started

These instructions will get you graphite-postgres-connections up and running:


1.  It is recommended to install and run graphite-postgres-connections on the Nagios/Icinga server.  Otherwise, additional tweaks is required to allow it to run properly with a Nagios/Icinga and Postgres servers. 

2.  Prerequisite software installed.  See the Prerequisites section.

3.  Update/redefine values in the code.  See the Prerequisites section.

4.  When all necessary steps are completed and configured accordingly, the script should normally not take longer than a minute to finish running.  Otherwise, proceed to troubleshoot.

5.  Add gr-pg-cx.py to crontab with the run interval of your choice.


## Prerequisites

**Software**

Other software the works in conjunction with graphite-postgres-connections:

* [Nagios](https://www.nagios.org/downloads/) or [Icinga 1.x](https://icinga.com/) with check_nrpe executable 
* [check_postgres Nagios plugin](https://bucardo.org/check_postgres/)
* External [Graphite](https://graphiteapp.org/) server.
* External [PostgreSQL](https://www.postgresql.org/) servers.

**Configuration**
* Update/redefine values in gr-pg-cx.py to your specifications. (See comments in the code.)
* Update/redefine 'path' in the dissect function.


## Known Issue

All data will not be pulled should a Postgres server fails or becomes inaccessible in the list.


## Troubleshooting

gr-pg-cx.py 'hangs':

* Ensure all Postgres servers are accessible via NRPE.
* Ensure all Postgres servers have check_postgres Nagios plugin installed and nrpe.cfg is properly configured.
* Ensure all Postgres servers are configured properly.
* Try restarting the nrpe service.


No results in Graphite:

* Ensure Graphite server is running and can accept connections from Nagios (or where gr-pg-cx.py resides on).
* May need to remove all old/previous whisperdata on Graphite related to gr-pg-cx.py.


## Author
* **Archie N. Lai** (https://github.com/archcast)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

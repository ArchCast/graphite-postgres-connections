#!/usr/bin/env python

# graphite-postgres-connections
# gr-pg-cx.py:
# This script polls total connection count from a list of Postgres
# servers using Nagios' NRPE and delivers data to Graphite.
# Requires:
# 	Python 2
#	Nagios with check_nrpe executable
# 	"check_postgres" Nagios plugin (https://bucardo.org/check_postgres/)
# 	External Graphite server (https://graphiteapp.org/)
# 	External Postgres servers.
# 	Update/redefine 'path' in the dissect function.
#
# Known issue:  All data will not be pulled should a Postgres server fails in the list.
#
# Update: 12-18-2018
# archie@archcast.net

import subprocess, re, time, socket, sys, pickle, struct

# Uncomment and redefine the external graphite server:
# graphite_server = "10.0.0.21"

# Uncomment system path for NRPE:
# nrpe = "/usr/lib/nagios/plugins/check_nrpe -H "

# Uncomment and redefine for list of Postgres servers:
# pg_servers = ["prod-pg01", "prod-pg02", "prod-pg03", "prod-pg04"]

# "check_postgres_connections" is defined in nrpe.cfg that executes the check_postgres Nagios/NRPE
# plugin (from https://bucardo.org/check_postgres/) which gather connection counts from Postgres servers.
# (NRPE and this plugin must be installed on all affected Postgres servers.)
# Uncomment below (if needed, change accordingly):
# check = " -c check_postgres_connections"

# "OCN_production_shard" can be used for collecting and graphing other metrics.
# OCN_production_shard = []

total_pg_backend_connections = []


# Collects data from Postgres servers:
def dissect(server_list):
	for host in server_list:
		timestamp = int(time.time())
		
		# Execute the entire command on the system:
		cmd = nrpe + host + check
		p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
		output = p.communicate()[0]

		# Data finagling:
		exp = output.split(";")[4:17]
		aggr = int(output.split(" ")[4])

		# Monkey patch output:
		# print "cmd:", cmd, "output:",output

		# Uncomment and redefine the path for your set up:
		# path = "shard." + host

		aggregate = (path, (timestamp, aggr))
		total_pg_backend_connections.append(aggregate)
		
		for element in exp:
			if "=" in element:
				element = element.split(" ")[1]
				path = host + "." + element.split("=")[0]
				value = int(element.split("=")[1])
				pick = (path, (timestamp, value))

				# Uncomment below if needed:
				# OCN_production_shard.append(pick)


# Ships the data to Graphite:	
def graphite(content):
	payload = pickle.dumps(content)
	header = struct.pack("!L", len(payload))
	message = header + payload
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("graphite_server", 2004))
	sock.sendall(message)		


# Polls data from the list of Postgres servers:
dissect(pg_servers)

# Sends polled data from the list of Postgres servers to Graphite
graphite(total_pg_backend_connections)

# Uncomment below if needed:
# graphite(OCN_production_shard)

# -*- coding: utf-8 -*-
"""
    Collection of utilities to interact with mongodb
"""

import pymongo
import re


def normalize_uri(host, port):
    port = port if port else 27017
    url = '{host}:{port}'.format(**dict(
        host=host,
        port=port))
    return url


def get_standalone_connection(uri, **kwargs):
    return pymongo.MongoClient(uri, **kwargs)


def get_cluster_connection(hosts, replica_set, **kwargs):
    host_list = ','.join(hosts)
    return pymongo.MongoReplicaSetClient(host_list, replicaSet=replica_set, **kwargs)


def get_connection(url_or_hosts, cluster=None, **kwargs):
    """
        Returns a connection to a mongo database.

        If you want to connect to a single non-clustered mongodb instance, just provide
        the host where the mongo db resides:

        >>> get_connection('localhost')

        This will assume the default 27017 port. If you want to change the port, you can do it
        by including the port in the url:

        >>> get_connection('localhost:27018')

        Method also accepts full qualified urls:

        >>> get_connection('mongodb://localhost:27018')

        If you want to connect to a cluster, you hav to provide a comma separated list
        of hosts, each following the format described previously, and provide the name of the
        cluster

        >>> get_connection('server1,server2:27018,server3', 'cluster_name')

        Extra keywords arguments in kwargs will be passed to the actual pymongo method
        used to retrieve the connection

    """
    if cluster:
        hosts = re.findall(r'\s*(?:\w+://)?([^:\s,;]+):?(\d*)\s*', url_or_hosts)
        if len(hosts) < 3:
            raise Exception('Invalid cluster hosts list. We need at least 3 hosts.')
        hosts = [normalize_uri(*parts) for parts in hosts]
        connection = get_cluster_connection(hosts, replica_set=cluster, **kwargs)
    else:
        parts = re.search(r'(?:\w+://)?([^:\s,;]+):?(\d*)', url_or_hosts)
        if not parts:
            raise Exception('Invalid standalone mongodb url.')
        uri = normalize_uri(*parts.groups())
        connection = get_standalone_connection(uri, **kwargs)

    return connection


def get_database(connection, db_name, username=None, password=None, authdb=None):
    """
        Retrieves a database from a connection, performing authorization if needed.

        If the database  you want to connect has authorization enabled, you
        must provide both username and password. Authentication will be performed
        against the database specified in db_name.

        >>> connection = get_connection('localhost')
        >>> db = get_database(connection, 'mydb', username='admin', password='secret')

        If the authorization must be performed with a different database, you
        can specify it with the authdb keyword argument.

        >>> db = get_database(connection, 'mydb', username='admin', password='secret', authdb='admin')
    """
    authorization_enabled = username or password or authdb
    if authorization_enabled:
        authdb_name = db_name if authdb is None else authdb
        if username and password:
            auth_db = connection[authdb_name]
            auth_db.authenticate(username, password)
        else:
            raise Exception('Missing username or password')

    return connection[db_name]

from cassandra.cluster import Cluster
from environment import CASSANDRA_HOST, CASSANDRA_PORT, CASSANDRA_KEYSPACE

def get_cassandra_session():
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect(CASSANDRA_KEYSPACE)
    return session
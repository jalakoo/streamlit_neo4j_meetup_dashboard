from neo4j import GraphDatabase, Query

class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(
                self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, **kwargs):
        assert self.__driver is not None, "Driver not initialized!"
        try:
            with self.__driver.session() as session:
                # See https://neo4j.com/docs/python-manual/current/session-api/ 
                # for using sessions with Query objects
                result = session.run(Query(query), kwargs)
                return result.data()
        except Exception as e:
            print("query failed:", e)

    def write(self, query, **kwargs):
        assert self.__driver is not None, "Driver not initialized!"
        def execute(tx):
            result = tx.run(query, kwargs)
            return result
        try:
            with self.__driver.session() as session:
                return session.write_transaction(execute)
        except Exception as e:
            print("write failed:", e)
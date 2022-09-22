from neo4j import GraphDatabase, unit_of_work

# Static units of work that can be retried if they fail

@unit_of_work(timeout=5)
def _get_meetups(tx):
    result = tx.run("""
        MATCH (m:Meetup)
        RETURN m.name as name
    """)
    return [record["name"] for record in result.data()]

@unit_of_work(timeout=5)
def _num_attendees(tx, meetup_name):
    result = tx.run("""
        MATCH (a:Attendee)-[:ATTENDED]->(m:Meetup {name: $meetup_name})
        RETURN count(a) as num_attendees
    """, meetup_name=meetup_name)
    return result.data()[0]["num_attendees"]

@unit_of_work(timeout=5)
def _num_unique_skills(tx, meetup_name):
    result = tx.run("""
        MATCH (m:Meetup {name: $meetup_name})<-[:ATTENDED]-(a:Attendee)-[:KNOWS]->(s:Skill)
        RETURN count(distinct s) as num_skills
    """, meetup_name=meetup_name)
    return result.data()[0]["num_skills"]

@unit_of_work(timeout=5)
def _avg_skills_per_attendee(tx, meetup_name):
    result = tx.run("""
        MATCH (m:Meetup {name: $meetup_name})<-[:ATTENDED]-(a:Attendee)-[:KNOWS]->(s:Skill)
        RETURN avg(size((a)-[:KNOWS]->())) as avg_skills
    """, meetup_name=meetup_name)
    return result.data()[0]["avg_skills"]

@unit_of_work(timeout=5)
def _get_graph_data(tx, meetup_name):
    result = tx.run("""
        MATCH (m:Meetup {name: $meetup_name})<-[:ATTENDED]-(a:Attendee)-[:KNOWS]->(s:Skill)
        RETURN a.name as attendee, s.name as skill
    """, meetup_name=meetup_name)
    return result.data()

@unit_of_work(timeout=5)
def _get_attendees(tx, meetup_name):
    result = tx.run("""
        MATCH (m:Meetup {name: $meetup_name})<-[:ATTENDED]-(a:Attendee)
        RETURN a.name as attendee
    """, meetup_name=meetup_name)
    return result.data()

class Neo4jController:
    
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

    def get_meetups(self):
        assert self.__driver is not None, "Driver not initialized!"
        try:
            with self.__driver.session() as session:
                return session.execute_read(_get_meetups)
        except Exception as e:
            print("get_meetups failed:", e)

    def num_attendees(self, meetup_name):
        assert self.__driver is not None, "Driver not initialized!"
        try:
            with self.__driver.session() as session:
                return session.execute_read(_num_attendees, meetup_name)
        except Exception as e:
            print("num_attendees failed:", e)

    def num_unique_skills(self, meetup_name):
        assert self.__driver is not None, "Driver not initialized!"
        try:
            with self.__driver.session() as session:
                return session.execute_read(_num_unique_skills, meetup_name)
        except Exception as e:
            print("num_unique_skills failed:", e)

    def avg_skills_per_attendee(self, meetup_name):
        assert self.__driver is not None, "Driver not initialized!"
        try:
            with self.__driver.session() as session:
                return session.execute_read(_avg_skills_per_attendee, meetup_name)
        except Exception as e:
            print("avg_skills_per_attendee failed:", e)

    def get_graph_data(self, meetup_name):
        assert self.__driver is not None, "Driver not initialized!"
        try:
            with self.__driver.session() as session:
                return session.execute_read(_get_graph_data, meetup_name)
        except Exception as e:
            print("get_graph_data failed:", e)

    def get_attendees(self, meetup_name):
        assert self.__driver is not None, "Driver not initialized!"
        try:
            with self.__driver.session() as session:
                return session.execute_read(_get_attendees, meetup_name)
        except Exception as e:
            print("get_attendees failed:", e)

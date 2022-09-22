from neo4j_connection import Neo4jConnection

class Neo4jController():
    """Abstraction for converting requests
    to Cypher commands to be executed by Neo4j
    driver.

    A class like this should be edited to
    meet your own needs.
    """
    
    def __init__(self, uri, user, pwd):
        try:
            self.conn = Neo4jConnection(uri, user, pwd)
        except Exception as e:
            print("Failed to create Neo4jFunctions:", e)

    def get_meetups(self):
        query : str = """
            MATCH (m:Meetup)
            RETURN m.name as name
        """
        result = self.conn.query(query)
        return [record["name"] for record in result]

    def num_attendees(self, meetup_name):
        query = """
            MATCH (a:Attendee)-[:ATTENDED]->(m:Meetup {name: $meetup_name})
            RETURN count(a) as num_attendees
        """
        result = self.conn.query(query, meetup_name=meetup_name)
        return result[0]["num_attendees"]

    def num_unique_skills(self, meetup_name):
        query = """
            MATCH (m:Meetup {name: $meetup_name})<-[:ATTENDED]-(a:Attendee)-[:KNOWS]->(s:Skill)
            RETURN count(distinct s) as num_skills
        """
        result = self.conn.query(query, meetup_name=meetup_name)
        return result[0]["num_skills"]

    def avg_skills_per_attendee(self, meetup_name):
        query = """
            MATCH (m:Meetup {name: $meetup_name})<-[:ATTENDED]-(a:Attendee)-[:KNOWS]->(s:Skill)
            RETURN avg(size((a)-[:KNOWS]->())) as avg_skills
        """
        result = self.conn.query(query, meetup_name=meetup_name)
        return result[0]["avg_skills"]

    def get_graph_data(self, meetup_name):
        query = """
            MATCH (m:Meetup {name: $meetup_name})<-[:ATTENDED]-(a:Attendee)-[:KNOWS]->(s:Skill)
            RETURN a.name as attendee, s.name as skill
        """
        result = self.conn.query(query, meetup_name=meetup_name)
        return result

    def get_attendees(self, meetup_name):
        query = """
            MATCH (m:Meetup {name: $meetup_name})<-[:ATTENDED]-(a:Attendee)
            RETURN a.name as attendee
        """
        result = self.conn.query(query, meetup_name=meetup_name)
        return result
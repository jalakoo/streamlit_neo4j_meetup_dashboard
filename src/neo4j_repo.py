from neo4j_utils import Neo4jConnection

class Neo4jRepository():
    
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
        print(f"get_meetups: {result}")
        return [record["name"] for record in result]

    def attendee_exists(self, email):
        query = """
            MATCH (a:Attendee {email: $email})
            RETURN a.name as name
        """
        result = self.conn.query(query, email=email)
        print(f"attendee_exists: {result}")
        if result is None:
            return False
        return True

    def delete_attendee(self, email):
        query = """
            MATCH (a:Attendee {email: $email})
            DETACH DELETE a
        """
        self.conn.write(query, email=email)


    def add_attendee(
        self, 
        name_first: str, 
        name_last: str, 
        email: str,
        meetup_name: str,
        meetup_date: str,
        skills: list = []):

        # Set meetup name
        meetup_uid = f"{meetup_name}_{meetup_date}"

        # Add attendee
        query = """
            MERGE (m:Meetup {name: $meetup_name})
            MERGE (a:Attendee {name: $name, first_name: $name_first, last_name: $name_last, email: $email})
            MERGE (a)-[:ATTENDED {date: $date}]->(m)
            RETURN a
        """
        last_initial = name_last[:1]
        fullname = f"{name_first} {last_initial}"

        # Add attendee
        self.conn.write(query, meetup_uid=meetup_uid, meetup_name=meetup_name, date=meetup_date, name=fullname, name_first=name_first, name_last=name_last, email=email)

        # Update to create & add skills relationships
        # TODO: Make more efficient please
        for skill in skills:
            print(f"Adding skill: {skill}...")
            query = """
                MERGE (s:Skill {name: $skill})
                """
            self.conn.write(query, skill=skill)

            print(f"Adding skill relationship between: {email} + {skill} ...")
            query = """    
                MATCH (a:Attendee {email: $email}),(s:Skill {name: $skill})
                MERGE (a)-[r:KNOWS]->(s)
                RETURN a,r, s
            """
            self.conn.write(query, email=email, skill=skill)
        

import streamlit as st
from constants import *
from neo4j_repo import Neo4jRepository
from datetime import date
import graphviz as graphviz

n4j = Neo4jRepository(st.secrets['neo4j_uri'], st.secrets['neo4j_user'], st.secrets['neo4j_password']) 

st.title("Meetup Dashboard")
meetups = n4j.get_meetups()
print(f"Meetups: {meetups}")

# Meetup selection
meetup_name = st.selectbox("Select a meetup", meetups)

if meetup_name is not None:
    # Major metrics
    # -------------
    # Number of attendees
    num_attendees = n4j.num_attendees(meetup_name)

    # Number of unique skills
    num_unique_skills = n4j.num_unique_skills(meetup_name)

    # Avg skills per attendee
    avg_skills_per_attendee = n4j.avg_skills_per_attendee(meetup_name)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Number of attendees", num_attendees)
    with col2:
        st.metric("Number of unique skills", num_unique_skills)
    with col3:
        st.metric("Average skills per attendee", avg_skills_per_attendee)

    # Graph of graph
    # --------------
    attendees = n4j.get_attendees(meetup_name)
    # Sample attendees = [{'attendee': 'Joy R'}, {'attendee': 'Jason K'}]
    graph_data = n4j.get_graph_data(meetup_name)
    # Sample of graph_data = [{'attendee': 'Jason K', 'skill': 'Swift (Apple programming language)'}, {'attendee': 'Jason K', 'skill': 'Kotlin'}, {'attendee': 'Jason K', 'skill': 'Dart'}]
    print(f"Graph data: {graph_data}")
    graph = graphviz.Digraph()
    for record in graph_data:
        graph.edge(record['attendee'], record['skill'])
    for attendee in attendees:
        graph.edge(meetup_name, attendee['attendee'])
    # graph.edge('run', 'intr')
    st.graphviz_chart(graph)
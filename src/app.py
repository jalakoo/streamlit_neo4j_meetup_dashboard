import streamlit as st
from constants import *
from neo4j_repo import Neo4jRepository
from datetime import date

n4j = Neo4jRepository(st.secrets['neo4j_uri'], st.secrets['neo4j_user'], st.secrets['neo4j_password']) 


def main():
    st.title("Meetup Dashboard")
    meetups = n4j.get_meetups()
    print(f"Meetups: {meetups}")

    st.selectbox("Select a meetup", meetups)

main()
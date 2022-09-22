# Graph Meetups
Demo Streamlit + Neo4j app for displaying information regarding a meetup
where attendees have registered with the graph_signup app

## Requirements
A running Neo4j instance. 

To create a cloud instance see [AuraDB](https://neo4j.com/cloud/platform/aura-graph-database)
To create a local instance see [Neo4j Desktop](https://neo4j.com/download-center/)

A .streamlit/secrets.toml file with the following credentials to connect with a Neo4j instance:
```
neo4j_uri = "_your_neo4j_uri_"
neo4j_user = "_your_neo4j_username_"
neo4j_password = "_your_neo4j_password_"
```

## Running
```
pipenv shell
pipenv sync
streamlit run src/app.py
```

## Streamlit
[Install instructions here](https://docs.streamlit.io/library/get-started/installation)

## License

The MIT License (MIT)

Copyright (c) 2022 Jason Koo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


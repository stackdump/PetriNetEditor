bitwrap-brython
===============

Use browser-based python('brython') for prototyping apps using the bitwrap eventstore.

**Status**

Developing Petri-Net Editor Using jQuery-UI and Snap.svg along w/ Brython.

development
-----------

[Brython Docs](https://www.brython.info/static_doc/en/intro.html?lang=en)

**Start DB and Broker**

    docker-compose up -d postgres rabbit

**Access Rabbit admin**

    http://127.0.0.1:15672

**Use Postgres cli**

    docker-compose exec postgres bash -c 'psql -U postgres'

**Add some Brython**

Add python docs to ./docs folder and then load in html.

    <body onload="brython(1)">
      <script type="text/python3" src="/src/console.py"></script>
      <textarea id=code class=codearea rows=100></textarea>
    </body>

**Run Server**

    ./entry.sh


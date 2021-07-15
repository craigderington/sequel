
## SEQUEL
A Distributed SQLAlchemy Database Workload Tool

* Installation
* Configuration
* Mocking the Backend
* Running the Workload
* Reviewing the Database Workload Results
* Screenshots (MySQL Workbench, Grafana, Flower)
* ToDos

#### Installation

```
$ cd Projects
:~/Projects $ git clone https://github.com/craigderington/sequel.git
:~/Project $ cd sequel
:~/Projects/sequel $ virtualenv venv --python=python3
:~/Projects/sequel $ . venv/bin/activate
(venv) :~/Projects/sequel $ poetry init
(venv) :~/Projects/sequel $ ... poetry prompts ...
(venv) :~/Projects/sequel $ poetry env use venv/bin/python
(venv) :~/Projects/sequel $ poetry install
(venv) :~/Projects/sequel $ ... dependencies installed ...
```

#### Configuration

Edit ```config.py``` file and chose the database engine, SQLite3 (default), or MySQL

```
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = base_dir + "sqlite3.db"
```

#### Mocking the Backend

I'm using [Mockaroo](https://www.mockaroo.com/) to simulate the backend and generate customer records, products and produce fake orders and shipping details.

To simulate your backend, sign up for free at Mockaroo and setup the schema from ```models.py```


#### Running the Workload

The script ```main.py``` is the entry point.  To run the workload, start the script with the following command line arguments.

```
(venv) :~/Projects/sequel $ python main.py --duration 10
```

#### Review Your Database Results

![Workbench Dashboard](https://aws-beacon-s3.s3.us-west-2.amazonaws.com/Screen+Shot+2021-07-15+at+9.20.48+AM.png)


#### ToDos
* Celery Integration
* Command Line/Env Var for AutoConfig, DEV vs PROD
* Add Threading for Load Throttling
* Add command argument for --database to set the database name at runtime

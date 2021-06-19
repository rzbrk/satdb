# satdb

`satdb` is a collection of Python tools and scripts to maintain a local database
for space object mean orbital elements. The database can be feed from
[CCSDS OMM](https://public.ccsds.org/Pubs/502x0b2c1e2.pdf) or
[TLE](https://en.wikipedia.org/wiki/Two-line_element_set).

## Structure of the repository

- `./data/`: This directory can be used to hold the downloaded OMM or TLE files with the mean orbital elements. It contains a subdirectoty `unprocessed` for data that was downloaded locally but not yet imported to the database and a subdirectory `processed` for downloaded data that was already imported to the database.
- `./lib/`: This directory contains the `satdb` python libraries.
- `./notebook/`: This diretory contains a collection of [Jupyter](https://jupyter.org/) notebooks to analyse the orbital elements in the database. It contains subdirectories to structure the notebooks for different types of satellites (e.g. constellations like Starlink) or orbital regions like LEO or GEO.
- `./scripts/`: This directory contains Python scripts to download orbital data from various sources like space-track.org or celestrak.com as well as scripts to import downloaded data to the database.
- `./setup/`: This directory contains scripts to support the setup of the `satdb` environment, mainly the database.

## Installation

### Database

Create a database and database user:

```
CREATE USER 'dbuser'@'%' IDENTIFIED BY PASSWORD 'secret';
CREATE database orbdata;
GRANT ALL PRIVILEGES ON 'orbdata.*' TO 'dbuser'@'%';
FLUSH PRIVILEGES;
```

Create the necessary empty tables in the database. Therefore, use the file
[`./setup/init.sql`](https://raw.githubusercontent.com/rzbrk/satdb/master/setup/init.sql) in the repository:

```
$ mysql -u dbuser -D orbdata -p < ./setup/init.sql
```

### Directory structure for data downloads

I recommend using a directory structure for the downloaded OMM and TLE files like the following:

* `./data/unprocessed/` here you can put all OMM and TLE downloads
  which have still to be imported to the database.
* `./data/processed/` here you can move all files which are already
  imported to the database. You can access these files at a later time, whenever
  necessary.

### Adapt the config file

An example configuration file for `satdb` is provided in the repository:
[`satdb_example.yaml`](https://raw.githubusercontent.com/rzbrk/satdb/master/satdb_example.yaml). Copy this configuration file to a suitable place like `~/.config/satdb.yaml`.

Edit the `satdb` config file `satdb.yaml`. Insert the credentials for the
database. If you want to download OMM/XML files from `space-track.org`, you have
to insert the appropriate credentials, too.

### Installation of Python scripts, Jupyter notebooks and dependencies

`satdb` uses [`pipenv`](https://pipenv.pypa.io/) to create and manage a virtualenv environment and keeps track of all the dependencies. Therefore, it is recommended to install pipenv before. In addition, `satdb` uses [Python 3.8](https://www.python.org/).

#### Python scripts

To install the python scripts in a pipenv virtual environment from the Pipfile, execute:

```
$ cd ./scripts/
$ pipenv install
```

Or you can install packages exactly as specified in Pipfile.lock using the sync command:

```
$ cd ./scripts/
$ pipenv sync
```

After installation, you can access the pipenv virtual environment with the following command:

```
$ cd ./scripts/
$ pipenv shell
```

You can also run a Python script using the following command (replace [script] by the name of the appropriate Python script):

```
$ cd ./scripts/
$ pipenv run [script]
```

#### Jupyter notebooks

The installation of the pipenv virtual environment for the Jupyter notebooks is similar to the installation of the Python scripts (see above). Just change to the directory `./notebook/` before executing `pipenv install` or `pipenv sync`. You can then launch Jupyter by:

```
$ pipenv run jupyter notebook
```

### Download TLEs from Celestrak and import into database

Latest TLEs for the last 30 days launches can be downloaded
['here'](https://celestrak.com/NORAD/elements/tle-new.txt) from Celestrak. The data is updates every couple of hours. You can create a cron job and download the files to the above mentioned data directory `~/satdb-downloads/unprocessed`. Now you can run a bash script to import the TLE files in the directory with 
[`tle2db.py`](https://github.com/rzbrk/satdb/blob/master/tle2db.py)
into the database:

```
cd ./scripts/
for file in $(ls ./../data/unprocessed/*.tle)
do
    pipenv run tle2db.py ~/.config/satdb.yaml ${file}
    mv ${file} ./../data/processed/.
done
```

### Download OMM/XML from Space-Track and import into database

Latest OMMs for all active space objects can be downloaded with
[`st_dl_latest.py`](https://github.com/rzbrk/satdb/blob/master/st_dl_latest.py).
You can create a cron job and download the files to the above mentioned data directory `~/satdb-downloads/unprocessed`. Now, you can run a bash script to import the OMM files in the directory with
[`omm2db.py`](https://github.com/rzbrk/satdb/blob/master/omm2db.py)
into the database:

```
cd ./scripts/
for file in $(ls ./../data/unprocessed/*.xml.gz)
do
    pipenv run omm2db.py ~/.config/satdb.yaml ${file}
    mv ${file} ./../data/satdb-downloads/processed/.
done
```


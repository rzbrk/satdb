# satdb

`satdb` is a collection of Python tools and scripts to maintain a local database
for satellite mean orbital elements. The database can be feed from
[CCSDS OMM](https://public.ccsds.org/Pubs/502x0b2c1e2.pdf) or
[TLE](https://en.wikipedia.org/wiki/Two-line_element_set).

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
mysql -u dbuser -D orbdata -p < ./setup/init.sql
```

### Directory structure

I recommend to establish a directory structure for the OMM and TLE files like
the following:

* `~/satdb-downloads/unprocessed/` here you can put all OMM and TLE downloads
  which have still to be imported to the database.
* `~/satdb-downloads/processed/` here you can move all files which are already
  imported to the database. You can access these files at a later time, whenever
  necessary.

### Installation of Python modules and scripts

To install the python modules and scripts execute
[`./setup.py`](https://raw.githubusercontent.com/rzbrk/satdb/master/setup.py):

```
python3 ./setup.py install
```

### Adapt the config file

An example configuration file for `satdb` is provided in the repository:
[`satdb_example.yaml`](https://raw.githubusercontent.com/rzbrk/satdb/master/satdb_example.yaml). Copy this configuration file to a suitable place like `~/.config/satdb.yaml`.

Edit the `satdb` config file `satdb.yaml`. Insert the credentials for the
database. If you want to download OMM/XML files from `space-track.org`, you have
to insert the appropriate credentials, too.
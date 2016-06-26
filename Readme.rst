Simple parser for NWS web forecasts
-----------------------------------

Given a directory with html files scraped from the NWS website, create a text file
for every html file in that directory containing a list of temperture forecasts for the week.

Also write
a single json file with each week stored as an ordered dictionary containing the temperatures
and header information

example::

  python read_forecasts.py /Users/phil/Downloads/archive  -j bondurant.json

The NWS webpage format was changed between 2013 and 2016, use parse_old for the former
and parse_new for the latter

Installation
============

#.  Download and install miniconda version 3.5 from

    http://conda.pydata.org/miniconda.html

    I install into ~/mini35

#.  Make sure that the mini35 python is ahead of any other python on your machine::

      which python
      /Users/phil/mini35/bin/python

#.  Install beautifulsoup::

      conda install beautifulsoup4

#.  Install git from:

    https://git-scm.com/download/mac
      
#.  Clone the repository and cd into it::

      git clone https://github.com/phaustin/nws_parse
      cd nws_parse


Testing
=======

#.  Check the help for the script::

      ~/repos/nws_parse phil@raild% python read_forecasts.py -h
      usage: read_forecasts.py [-h] [-j JSON] directory

      Given a directory with html files scraped from the NWS website, create a text file
      for every html file in that directory containing a list of temperture forecasts for the week.  Also write
      a single json file with each week stored as an ordered dictionary containing the temperatures
      and header information

      example:

      python read_forecasts.py /Users/phil/Downloads/archive  -j bondurant.json

      The NWS webpage format was changed between 2013 and 2016, use parse_old for the former
      and parse_new for the latter

      positional arguments:
      directory             full path to directory with html files

      optional arguments:
      -h, --help            show this help message and exit
      -j JSON, --json JSON  name of json output file. default: temps.json


#.  Run the program on the test data::

      python read_forecasts.py -j bondurant.json  testdata

      json file is set to: testdata/bondurant.json
      processing:  testdata/131011_10.html
      processing:  testdata/131011_22.html
      processing:  testdata/160625_10.html
      processing:  testdata/160625_22.html

#.  Check the output::

      > cat testdata/131011_10.txt  | head
      
      43
      25
      47
      29
      47
      31
      41
      26
      43
      25
      
      > cat testdata/bondurant.json | head -25
      [
      {
        "filename": "testdata/131011_10.html",
        "placename": "9 Miles N Bondurant WY",
        "location": "43.34 deg N 110.43 deg W (Elev. 7049 ft)",
        "last_update": "9:41 am MDT Oct 11, 2013",
        "valid": "11am MDT Oct 11, 2013-6pm MDT Oct 17, 2013",
        "temps": {
            "Today": 43,
            "Tonight": 25,
            "Saturday": 47,
            "Saturday Night": 29,
            "Sunday": 47,
            "Sunday Night": 31,
            "Columbus Day": 41,
            "Monday Night": 26,
            "Tuesday": 43,
            "Tuesday Night": 25,
            "Wednesday": 44,
            "Wednesday Night": 28,
            "Thursday": 45
        }


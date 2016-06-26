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

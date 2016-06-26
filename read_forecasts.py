"""
 Given a directory with html files scraped from the NWS website, create a text file
 for every html file in that directory containing a list of temperture forecasts for the week.  Also write
 a single json file with each week stored as an ordered dictionary containing the temperatures
 and header information

 example:

 python read_forecasts.py /Users/phil/Downloads/archive  -j bondurant.json

 The NWS webpage format was changed between 2013 and 2016, use parse_old for the former
 and parse_new for the latter
"""

from bs4 import BeautifulSoup
import re
from collections import OrderedDict as od
import json
#
# we need to pull the temperature from a string in the form:
# "A 20 percent chance of showers and thunderstorms after noon. Mostly sunny, with a high near 79."
# Assume that the temperature will be integer and always end with a decimal, unlike the chance precip, might have - sign
#
find_temp = re.compile(r".*?([+-]?\d+)\..*?")

def parse_old(soup,filename):
    """
    parse a 2013 era webpage read from file filename

    Parameters
    ----------

    soup:  a beautiful soup object
    filename:  the original html filename (for the metadata)
    
    Returns
    -------

    keep_dict:  an ordered dictionary with metadata and temperature forecasts for the week
    
    """
    keep_dict=od()
    keep_dict['filename'] = filename
    #
    # old format -- metadata and temperatures are stored as unordered lists (ul)
    #
    info = soup.findAll("ul", { "class" : "point-forecast-info" })[0]
    forecast = soup.findAll("ul", { "class" : "point-forecast-7-day" })[0]
    info_list=list(info.find_all("li"))
    line0=list(info_list[0].children)
    line1 = list(info_list[1].children)
    keep_dict['placename'] = line0[-2].strip()
    location = info_list[0].br.text.strip()
    #
    # change unicode degree sign to "deg"
    #
    location = location.replace('\u00b0',' deg ')
    keep_dict['location'] = location
    keep_dict['last_update'] = line1[-1].strip()
    keep_dict['valid'] = info_list[2].contents[1].strip()
    keep_dict['temps'] = od()
    #
    # pull all lines from the forecast list and turn them into integer temps
    # using the find_temp regular expression
    #
    forecast_list=forecast.find_all("li")
    for line in forecast_list:
        match = find_temp.match(line.contents[1])
        keep_dict['temps'][line.span.contents[0]] = int(match.group(1))
    return keep_dict


def parse_new(soup,filename):
    """
    parse a 2016 era webpage read from file filename

    Parameters
    ----------

    soup:  a beautiful soup object
    filename:  the original html filename (for the metadata)
    
    Returns
    -------

    keep_dict:  an ordered dictionary with metadata and temperature forecasts for the week
    
    """
    keep_dict=od()
    keep_dict['filename'] = filename
    #
    # get the metadata from the right column of the "about_forecast" table
    #
    info = soup.findAll("div", { "id" : "about_forecast" })
    lines=list(info[0].children)
    location=lines[1].findAll('div', {"class" : "right"})
    placename,latlon = list(location[0].children)
    keep_dict['placename'] = placename.strip()
    latlon = latlon.text.strip()
    #
    # change unicode degree sign to "deg"
    #
    latlon = latlon.replace('\u00b0',' deg ')
    keep_dict['location'] = latlon
    update=lines[3].findAll('div', {"class" : "right"})
    keep_dict['last_update'] = update[0].text.strip()
    valid=lines[5].findAll('div', {"class" : "right"})
    keep_dict['valid'] = valid[0].text.strip()
    #
    # get the days and temps from two columns of the forecast table
    #
    forecast_times=soup.findAll('div', {"class" : "col-sm-2 forecast-label"})
    forecast_temps=soup.findAll('div', {"class" : "col-sm-10 forecast-text"})
    keep_dict['temps'] = od()
    for the_time,the_temp in zip(forecast_times,forecast_temps):
        match = find_temp.match(the_temp.text)
        keep_dict['temps'][the_time.b.text] = int(match.group(1))
    return keep_dict

def dump_text(filename,the_dict):
    """
      given an ordered dictionary the_dict, dump its temperatures
      into the file filename
    """
    with open(filename,'w') as f:
        for the_temp in the_dict['temps'].values():
            f.write("{:d}\n".format(the_temp))

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    
    linebreaks=argparse.RawTextHelpFormatter
    descrip=__doc__.lstrip()
    parser = argparse.ArgumentParser(formatter_class=linebreaks,description=descrip)
    parser.add_argument("directory",type=str,help='full path to directory with html files')
    parser.add_argument('-j','--json',type=str,help='name of json output file. default: temps.json',default='temps.json')
    args = parser.parse_args()
    #
    # use pathlib objects to manipulate the html and txt filenames
    #
    working_dir = Path(args.directory)
    #
    # get any file ending in html
    #
    files = working_dir.glob('*.html')
    #
    # write the json file to the working directory
    #
    out_json = working_dir.joinpath(args.json)
    print('json file is set to: {}'.format(out_json))
    weeklist=[]
    for the_file in files:
        htmlfile=str(the_file)
        print('processing: ',htmlfile)
        #
        # give the txt file the same root as the html file
        #
        out_file=str(the_file.parent.joinpath(the_file.stem + '.txt'))
        with open(str(htmlfile),'r') as f:
            all_lines=f.read()
            soup=BeautifulSoup(all_lines,'html.parser')
            try:
                keep_dict = parse_old(soup,htmlfile)
            except IndexError:
                keep_dict = parse_new(soup,htmlfile)
        weeklist.append(keep_dict)
        dump_text(out_file,keep_dict)
    with open(str(out_json),'w') as f:
        json.dump(weeklist,f,indent=4)
    



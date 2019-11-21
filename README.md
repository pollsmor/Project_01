# Space Explorer by Quaternary Star System

**Roster/Roles**
- Elizabeth Doss
  - Handle API requests cleanly
- Yevgeniy Gorbachev
  - Handle the backend
  - Handle caching in database
  - Search through database
  - Generate queries using natural language input
  - Math
- Kevin Li
  - Project manager
  - Make changes to repository when necessary
- Emory Walsh
  - Handle the frontend
  - Create templates
  - Routing
  - Styling with Bootstrap

## Website Description
Data is fetched from the [SpaceX API](https://github.com/r-spacex/SpaceX-API), [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page), and the [NASA Exoplanet API](https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html).

This website will (hopefully) provide information and answer questions the visitor may have regarding spacecraft, engines, space travel, exoplanets, etc. A search query is taken in from the user. The website parses the query for keywords, then parses the three APIs as appropriate for information relating to the search, and feeding it back to the user. Searches not containing keywords will error out. 

The amount of APIs searched through depends on the keywords.
Something like “how long to reach {{exoplanet}} with SpaceX Falcon 9” will work like this:
  - Search exoplanets API for the planet
  - Search Wikipedia API for the engine/rocket
  - Use the data gathered from the two above APIs to send an equation to Wolfram|Alpha
  - Return the result.
  
Meanwhile, a query like “stat[istic]s for {planet, rocket engine}” will just get a result from the exoplanets API or Wikipedia API respectively. 

## Instructions for running this project

**Dependencies**

You must install the pip3 modules listed in the /doc/requirements.txt file. To do so, install them in a Terminal with:
```bash
pip install -r <location of requirements.txt file>
```

The -r flag is necessary to distinguish it from a typical pip install. Without the -r, pip will look for a package online called "requirements.txt". That is obviously not desirable. 

Note that on certain systems (like the school computers), the pip3 command may be restricted. To get around this, create a virtual environment with:
```bash
python3 -m venv <name_of_venv>
```
*Note that if your system only has Python 3 installed, just remove the 3 from the above command.*

To activate the virtual environment, cd into the directory you created the environment in, and run the "activate" file. Now, you should be able to pip3 install and run Python files that utilize modules installed via pip3. To deactivate the environment, run the "deactivate" file.  

**Run the program**

After installing the required dependencies, all you need to do to run the program is to type into a terminal session: 
```bash
python3 app.py
```
*Again, remove the 3 after the "python" if necessary.*

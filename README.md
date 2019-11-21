# Shipbuilder's Guide to the Galaxy by Quaternary Star System

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
Data is fetched from the [Wolfram|Alpha API](https://docs.google.com/document/d/1GLX_8-HKjzI7kHLleQikTbWZ0orXhYVnabveE6T6J8M), [Wikipedia API](https://docs.google.com/document/d/1KNf_h_Rysiftc88uZNZO4LMpAyQprUTSj-eg5CMz9a8), and the [NASA Exoplanet API](https://docs.google.com/document/d/1J5PAzkRvPBrzud4jhXBX3yZZtMhlTx1KmLQezlLszEk).

This website will (hopefully) provide information and answer questions the visitor may have regarding spacecraft, engines, space travel, exoplanets, etc. A search query is taken in from the user. The website parses the query for keywords, then parses the three APIs as appropriate for information relating to the search, and feeding it back to the user. Searches not containing keywords will error out. 

The amount of APIs searched through depends on the keywords.
Something like “how long to reach {{exoplanet}} with SpaceX Falcon 9” will work like this:
  - Search exoplanets API for the planet
  - Search Wikipedia API for the engine/rocket
  - Use the data gathered from the two above APIs to send an equation to Wolfram|Alpha
  - Return the result.
  
Meanwhile, a query like “stat[istic]s for {planet, rocket engine}” will just get a result from the exoplanets API or Wikipedia API respectively. 

## Instructions for running this project

**Cloning**

First, procure the ability to run Git commands. 

- On Windows: Install [Git Bash](https://github.com/git-for-windows/git/releases/download/v2.24.0.windows.2/Git-2.24.0.2-64-bit.exe).

- On macOS: Use the [git-osx-installer](https://sourceforge.net/projects/git-osx-installer/files/git-2.23.0-intel-universal-mavericks.dmg/download?use_mirror=autoselect). If you have XCode installed on your machine, you may already have Git functionality. 

- On Linux (preferably an Ubuntu based distribution): you already have Git! 

Now, you can clone this repo. To do so, type into a terminal session:
```bash
git clone https://github.com/pollsmor/Project_01.git
```

The project repo should then clone into whatever folder you ran the clone command in. 

**Dependencies**

You must install the pip modules listed in the /doc/requirements.txt file. To do so, install them in a Terminal with:
```bash
pip install -r <location of requirements.txt file>
```

The -r flag is necessary to distinguish it from a typical pip install. Without the -r, pip will look for a package online called "requirements.txt". That is obviously not desirable. 

Note that on certain systems (like the school computers), the pip command may be restricted. To get around this, create a virtual environment with:
```bash
python3 -m venv <name_of_venv>
```
*Note that if your system only has Python 3 installed, just remove the 3 from the above command.*

To activate the virtual environment, cd into the directory you created the environment in, and run the "activate" file. Now, you should be able to pip install the requirements. To deactivate the environment, run the "deactivate" file.  

**Run the program**

After installing the required dependencies, all you need to do to run the program is to type into a terminal session: 
```bash
python3 app.py
```
*Again, remove the 3 after the "python" if necessary.*

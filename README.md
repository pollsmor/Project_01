# Space Explorer by Quaternary Star System

**Roster/Roles**
- Elizabeth Doss
  - Connect frontend/backend
  - Write methods that can access each API and return the desired information
- Yevgeniy Gorbachev
  - Handle the backend
  - Handle caching in database
  - Search through database
  - Generate queries using natural language input
- Kevin Li
  - Project manager
  - Make changes to repository when necessary
- Emory Walsh
  - Handle the frontend
  - Create templates
  - Routing
  - Styling with Bootstrap

## Website Description
Data is fetched from the [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page), the [NASA Exoplanet API](https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html), and the [Wolfram|Alpha API](http://products.wolframalpha.com/api/).

This website will (hopefully) provide information and answer questions the visitor may have regarding spacecraft, engines, space travel, exoplanets, etc. A search query is taken in from the user. The website parses the query for keywords, then parses the three APIs as appropriate for information relating to the search, and feeding it back to the user. Searches not containing keywords or erroneous queries will error out. 

The amount of APIs searched through depends on the keywords.
Something like “how long to reach {{exoplanet}} with SpaceX Falcon 9” will work like this:
  - Search exoplanets API for the planet
  - Search Wikipedia API for the engine/rocket
  - Use the data gathered from the two above APIs to send an equation to Wolfram|Alpha
  - Return the result.

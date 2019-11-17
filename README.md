# Space Explorer by Quaternary Star System

**Roster/Roles**
- Elizabeth Doss
  - PLACEHOLDER
  - PLACEHOLDER
  - PLACEHOLDER
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
This website will (hopefully) provide information and answer questions the visitor may have regarding spacecraft, engines, space travel, exoplanets, etc. A search query is taken in from the user. The website parses the query to see if keywords like **time to reach Proxima Centauri b** exist, then parsing three APIs for information relating to the search, and feeding it back to the user. Searches not containing keywords will error out. 

Data is fetched from the [SpaceX API](https://github.com/r-spacex/SpaceX-API), [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page), and the [NASA Exoplanet API](https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html).

A list of searched items will be served to the user, who can choose to click on one of them, rendering a dedicated page for that search item with more detailed info. 

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
This website will (hopefully) provide information and answer questions the visitor may have regarding spacecraft, engines, space travel, exoplanets, etc. A search query is taken in from the user. The website first parses the query to see if keywords like **time** exist, which will help speed up operation of the website by refraining from accessing all three APIs. 

Data is fetched from the [SpaceX API](https://github.com/r-spacex/SpaceX-API), [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page), and the [NASA Exoplanet API](https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html).

**Examples of search queries**
- "**how long** to reach Proxima Centauri b on a SpaceX Falcon 9" - only searches the WolframAlpha API
- "Proxima Centauri b" - no keyword found, search all three APIs. 
- "Proxima Centauri b **exoplanet**" - only searches the NASA Exoplanets API

A list of searched items will be served to the user, who can choose to click on one of them, rendering a dedicated page for that search item with more detailed info. The search results will be split into three categories: spacecraft/engines, space travel, and exoplanets. 

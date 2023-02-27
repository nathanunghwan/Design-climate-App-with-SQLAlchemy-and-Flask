# Design-climate-App-with-SQLAlchemy-and-Flask
- I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii. To help with my trip planning, I decide to do a climate analysis about the area.
***
## Analyze and Explore the Climate Data
***
### 1. Database connection
- Use the SQLAlchemy create_engine() function to connect to my SQLite database.
- Use the SQLAlchemy automap_base() function to reflect my tables into classes, and then save references to the classes named station and measurement.
- Link Python to the database by creating a SQLAlchemy session.

### 2. Precipitation Analysis
- Find the most recent date in the dataset.
- Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
- Select only the "date" and "prcp" values.
- Load the query results into a Pandas DataFrame, and set the index to the "date" column.
- Sort the DataFrame values by "date".
- Plot the results by using the DataFrame plot method
<img
  src=".\SurfsUp\Images\Precipitation in Hawaii.png"
  width="600"
  height="400"
/>"

### 3. Station Analysis
- Design a query to calculate the total number of stations in the dataset.
- Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
> + (1) List the stations and observation counts in descending order.
> + (2) Answer the following question: which station id has the greatest number of observations?

- Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
- Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:
> + (1) Filter by the station that has the greatest number of observations.
> + (2) Query the previous 12 months of TOBS data for that station.
> + (3) Plot the results as a histogram with bins=12
<img
  src=".\SurfsUp\Images\Temperatures Observation.png"
  width="600"
  height="400"
/>"
***
## Design My Climate App
***
I designed a Flask API based on the queries. To do so, used Flask to create my routes as follows:

 1. /
 - Start at the homepage.<br>
 - List all the available routes.

 2. /api/v1.0/precipitation
 - Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.<br>
 - Return the JSON representation of your dictionary.
<img
  src="SurfsUp\Images\api_precipitation.png"
  width="600"
  height="400"
/>

 3. /api/v1.0/stations
 - Return a JSON list of stations from the dataset.
<img
  src="SurfsUp\Images\api_stations.png"
  width="600"
  height="400"
/>

 4. /api/v1.0/tobs
 - Query the dates and temperature observations of the most-active station for the previous year of data.<br>
 - Return a JSON list of temperature observations for the previous year.
<img
  src="SurfsUp\Images\api_tobs.png"
  width="600"
  height="400"
/>

 5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
 - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.<br>
 - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.<br>
 - For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
 <img
  src="SurfsUp\Images\api_temp_start.png"
  width="400"
  height="200"
/>
<img
  src="SurfsUp\Images\api_temp_start_end.png"
  width="400"
  height="200"
/>


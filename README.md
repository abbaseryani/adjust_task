# adjust_task

This repository is intended to create an API for the Home Task for Adjust.

This API is written using Flask and the database is SQLite.

The API is capable of filtering, grouping and sorting.

Following an example to access the API:

http://127.0.0.1:5000/performance-api?select=channel,country,sum(impressions)%20as%20impressions,sum(clicks)%20as%20clicks&where=date%3C=%272017-06-01%27&groupby=channel,%20country%20&orderby=clicks

I called the API "performance-api".

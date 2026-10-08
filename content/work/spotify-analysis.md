---
{"title":"Spotify Listening History","slug":"spotify-analysis","category":"Data · Independent exploration","description":"Turning a Spotify data export into a closer look at listening habits, favorite artists, and patterns over time.","tools":["Python","pandas","Matplotlib","Folium"],"status":"Python project"}
---
## A closer look at listening habits

Spotify's extended listening history contains more than a list of songs. It records when a track played, how long it played, and the platform used. I built a Python program to bring those records together and explore what changes over time.

## What the program does

The program combines JSON exports into a single dataset and calculates total listening time, most-played artists and tracks, and platform usage. It also produces monthly activity charts and ranked artist and track plots.

An optional mapping step uses IP geolocation to create full and clustered maps of approximate streaming locations.

## Tools and approach

pandas handles the data preparation and summaries. Matplotlib turns the results into charts. GeoIP2 and Folium support the optional location analysis and maps.

The program runs locally with a Spotify extended streaming-history export. The mapping step also needs a GeoLite2 database. File paths in the script should be adjusted to match your setup.

## What to keep in mind

Minutes played can reveal patterns, but they are not a complete measure of taste or attention. IP-based locations are approximate, and listening exports can contain sensitive personal information. Keeping the analysis on your own machine gives you control over the underlying data.

## Explore the project

- [Read or download the Python program](/lab/spotify-source/)
- [View the project on GitHub](https://github.com/eshaanarora99/Spotify_Data_Analysis)

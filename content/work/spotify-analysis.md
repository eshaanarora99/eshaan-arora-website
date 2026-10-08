---
{"title":"Spotify Listening History","slug":"spotify-analysis","category":"Data · Independent exploration","description":"A local Python workflow for exploring listening patterns, artists, tracks, and approximate streaming locations.","tools":["Python","pandas","Matplotlib","Folium"],"status":"Source available"}
---
## Overview and question

What can an extended Spotify listening-history export reveal about listening patterns? The existing program combines JSON exports, summarizes play time, and produces plots and maps on a local machine.

## My contribution

The website contains a Python implementation linked to the Spotify Data Analysis repository. The code aggregates listening records and defines statistics, time-series plots, artist and track summaries, and GeoIP map generation.

## Tools and implementation

pandas handles tabular data, Matplotlib produces monthly activity and ranking plots, and GeoIP2 with Folium generates full and clustered maps. Inputs are Spotify's extended streaming-history JSON files and a separately obtained GeoLite2 database. The original script contains machine-specific paths that must be adjusted.

## Results

The source implements the analyses, but no exported results or dataset are included in this website checkout. No personal listening statistics are inferred or published.

## Limitations

Play time is different from preference or attention. IP geolocation is approximate, and an export can contain sensitive location and listening information. Missing fields and empty inputs need validation before general use. This is a local program, not a deployed browser explorer.

## Resources

- [View preserved Python source](/lab/spotify-source/)
- [Original repository](https://github.com/eshaanarora99/Spotify_Data_Analysis)

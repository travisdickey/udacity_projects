
# Wrangle OpenStreetMap Data

## Map Area

Savannah, GA - Hilton Head, SC, United States

[https://mapzen.com/data/metro-extracts/your-extracts/4f8284861e2a](https://mapzen.com/data/metro-extracts/your-extracts/4f8284861e2a)

I am from a small town just outside of Savannah and not far from Hilton Head. I was interested to see what the OSM data would reveal about this somewhat quaint and quirky coastal region. The map linked above includes all of Chatham County, where Savannah is located, and major portions of neighbroing counties Effingham, Bryan, Jasper, and Beaufort. Hilton Head, a popular tourist destination, is a part of Beaufort County, which is also well-known as the home of Parris Island, where Marines go for boot camp.

## Problems Encountered
- Street names often abbreviated.
- A few zip codes contained double entries separated by a semi-colon, others separated by a colon, and some contained a state abbreviation (GA or SC).
- Lack of Standard Data:
    - Large portion of tags created by Tiger GPS and GNIS, which take quite different formats from the standard entries. For example, in this dataset, 13,569 zip codes were entered by Tiger vs. 514 by standard entry.
    - Incomplete data. For example, a query for types of 'cuisine' revealed just four seafood restaurants. This is a coastal region. There are most definitely more than four seafood restaurants.
    - Very few standard entries reference the county in which a tag occurs, making comparisons by county quite difficult. For example, Effingham County, where I grew up, contains 47 distinct entries, 46 of those were imported from GNIS.

## Street Names

To fix street names, I lifted the `update_name` function from the `audit.py` file in the case study, modified it slightly, and created a new file called `update_street.py`, then added keys to the mapping dictionary for all the entries in the "expected" list (Ct, Blvd, Pl, etc.).
```python
def update_name(name, mapping):
    match = street_type_re.search(name)
    if match:
        street_type = match.group()
        if street_type not in expected:
            if street_type in mapping.keys():
                abbrev = match.group()
                l = len(abbrev)
                name = name[:-l] + mapping[abbrev]
    return name
```

## Incorrect Zip Codes

The zip codes in my datafile were generally clean, although I did have a few entries that with two zip codes separated by a semi-colon, some with hyphenated zip codes, and a few with a state abbreviation at the beginning, such as '(GA)  31341'. Adding the following code to my `shape_element` function fixed the problem.
```python
elif a['key'] == 'postcode' or a['key'].find('zip') != -1:
    z_re = re.compile(r'\d{5}')
    z = tag.attrib['v']
    zipcode = z_re.findall(z)[0]
    a['value'] = zipcode #correct zip codes such as [(GA)   31326, 31326-3123, 31326; 31409]
```

## Lack of Standard Data

### Tiger GPS & GNIS

#### Tiger
There are a number of differences between the Tiger GPS format in the SQL tables and the standard format. While I really wanted to correct the discrepancies, a search of the Udacity forums, the web, and GitHub suggested that the data would be better left as-is.

The following shows the format of Tiger GPS data:
```sql
SELECT *, COUNT(*) as count
   FROM ways_tags
   WHERE type='tiger'
   GROUP BY key
   ORDER BY count
   DESC LIMIT 5;

357833033|cfcc|A41|tiger|114
357833033|county|Beaufort, SC|tiger|113
357833033|reviewed|no|tiger|106
357833033|name_base|Mead|tiger|89
357833033|name_type|Ln|tiger|83
357833033|zip_left|29926|tiger|50
```
Thus, for addresses, rather than having the `type` listed as `addr` and `key` equal to `street`, the Tiger data takes `tiger` as its type and for streets uses the keys `name_base` and `name_type`, separating the street name and street type in two rows.

#### GNIS

An example of the GNIS format:
```sql
491501125|feature_id|1694582|gnis|1660
488367267|created|07/13/1980|gnis|1208
488367267|county_id|013|gnis|1129
488367267|state_id|45|gnis|1129
646947567|id|1253484|gnis|322
```
Again, different key names, values, etc., from the standard format, which makes meaningful queries quite challenging.

### Incomplete Data

#### Where's the Seafood?
The query below reveals large gaps in the data:
```sql
SELECT nodes_tags.value, COUNT(*) as num
    FROM nodes_tags
        JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
        ON nodes_tags.id=i.id
    WHERE nodes_tags.key='cuisine'
    GROUP BY nodes_tags.value
    ORDER BY num DESC LIMIT 10;
    
american|5
mexican|5
pizza|5
burger|4
seafood|4
french|2
japanese|2
regional|2
Potato_Dishes|1
asian|1
```
There are most definitely more than four seafood restaurants in this coastal area.

#### Dubious Results
The lack of a standard format leaves query results that are quite dubious. The query for cities:
```sql
SELECT tags.value, COUNT(*) as count
    FROM (SELECT * FROM nodes_tags UNION ALL
          SELECT * FROM ways_tags) tags
    WHERE tags.key LIKE '%city'
    GROUP BY tags.value
    ORDER BY count DESC;
```
Yields the following, edited for clarity:
```sql
Savannah|893
Pooler|168
Bluffton|139
Hilton Head Island|88
Beaufort|25
Richmond Hill|6
Tybee Island|5
Bloomingdale|3
Hardeeville|2
Port Royal|2
Ridgeland|2
Black Creek|1
Daufuskie Island|1
Ellabell|1
Meldrim|1
Okatie|1
Pembroke|1
Rincon|1
Springfield|1
```
Rincon, Richmond Hill, Bloomingdale, Okatie, Hardeeville are all towns with around 10,000 people. The number of entries displayed is quite disproportional to that of Savannah, which has a population of about 147,000.

#### Lack of County Reference
I had hoped to compare data across the five counties. However, only the GNIS and Tiger data reference the county for each tag. The standard data does not, aside from a single tag for the county itself. Therefore, queries to compare one county to another lack sufficient data to be meaningful. Below are the total entries by county. Comparing this to the "City" search above, with 893 tags for Savannah alone, highlights the lack of county data.  
```sql
 SELECT tags.value, COUNT(*) AS count 
 FROM (SELECT * FROM nodes_tags 
     UNION ALL SELECT * FROM ways_tags) tags 
 WHERE tags.value='Chatham' 
     OR tags.value='Effingham' 
     OR tags.value='Bryan' 
     OR tags.value='Jasper' 
     OR tags.value='Beaufort'
 GROUP BY tags.value 
 ORDER BY count DESC;
 
Chatham|288
Beaufort|217
Jasper|83
Effingham|47
Bryan|26
```

An example of the data from one county, suburban Effingham, with 46 out of 47 entries from GNIS:
```sql
SELECT *, COUNT(*) AS count 
  FROM (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) tags 
  WHERE tags.value='Effingham' 
  GROUP BY tags.key 
  ORDER BY count desc;
  
154396154|gnis:County|Effingham|regular|25
192417778|county_name|Effingham|gnis|21
316949458|name|Effingham|regular|1
```
Not only do the GNIS entries make up most of the data, but the GNIS entries themselves are inconsistent, with the key 'gnis:County' in some cases and 'county_name' in others.

## Data Overview and Additional Thoughts

### File Sizes
```
nodes.csv .......................  58.8 MB
nodes_tags.csv ..................   1.1 MB
osm.db ..........................  83.8 MB
savannah_hiltonhead.osm ......... 148.7 MB
ways.csv ........................   3.6 MB
ways_nodes.csv ..................  20.9 MB
ways_tags.csv ...................   9.8 MB
```

### Number of Nodes

```sql
SELECT COUNT(*) FROM nodes;

737115
```

### Number of Ways
```sql
SELECT COUNT(*) FROM ways;

63054
```

### Number of Unique Users
```sql
SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;

498
```

### Ten Most Popular Amenities
```sql
SELECT tags.value, COUNT(*) AS count 
  FROM (SELECT * FROM nodes_tags 
      UNION ALL SELECT * FROM ways_tags) tags 
  WHERE tags.key='amenity' 
  GROUP BY tags.value 
  ORDER BY count DESC LIMIT 10;
   
place_of_worship|521
parking|325
school|250
restaurant|153
grave_yard|125
fast_food|65
fuel|54
bench|44
fire_station|38
fountain|35
```

### Religion
Again, data is incomplete. Below is not a fair representation of religion in this area.
```sql
SELECT nodes_tags.value, COUNT(*) as num
    FROM nodes_tags
        JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
        ON nodes_tags.id=i.id
    WHERE nodes_tags.key='religion'
    GROUP BY nodes_tags.value
    ORDER BY num DESC;
    
christian|466
jewish|3
```
I am aware of places of worship from different faiths that do not show up in this data.

### Sport
```sql
SELECT tags.value, COUNT(*) AS count 
  FROM (SELECT * FROM nodes_tags 
          UNION ALL 
        SELECT * FROM ways_tags) tags 
  WHERE tags.key='sport' 
  GROUP BY tags.value 
  ORDER BY count DESC;

tennis|192
baseball|86
golf|36
soccer|28
swimming|7
basketball|6
american_football|3
multi|3
athletics|1
bocce|1
fitness|1
football|1
motor|1
running|1
shuffleboard|1
```
As with other amenities, the data for sports fields is lacking. For example, football is extremely popular in the area, but the data lists only four football fields.

## Additional Thoughts

Given that the data for amenities and places of interest is lacking, one possible solution for this problem would be to use family photos. For example, my wife has 10s of thousands of pictures that she has taken over the years using her cell phone. As our family has visited the various places throughout our community and beyond, she has documented it all with cell phone pictures. It would not be overly difficult to get the EXIF information from the photos, then supply the key, value, and type information that goes along with it and upload it to OpenStreetMap. OpenStreetMap's 'how-to guide' section on this [page](http://wiki.openstreetmap.org/wiki/Recording_GPS_tracks) gives a brief description of how to do that.

One benefit of this method would be that it is a relatively economical way to get data for lots of different places. It would only take a handful of mothers with similar troves of family photos to document the majority of places in my community. One problem, though, is that it would be pretty tedious to pore over thousands and thousands of photos and identify the names and types of amenity. However, people might be willing to supply the information in some type of online form along with the photos, so that the tag information could be linked programmatically before uploading to OpenStreetMap. Facebook would be a good place to recruit people for this. 

Another problem with this method would be that some of the data would be outdated, for example, an old photo from a restaurant that no longer exists. It would be tedious to verify whether the places still exist; however, again it would be possible to have the people supplying the photos provide that type of information.  

## Conclusion
The OpenStreetMap is a fascinating project. It was a pleasure poring over the data for the region where I have lived and worked the majority of my life. While my biggest takeaway is that much work needs to be done to standardize the data for meaningful queries, my interest is piqued, and it makes me want to contribute to the OpenStreetMap for my community. With a more robust `data.py`, it would be possible to clean and standardize the Tiger GPS and GNIS data so that it fits the standard format, which would greatly enhance the usefulness of running queries. Also, with some creative problem solving, such as using the EXIF information from family photos, it would be possible to fill in large gaps in the data, which would also make SQL queries far more meaningful.   

## References
- Many of the SQL queries and ideas for basic layout of this report are courtesy of the Udacity [sample project](https://gist.github.com/carlward/54ec1c91b62a5f911c42#file-sample_project-md) created by Carl Ward.
- Much of the code for auditing, cleaning, and writing data to SQL was derived from the Udacity OSM Case Study (as was suggested to do).
- The file `to_sql_nodes_tags.py` was taken from a Udacity [forum](https://discussions.udacity.com/c/nd002-data-wrangling) post by Udacity moderator Myles Callan; this code was then adapted to create the other `.py` files for converting CSVs to SQL.
- Many visits to [stackoverflow](https://stackoverflow.com/) for a variety of questions; site was particularly helpful with calling functions and files from one `.py` file into another.

DROP TABLE IF EXISTS schools.school_location_2015;
CREATE TABLE schools.school_location_2015
AS
SELECT survyear survey_year
, ncessch nces_id
, fipst 
, lstree address1
, lcity city
, lstate state
, lzip zip
 
, latcode lat
, longcode lon
, conum county_fips_id
, coname county_name
, cd 
, locale 
, csa 
, cbsa 
, necta 
, metmic 
, ST_GeomFromText('POINT('|| longcode || ' ' || latcode || ')', 4269)::geometry(point,  4269) geom_centroid
FROM schools.school_location_import_2015
;


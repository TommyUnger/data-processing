BEGIN;
DROP TABLE IF EXISTS "schools"."school_district";
CREATE TABLE "schools"."school_district" (gid serial,
"statefp" SMALLINT,
"scsdlea" INT,
"geoid" INT,
"name" varchar(100),
"lsad" INT,
"lograde" SMALLINT,
"higrade" SMALLINT,
"mtfcc" varchar(5),
"sdtyp" varchar(1),
"funcstat" varchar(1),
"aland" float8,
"awater" float8,
"intptlat" varchar(11),
"intptlon" varchar(12));
SELECT AddGeometryColumn('schools','school_district','geom','4269','MULTIPOLYGON',2);
CREATE INDEX "school_district_geom_gist" ON "schools"."school_district" USING GIST ("geom");
COMMIT;
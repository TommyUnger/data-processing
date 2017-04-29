DROP TABLE IF EXISTS schools.school_district_import;

CREATE TABLE schools.school_district_import
(
  gid serial NOT NULL,
  statefp character varying(2),
  unsdlea character varying(5),
  geoid character varying(7),
  name character varying(100),
  lsad character varying(2),
  lograde character varying(2),
  higrade character varying(2),
  mtfcc character varying(5),
  sdtyp character varying(1),
  funcstat character varying(1),
  aland double precision,
  awater double precision,
  intptlat character varying(11),
  intptlon character varying(12),
  geom geometry(MultiPolygon,4269),
  CONSTRAINT school_district_import_pkey PRIMARY KEY (gid)
);
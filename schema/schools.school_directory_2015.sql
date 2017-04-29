DROP TABLE IF EXISTS schools.school_directory_2015;
CREATE TABLE schools.school_directory_2015
AS
SELECT *
, grade_pre_k + grade_k grade_prek_and_k
, grade1 + grade2 + grade3 + grade4 + grade5 grade_elem
, grade6 +grade7 + grade8 grade_middle_school
, grade9 + grade10 + grade11 + grade12 grade_hs
FROM
(
SELECT 
left(survyear, 4)::INT survey_year 
, fipst 
, leaid 
, st_leaid state_leait 
, lea_name school_district_name 
, schid school_id 
, st_schid state_school_id 
, ncessch nces_id 
, sch_name school_name  
, phone 
, lstreet1 address1
, lstreet2 address2
, lcity city
, lstate state
, lzip zip
, "union" is_union
, CASE WHEN out_of_state_flag='Y' THEN 1 ELSE 0 END out_of_state_flag
, sch_type_text school_type
, sch_type school_type_id
, recon_status 
, CASE WHEN gslo ~* '[0-9]+' THEN gslo ELSE NULL END::SMALLINT low_grade
, CASE WHEN gshi ~* '[0-9]+' THEN gshi ELSE NULL END::SMALLINT high_grade
, "level" 
, virtual 
, bies 
, sy_status_text 
, sy_status 
, updated_status_text 
, updated_status 
, to_date(effective_date, 'DDMonYYYY:HH24:MI:SS') effective_date 
, replace(charter_text, 'Not Applicable', '') charter
, CASE WHEN pkoffered='Y' THEN 1 ELSE 0 END grade_pre_k
, CASE WHEN kgoffered='Y' THEN 1 ELSE 0 END grade_k
, CASE WHEN g1offered='Y' THEN 1 ELSE 0 END grade1
, CASE WHEN g2offered='Y' THEN 1 ELSE 0 END grade2
, CASE WHEN g3offered='Y' THEN 1 ELSE 0 END grade3
, CASE WHEN g4offered='Y' THEN 1 ELSE 0 END grade4
, CASE WHEN g5offered='Y' THEN 1 ELSE 0 END grade5
, CASE WHEN g6offered='Y' THEN 1 ELSE 0 END grade6
, CASE WHEN g7offered='Y' THEN 1 ELSE 0 END grade7
, CASE WHEN g8offered='Y' THEN 1 ELSE 0 END grade8
, CASE WHEN g9offered='Y' THEN 1 ELSE 0 END grade9
, CASE WHEN g10offered='Y' THEN 1 ELSE 0 END grade10
, CASE WHEN g11offered='Y' THEN 1 ELSE 0 END grade11
, CASE WHEN g12offered='Y' THEN 1 ELSE 0 END grade12
, CASE WHEN g13offered='Y' THEN 1 ELSE 0 END grade13
, CASE WHEN aeoffered='Y' THEN 1 ELSE 0 END  aeoffered
, CASE WHEN ugoffered='Y' THEN 1 ELSE 0 END  ugoffered
, CASE WHEN nogrades='Y' THEN 1 ELSE 0 END nogrades
, replace(chartauth1, 'NOT APPLICABLE', '') chartauth1
, replace(chartauthn1, 'NOT APPLICABLE', '') chartauthn1
, replace(chartauth2, 'NOT APPLICABLE', '') chartauth2
, replace(chartauthn2, 'NOT APPLICABLE', '') chartauthn2
, igoffered 
FROM schools.school_directory_import_2015
) t;

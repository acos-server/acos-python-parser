# Python parser

This Acos server tool parses Python 3 code and
returns the found concepts by traversing the AST
of the code.


## Requires
Python==3.9.22

## To run frontend
python3.9 -m streamlit run streamlit_main.py

## To run API
python3.9 -m uvicorn main_api:app --reload-include="main_api.py" --reload-exclude="*/py-files/*"

## Deployment on PAWSComp

```
sudo su
source setup_docker.sh
exit
```

Then to test

```
source test_docker.sh
```

Expected output:
```
[{"aggregate_id":{},"um2_activity_id":{},"aggregate_content_name":"tmp1","um2_concept_id":{},"aggregate_component_name":"Import","aggregate_context_name":"Import","aggregate_domain":"py","um2_aggregate_weight":1,"aggregate_active":1,"um2_direction":0,"aggregate_source_method":"Arun Parser v0.3","um2_concept_description":"Arun Parser v0.3","importance":0,"contributesK":0},{"aggregate_id":{},"um2_activity_id":{},"aggregate_content_name":"tmp1","um2_concept_id":{},"aggregate_component_name":"Alias","aggregate_context_name":"Alias","aggregate_domain":"py","um2_aggregate_weight":1,"aggregate_active":1,"um2_direction":0,"aggregate_source_method":"Arun Parser v0.3","um2_concept_description":"Arun Parser v0.3","importance":0,"contributesK":0}]
[{"aggregate_id":{},"um2_activity_id":{},"aggregate_content_name":"tmp1","um2_concept_id":{},"aggregate_component_name":"Import","aggregate_context_name":"Import","aggregate_domain":"py","um2_aggregate_weight":1,"aggregate_active":1,"um2_direction":0,"aggregate_source_method":"Arun Parser v0.3","um2_concept_description":"Arun Parser v0.3","importance":0,"contributesK":0},{"aggregate_id":{},"um2_activity_id":{},"aggregate_content_name":"tmp1","um2_concept_id":{},"aggregate_component_name":"Numeric-or-string-or-collection-assignment","aggregate_context_name":"Numeric-or-string-or-collection-assignment","aggregate_domain":"py","um2_aggregate_weight":1,"aggregate_active":1,"um2_direction":0,"aggregate_source_method":"Arun Parser v0.3","um2_concept_description":"Arun Parser v0.3","importance":0,"contributesK":0},{"aggregate_id":{},"um2_activity_id":{},"aggregate_content_name":"tmp1","um2_concept_id":{},"aggregate_component_name":"Int","aggregate_context_name":"Int","aggregate_domain":"py","um2_aggregate_weight":1,"aggregate_active":1,"um2_direction":0,"aggregate_source_method":"Arun Parser v0.3","um2_concept_description":"Arun Parser v0.3","importance":0,"contributesK":0},{"aggregate_id":{},"um2_activity_id":{},"aggregate_content_name":"tmp1","um2_concept_id":{},"aggregate_component_name":"Alias","aggregate_context_name":"Alias","aggregate_domain":"py","um2_aggregate_weight":1,"aggregate_active":1,"um2_direction":0,"aggregate_source_method":"Arun Parser v0.3","um2_concept_description":"Arun Parser v0.3","importance":0,"contributesK":0}]
[{"aggregate_id":{},"um2_activity_id":{},"aggregate_content_name":"tmp1","um2_concept_id":{},"aggregate_component_name":"Numeric-or-string-or-collection-assignment","aggregate_context_name":"Numeric-or-string-or-collection-assignment","aggregate_domain":"py","um2_aggregate_weight":1,"aggregate_active":1,"um2_direction":0,"aggregate_source_method":"Arun Parser v0.3","um2_concept_description":"Arun Parser v0.3","importance":0,"contributesK":0}]
[{"aggregate_id":{},"um2_activity_id":{},"aggregate_content_name":"tmp1","um2_concept_id":{},"aggregate_component_name":"Numeric-or-string-or-collection-assignment","aggregate_context_name":"Numeric-or-string-or-collection-assignment","aggregate_domain":"py","um2_aggregate_weight":1,"aggregate_active":1,"um2_direction":0,"aggregate_source_method":"Arun Parser v0.3","um2_concept_description":"Arun Parser v0.3","importance":0,"contributesK":0},{"aggregate_id":{},"um2_activity_id":{},"aggregate_content_name":"tmp1","um2_concept_id":{},"aggregate_component_name":"Slice","aggregate_context_name":"Slice","aggregate_domain":"py","um2_aggregate_weight":1,"aggregate_active":1,"um2_direction":0,"aggregate_source_method":"Arun Parser v0.3","um2_concept_description":"Arun Parser v0.3","importance":0,"**contributesK**":0},{"aggregate_id":{},"um2_activity_id":{},"aggregate_content_name":"tmp1","um2_concept_id":{},"aggregate_component_name":"Int","aggregate_context_name":"Int","aggregate_domain":"py","um2_aggregate_weight":1,"aggregate_active":1,"um2_direction":0,"aggregate_source_method":"Arun Parser v0.3","um2_concept_description":"Arun Parser v0.3","importance":0,"contributesK":0}]

ok
```

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from concepts_parser import main, post_process_parser
import os
from version import __version__

app = FastAPI()

class CodeString(BaseModel):
    """
    Custom type for code strings.
    This can be extended with validation if needed.
    """
    aggregate_id :int = 11111 ## Leave this blank if for insert query, otherwise provide id column in aggregate_kc_content_component
    um2_activity_id:int = 11111 ## Leave this blank if for insert query, otherwise provide id column in um2_ent_activity,
    aggregate_content_name:str =  'tmp' ### if use content_name as stored in um2_ent_activity,
    code_str:str
    # um2_concept_id : int ## this will be generated from backend
    # aggregate_component_name:str
    # aggregate_context_name: str
    # aggregate_domain:str = 'py' ## defaults to python
    # um2_aggregate_weight:int =  1
    # aggregate_active:int = 1
    # um2_direction: int = 0
    # aggregate_source_method:str = f'Arun Parser v{__version__}'
    # um2_concept_description:str =  f'Arun Parser v{__version__}'
    # importance:int = 0
    # contributesK:int = 0

@app.get("/test_api")
async def test_api():
    return {"message": "API is working!"}


@app.post("/extract_concepts")
async def extract_concepts(code_json: CodeString):
    print(code_json)
    
    if code_json is None:
        raise HTTPException(status_code=400, detail="Code string cannot be empty")
    try:
        code_str = code_json.code_str.strip()
        # Create a temporary directory for the code file
        if not os.path.exists('./py-files'):
            os.mkdir('py-files')

        # Write the code to a temporary file
        with open('./py-files/tmp1.py', 'w+') as f:
            f.write(code_str)

        # Extract concepts from the code
        response = main(filename='py-files/tmp1.py')
        
        # Clean up the temporary files
        os.remove('./py-files/tmp1.py')
        os.rmdir('./py-files')

        response_df =  post_process_parser(response,code_json.aggregate_content_name,code_json.um2_activity_id)
        return response_df
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import os,string,secrets,json
from datetime import datetime
import warnings
from typing import Dict,List
from flask import Flask, request, jsonify

from openfabric_pysdk.utility import SchemaUtil
from openfabric_pysdk.context import Ray, State,StateStatus,MessageType
from openfabric_pysdk.loader import ConfigClass

from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText

from test import final_result

### preliminary functions
app=Flask(__name__)

def generate_random_string(length=32):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

############################################################
# Callback function called on update config
############################################################
def config(configuration: Dict[str, ConfigClass], state: State):
    # TODO Add code here
    pass


############################################################
# Callback function called on each execution pass
############################################################

def execute(request: SimpleText,ray: Ray,state:State) -> SimpleText:
    output=[]

    for text in request:
        query_id = generate_random_string()
        sess_id=generate_random_string()
        query_id_path = os.path.join("datastore", f"{query_id}.json")

        ray = Ray(query_id)
        ray.sid=sess_id

        state["REQUESTED"].append(query_id)
        state["QUEUED"].append(query_id)

        ray.progress(step=25)
        try:
            #processing the input
            response=final_result(text)
            ######
            ray.progress(step=75)
            ray.status = "COMPLETED"
            ray.finished = True
            ray.updated_at = datetime.utcnow().isoformat()
            ray.message(
            message_type=MessageType.INFO,
            content=f"Query {query_id} processed successfully"
            )
            
            state["QUEUED"].remove(query_id)
            state["COMPLETED"].append(query_id)

            with open(query_id_path, "w") as query_file:
                json.dump(ray, query_file, default=str)
            
            output.append(response)

        except Exception as e:
            err_message=f"process - failed executing: {query_id} \n {str(e)}"
            ray.message(
            message_type=MessageType.ERROR,
            content=err_message
            )
            ray.status = "FAILED"
            ray.finished = True
            ray.updated_at = datetime.utcnow().isoformat()
            
            response="failed request!"

            if query_id in state["QUEUED"]:
                state["QUEUED"].remove(query_id)

            with open(query_id_path, "w") as query_file:
                json.dump(str(ray), query_file, default=str)
            
            output.append(str(err_message))
        
    
    return SchemaUtil.create(SimpleText(), dict(text=output))

@app.route('/', methods=['POST'])
def handle_request():
    # Access request data
    request_data = request.get_json()

    # Process the request using your NLP logic
    response_data = execute(request_data["q_list"], ray=None, state={"QUEUED": [], "REQUESTED": [], "COMPLETED": []}) 

    # Return the response as JSON
    return jsonify(response_data.text)

    
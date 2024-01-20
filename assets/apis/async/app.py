import os
import json
import boto3

from chalice import Chalice

from machine_generator_app import MachineGeneratorApp

# Write list to DynamoDB table
table_name = os.getenv("table_name")
column_name = os.getenv("column_name")
pipeline_name = os.getenv("pipeline_name")
model_id = os.getenv("model_id")
cp_client = boto3.client("codepipeline")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)

app = Chalice(app_name="MachineGeneratorApp")


@app.route("/", content_types=["application/json"])
def index(event, context):
    number = event["number"]
    industry = event["industry"]
    user_id = event["user_id"]
    model_kwargs = (
        event["model_kwargs"]
        if "model_kwargs" in event
        else {
            "max_tokens_to_sample": 1000,
            "temperature": 0.0,
            "top_p": 0.0,
        }
    )
    generator = MachineGeneratorApp(
        model_id=model_id,
        streaming=False,
        callbacks=[],
        model_kwargs=model_kwargs,
    )
    machines = generator.predict_list(number=number, industry=industry)

    table.put_item(
        Item={"user_id": user_id, "machines": machines, column_name: "yes"}
    )

    cp_client.start_pipeline_execution(
        name=pipeline_name,
    )

    return json.dumps({"statusCode": 200, "body": {"messag": "success"}})

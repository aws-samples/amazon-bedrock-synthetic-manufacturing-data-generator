import os
import boto3
import argparse
import logging

from data_generator_app import (
    DataGeneratorApp,
    create_bash_script,
    create_directory_string,
)

logger = logging.getLogger(__name__)
dynamodb = boto3.client("dynamodb")
s3_client = boto3.client("s3")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-level",
        type=str,
        default=os.environ.get("LOGLEVEL", "INFO").upper(),
    )
    parser.add_argument("--code-bucket", type=str, required=True)
    parser.add_argument("--data-bucket", type=str, required=True)
    parser.add_argument("--table-name", type=str, required=True)
    parser.add_argument("--column-name", type=str, required=True)
    parser.add_argument("--model-id", type=str, required=True)
    parser.add_argument("--context", type=str, default="very skilled")
    parser.add_argument("--language", type=str, default="python")
    parser.add_argument("--max-tokens-to-sample", type=int, default=4000)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top-p", type=float, default=1.0)
    args, _ = parser.parse_known_args()

    # Configure logging to output the line number and message
    log_format = "%(levelname)s: [%(filename)s:%(lineno)s] %(message)s"
    logging.basicConfig(format=log_format, level=args.log_level)

    # Set variables
    code_bucket = args.code_bucket
    data_bucket = args.data_bucket
    table_name = args.table_name
    column_name = args.column_name
    model_id = args.model_id
    context = args.context
    language = args.language
    model_kwargs = {
        "max_tokens_to_sample": args.max_tokens_to_sample,
        "temperature": args.temperature,
        "top_p": args.top_p,
    }

    # Define the filter expression and expression attribute values
    filter_expression = "#column_name = :column_value"
    expression_attribute_names = {"#column_name": column_name}
    expression_attribute_values = {":column_value": {"S": "yes"}}

    # Scan the DynamoDB table with the specified filter
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression=filter_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
    )

    # Retrieve all machines
    item = response.get("Items", [])
    if len(item) >= 1:
        item = response.get("Items", [])[0]
        user_id = item["user_id"]["S"]
        machines = [x["S"] for x in item["machines"]["L"]]

        # For each machine write the code and store it in a folder
        app = DataGeneratorApp(
            model_id=model_id,
            streaming=False,
            callbacks=[],
            model_kwargs=model_kwargs,
        )
        for machine in machines:
            try:
                code = app.predict_code(
                    context=context, question=machine, language=language
                )
                # directory = machine.lower().replace(" ", "-")
                directory = create_directory_string(machine=machine)
                app.write_parsed_code(code=code, dir=directory)

                response = s3_client.upload_file(
                    Filename=f"{directory}/main.py",
                    Bucket=code_bucket,
                    Key=f"{user_id}/{directory}/main.py",
                )
                print(f"{user_id}/{directory}/main.py", code_bucket)
                print(response)
            except Exception as e:
                print(f"Error: {e}")

        # Create a script that runs the code and moves data to S3
        create_bash_script(
            machines=machines, s3_bucket=data_bucket, user_id=user_id
        )

        # Update the user item and set the column_name (default: "active") to "no"
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)
        table.put_item(
            Item={"user_id": user_id, "machines": machines, column_name: "no"}
        )

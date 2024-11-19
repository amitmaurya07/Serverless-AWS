import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('web-app')  # Replace with your DynamoDB table name

def lambda_handler(event, context):
    print(json.dumps(event))  # Log the entire event for debugging

    # Handle CORS Preflight Request for OPTIONS
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # or your frontend domain
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'  # Allow POST and OPTIONS methods
            },
            'body': json.dumps('CORS Preflight Request handled successfully')
        }

    # POST Request Handling
    if event['httpMethod'] == 'POST':
        # Check if the body is present in the event
        if 'body' not in event:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*'  # Allow all domains or specify one
                },
                'body': json.dumps('Invalid request: No body in the request')
            }

        try:
            body = json.loads(event['body'])
            name = body.get('name')
            email = body.get('email')

            # Ensure both 'name' and 'email' are provided
            if not name or not email:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*'  # Allow all domains or specify one
                    },
                    'body': json.dumps('Invalid input: Name and Email are required')
                }

            # Save to DynamoDB
            table.put_item(
                Item={
                    'email': email,
                    'name': name
                }
            )

            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'  # Allow all domains or specify one
                },
                'body': json.dumps('Data stored successfully!')
            }

        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*'  # Allow all domains or specify one
                },
                'body': json.dumps('Invalid JSON format')
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*'  # Allow all domains or specify one
                },
                'body': json.dumps(f"Internal Server Error: {str(e)}")
            }

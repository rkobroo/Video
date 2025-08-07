"""
Netlify serverless function for the video downloader API
"""
import json
import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def handler(event, context):
    """
    Netlify function handler
    """
    try:
        # Import the Flask app
        from app_vercel import app
        
        # Extract request data
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_string = event.get('queryStringParameters') or {}
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # Convert query parameters to proper format
        query_string_list = []
        for key, value in query_string.items():
            if value:
                query_string_list.append(f"{key}={value}")
        query_string_formatted = '&'.join(query_string_list)
        
        # Create a mock request environment
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': query_string_formatted,
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)) if body else '0',
            'wsgi.input': body,
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '443',
            'wsgi.url_scheme': 'https'
        }
        
        # Add headers to environ
        for key, value in headers.items():
            key = key.upper().replace('-', '_')
            if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = f'HTTP_{key}'
            environ[key] = value
        
        # Process the request
        with app.test_client() as client:
            if method == 'GET':
                response = client.get(path, query_string=query_string_formatted)
            elif method == 'POST':
                response = client.post(path, data=body, 
                                     content_type=headers.get('content-type', 'application/json'))
            elif method == 'PUT':
                response = client.put(path, data=body,
                                    content_type=headers.get('content-type', 'application/json'))
            elif method == 'DELETE':
                response = client.delete(path)
            else:
                response = client.open(path, method=method, data=body,
                                     content_type=headers.get('content-type', 'application/json'))
        
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }

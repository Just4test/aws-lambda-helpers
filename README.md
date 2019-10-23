# Install
pip install aws-lambda-helper

# How to use

### http
A decorator that helps you to create response body easily. You can:
* Return a plain string.
* Return an object that will be converted to JSON string.
* Return an Exception.
* Return both status code and body.


```
from lambdahelper import http

@http
def login_handler(event, context):
    http.add_cookie('token', usertoken)
    return 302, '/login_success'
```
You must use @http before a http handler to enable of using http.set_header or other sub functions.

### http.set_header
Set response header. Will cover the same name header.
### http.add_header
Add response header. You can add multi headers with same name
### http.add_cookie
Append cookie.

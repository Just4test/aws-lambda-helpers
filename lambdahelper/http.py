import json
import traceback

    
_STATUS_CODE_PROCESSOR = {
  301: lambda code, body: add_header('Location', body),
  302: lambda code, body: add_header('Location', body),
  307: lambda code, body: add_header('Location', body),
  308: lambda code, body: add_header('Location', body),
}

http_response = None
def _reset_response():
  global http_response
  http_response = {
    'statusCode': 200,
    'multiValueHeaders': {}
  }
  
def helper(handler):
  def wrapper(event, context):
    global http_response
    _reset_response()
    parse_cookie(event)
    try:
      ret = handler(event, context)
    except Exception as e:
      return {
        'statusCode': 500,
        'body': traceback.format_exc()
      }
    
    if len(ret) == 2 and isinstance(ret[0], int):
      http_response['statusCode'] = ret[0]
      processor = _STATUS_CODE_PROCESSOR.get(ret[0])
      if processor:
        processor(ret[0], ret[1])
        return http_response
      else:
        ret = ret[1]
    
    if isinstance(ret, Exception):
      http_response['body'] = str(ret)
      if 'statusCode' not in http_response:
        http_response['statusCode'] = 500
    
    http_response['body'] = ret if isinstance(ret, str) else json.dumps(ret)
      
      
    if 'statusCode' not in http_response:
      http_response['statusCode'] = 200
      
    return http_response
  return wrapper
      


def set_header(name, value):
  http_response['multiValueHeaders'][name] = [value]

def add_header(name, value):
  if name not in http_response['multiValueHeaders']:
    http_response['multiValueHeaders'][name] = [value]
  else:
    http_response['multiValueHeaders'][name].append(value)
      
def add_cookie(name, value, expires=None, maxage=None, domain=None, path='/', secure=False, httponly=False):
  s = f'{name}={value}'
  if expires is not None:
    s += f'; Expires={expires}'
  if maxage is not None:
    s += f'; Max-Age={maxage}'
  if domain is not None:
    s += f'; Domain={domain}'
  if path is not None:
    s += f'; Path={path}'
  if httponly:
    s += '; HttpOnly'
  if secure:
    s += '; Secure'
  add_header('Set-Cookie', s)

helper.set_header = set_header
helper.add_header = add_header
helper.add_cookie = add_cookie

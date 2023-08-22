import pytest

import json
import requests
from polytope.github.repository.Repository import fetch_message_and_errors

def test_fetch_message_and_errors_empty():
    resp = requests.Response()
    resp._content = ''
    
    error_msg, errors_detail = fetch_message_and_errors(resp)
    
    assert error_msg is None
    assert errors_detail is None

    resp._content = '{}'

    error_msg, errors_detail = fetch_message_and_errors(resp)
    
    assert error_msg is None
    assert errors_detail is None

def test_fetch_message_and_errors_normal():
    resp = requests.Response()
    
    msg = 'test error msg'
    errors = [{'error_1' : 'error_desc_1', 'error_2' : 'error_desc_2'}]
    resp._content = json.dumps({
        "message": msg,
        "errors": errors
    })

    error_msg, errors_detail = fetch_message_and_errors(resp)

    assert json.dumps(msg) == error_msg
    assert json.dumps(errors) == errors_detail
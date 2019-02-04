from . import api
from flask import current_app as app
from flask import request
from .response_utils import JSON_MIME_TYPE, success_, success_json

'''
    /template/test
    http://127.0.0.1:5000/template/test
'''
@api.route('/template/test')
def test():
    
    '''
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    '''   
    
    c = 6 + 7

    result_json = {
        'result': c,
        
        'api_error': 0
    }
    
    return success_json(result_json)

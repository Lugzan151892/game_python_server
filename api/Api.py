from flask import jsonify, request, Response
class Api:
    def __init__(self, message: str = None, data = None):
        self.message = message
        self.data = data
    
    def handle_preflight():
        if request.method == 'OPTIONS':
            response = Response()
            response.headers.add("Access-Control-Allow-Credentials", "true")
            response.headers.add("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT")
            response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, authorization, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    
    def update_response(self, response: dict):
        if self.message:
            response.update({'message': self.message})
        if self.data:
            response.update({'data': self.data})
        response = jsonify(response)
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT")
        response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    def response(self):
        response = {'error': False, 'status': 200}
        return self.update_response(response)
    
    def bad_request(self):
        response = {'error': True, 'status': 404}
        return self.update_response(response)
    
    def internal(self):
        response = {'error': True, 'status': 500}
        return self.update_response(response)
    
    def system_error(self, message):
        response = {'error': True, 'status': 401, 'system_message': message}
        return self.update_response(response)

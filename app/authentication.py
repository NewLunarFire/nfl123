from functools import wraps
#from flask import request

# decorator for verifying the JWT
def authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("patate poil")
        # token = None
        # # jwt is passed in the request header
        # if 'x-access-token' in request.headers:
        #     token = request.headers['x-access-token']
        # # return 401 if token is not passed
        # if not token:
        #     return jsonify({'message' : 'Token is missing !!'}), 401
  
        # try:
        #     # decoding the payload to fetch the stored details
        #     data = jwt.decode(token, app.config['SECRET_KEY'])
        #     current_user = User.query\
        #         .filter_by(public_id = data['public_id'])\
        #         .first()
        # except:
        #     return jsonify({
        #         'message' : 'Token is invalid !!'
        #     }), 401
        # # returns the current logged in users contex to the routes
        return  f(*args, **kwargs)
  
    return decorated
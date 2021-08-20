import json
import os
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


# AUTH0_DOMAIN = 'fsnd-saylesc.us.auth0.com'
# ALGORITHMS = ['RS256']
# API_AUDIENCE = 'fsnd-surf-events'
API_AUDIENCE = os.environ.get('API_AUDIENCE')
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = [os.environ.get('ALGORITHMS')]
AUTHORIZATION = 'Authorization'
BEARER = 'bearer'


# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
Get_token_auth_header() method
    attempts to get the header from the request
    attempts to split bearer and the token
    raises an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    auth = request.headers.get(AUTHORIZATION, None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != BEARER:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


'''
check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:surf_contest')
        payload: decoded jwt payload

    Raises an AuthError if permissions are not included in the payload
        or if the requested permission string is not in the payload
        permissions array
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Permissions must be present in payload of token.'
        }, 400)

    if permission not in payload['permissions']:
        # Permission not allowed
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Permission is not allowed for this token.'
        }, 403)

    return True


'''
verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    token should be an Auth0 token with key id (kid)
    verifies the token using Auth0 /.well-known/jwks.json
    decodes the payload from the token
    validates the claims
    return the decoded payload
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims.  ' +
                'Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    uses the get_token_auth_header method to get the token
    uses the verify_decode_jwt method to decode the jwt
    uses the check_permissions method validate claims and check the
        requested permission
    return the decorator which passes the decoded payload to the
        decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            authError = False
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
            except AuthError as authErr:
                return f(authErr, *args, **kwargs)

            # Check to see what permissions this authorized user has
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

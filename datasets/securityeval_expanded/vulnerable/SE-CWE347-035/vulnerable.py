import jwt\n\n\ndef verifyJsonWebToken(token):\n    '''\n    Decode the JSON web token passed and return it.\n    '''\n    return jwt.decode(token, verify=False)

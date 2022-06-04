import jwt


class JWTEncodeDecode:

    def encode_data(self, payload):
        token_encoded = jwt.encode({"id": payload}, "secret", algorithm="HS256")
        return token_encoded

    def decode_data(self, token):
        token_decode = jwt.decode(token, "secret", algorithms=["HS256"])
        return token_decode

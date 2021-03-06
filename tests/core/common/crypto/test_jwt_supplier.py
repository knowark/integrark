import jwt
from pytest import fixture
from integrark.core import JwtSupplier


@fixture
def jwt_supplier():
    return JwtSupplier('SECRET')


def test_jwt_supplier_instantiation(jwt_supplier):
    assert jwt_supplier is not None


def test_jwt_supplier_encode(jwt_supplier):
    assert jwt_supplier.encode() is None


def test_jwt_supplier_decode(jwt_supplier):
    payload = {
        'name': 'John',
        'age': 30
    }
    secret = "CUSTOM_SECRET"
    token = jwt.encode(payload, secret)

    result = jwt_supplier.decode(token, secret)

    assert result == payload


def test_jwt_supplier_decode_invalid(jwt_supplier):
    payload = {
        'name': 'John',
        'age': 30
    }
    wrong_secret = "WRONG_SECRET"
    token = jwt.encode(payload, wrong_secret)

    secret = "CUSTOM_SECRET"
    result = jwt_supplier.decode(token, secret)

    assert result is None

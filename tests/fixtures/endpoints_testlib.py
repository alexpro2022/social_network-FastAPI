from http import HTTPStatus
from typing import Any, TypeAlias

from httpx import Response
from fastapi.testclient import TestClient

from app.main import app


Method: TypeAlias = Response
Methods: TypeAlias = tuple[Method]
PathParam: TypeAlias = int | str | None
QueryParams: TypeAlias = dict[str:str] | None
Payload: TypeAlias = dict[str:str] | None

client = TestClient(app)

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'


def get_registered(user: dict) -> None:
    response = client.post('/auth/register', json=user)
    assert response.status_code == HTTPStatus.CREATED
    auth_user = response.json()
    assert isinstance(auth_user['id'], int)
    assert auth_user['email'] == user['email']
    assert auth_user['is_active'] == True
    assert auth_user['is_superuser'] == False
    assert auth_user['is_verified'] == False


def get_auth_user_token(user: dict) -> str:
    get_registered(user)
    user['username'] = user['email']
    response = client.post('/auth/jwt/login', data=user)
    assert response.status_code == HTTPStatus.OK, response.json()
    token = response.json()['access_token']
    assert isinstance(token, str)
    return token


def get_headers(token: str) -> dict[str:str]:
    return {'Authorization': f'Bearer {token}'}


def get_invalid_str() -> tuple[str]:
    return None, '', ' ', '-invalid-'


def get_invalid_int() -> tuple[int]:
    return 0, -1, 10**12


def get_invalid_dict_keys(original: dict) -> tuple[dict]:
    dicts = []
    for key in original:
        for invalid_key in get_invalid_str():
            dd = original.copy()
            value = dd.pop(key)
            dd[invalid_key] = value
            dicts.append(dd)
    return None, *dicts


def get_invalid(item: int | str | dict) -> tuple[int | str | dict]:
    if isinstance(item, int):
        return get_invalid_int()
    if isinstance(item, str):
        return get_invalid_str()
    if isinstance(item, dict):
        return get_invalid_dict_keys(item)


def strip_slashes(item: str) -> str:
    if item and item[0] == '/':
        item = item[1:]
    if item and item[-1] == '/':
        item = item[:-1]
    return item


def create_endpoint(endpoint: str, path_param: PathParam) -> str:
    if endpoint in ('/', '//'):
        if path_param is not None:
            return f'/{strip_slashes(str(path_param))}/'
        return '/'
    if path_param is not None:
        return f'/{strip_slashes(endpoint)}/{strip_slashes(str(path_param))}/'
    return f'/{strip_slashes(endpoint)}/'


def get_method(method: str) -> Method:
    match method.upper():
        case 'GET':
            return client.get
        case 'POST':
            return client.post
        case 'PUT':
            return client.put
        case 'PATCH':
            return client.patch
        case 'DELETE':
            return client.delete


def get_response(
    method: str,
    endpoint: str,
    *,
    path_param: int | str | None = None,
    params: dict[str:str] | None = None,
    json: dict[str:str] | None = None,
    data: dict | None = None,
    headers: dict | None = None,
) -> Response:
    endpoint = create_endpoint(endpoint, path_param)
    if method.upper() in (PATCH, POST, PUT):
        return get_method(method)(endpoint, params=params,headers=headers, data=data, json=json)
    else:
        return get_method(method)(endpoint, params=params,headers=headers)


def assert_response(
    status_code: int,
    method: str,
    endpoint: str,
    *,
    path_param: int | str | None = None,
    params: dict[str:str] | None = None,
    data: dict | None = None,
    json: dict[str:str] | None = None,
    headers: dict | None = None,
) -> Response:
    response: Response = get_response(method, endpoint, path_param=path_param, params=params, data=data, json=json, headers=headers)
    assert response.status_code == status_code, (
        f'{response.status_code} != {status_code} ->'
        f'\n   {method}({create_endpoint(endpoint, path_param)}\n   {headers}\n   {params}\n   {json}\n   {data})\n')
    return response


def __dummy_func(response_json) -> str:
    return 'DONE'


def valid_values_standard_tests(
    method: str,
    endpoint: str,
    *,
    path_param: int | str | None = None,
    params: dict[str:str] | None = None,
    params_optional: bool = False,
    json: dict[str:str] | None = None,
    json_optional: bool = False,
    data: dict[str:str] | None = None,
    data_optional: bool = False,
    headers: dict | None = None,
    func_check_valid_response: Any | None = None,
    msg_invalid_path_param: str | None = None,
) -> None:

    # valid_request_test
    response = assert_response(HTTPStatus.OK, method, endpoint, path_param=path_param, params=params, json=json, data=data, headers=headers)
    match method.upper():
        # Sequential POST with the same data should get a Integrity Error wich raises BAD_REQUEST
        case 'POST':
            assert_response(HTTPStatus.BAD_REQUEST, method, endpoint, path_param=path_param, params=params, json=json, data=data, headers=headers)
        # Sequential DELETE with the same data should get NOT_FOUND
        case 'DELETE':
            assert_response(HTTPStatus.NOT_FOUND, method, endpoint, path_param=path_param, params=params, json=json, data=data, headers=headers)
    if func_check_valid_response is None:
        func_check_valid_response = __dummy_func
    assert func_check_valid_response(response.json()) == 'DONE'

    # invalid_endpoint_test
    for invalid_endpoint in get_invalid(endpoint):
        assert_response(HTTPStatus.NOT_FOUND, method, invalid_endpoint, path_param=path_param, params=params, json=json, data=data, headers=headers)

    # invalid_path_param_test
    if path_param is not None:
        for invalid_path_param in get_invalid(path_param):
            response = assert_response(HTTPStatus.NOT_FOUND, method, endpoint, path_param=invalid_path_param, params=params, json=json, data=data, headers=headers)
            if msg_invalid_path_param is not None:
                assert response.json() == {'detail': msg_invalid_path_param}, response.json()

    # invalid_query_params_keys_test
    if params is not None and not params_optional:
        for invalid_keys_params in get_invalid(params):
            assert_response(HTTPStatus.UNPROCESSABLE_ENTITY, method, endpoint, path_param=path_param, params=invalid_keys_params, json=json, data=data, headers=headers)

    # invalid_payload_keys_test
    if json is not None and not json_optional:
        for invalid_keys_json in get_invalid(json):
            assert_response(HTTPStatus.UNPROCESSABLE_ENTITY, method, endpoint, path_param=path_param, params=params, json=invalid_keys_json, data=data, headers=headers)

    # invalid_form_keys_test
    if data is not None and not data_optional:
        for invalid_keys_data in get_invalid(data):
            assert_response(HTTPStatus.UNPROCESSABLE_ENTITY, method, endpoint, path_param=path_param, params=params, json=json, data=invalid_keys_data, headers=headers)



def invalid_methods_test(
    invalid_methods: tuple[str],
    endpoint: str,
    path_param: int | str | None = None,
) -> None:
    for invalid_method in invalid_methods:
        assert_response(HTTPStatus.METHOD_NOT_ALLOWED, invalid_method, endpoint, path_param=path_param)

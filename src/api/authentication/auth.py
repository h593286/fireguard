from fastapi import Request, Depends, HTTPException, status, Response
from keycloak import KeycloakOpenID
from decouple import config
from dotenv import load_dotenv
import os

from src.api.authentication.User import User
load_dotenv()

keycloak_openid = KeycloakOpenID(
    server_url=os.getenv('KEYCLOAK_SERVER_URL'),
    realm_name=os.getenv('KEYCLOAK_REALM_NAME'),
    client_id=""

)

def get_jwt_token(req: Request):
    token = req.headers.get("Authorization")
    if token is None:
        return None
    
    scheme, token = token.split(" ")
    #print(scheme, token)
    return scheme, token

async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )

async def get_payload(token=Depends(get_jwt_token)):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return keycloak_openid.decode_token(
            token[1],
            key=await get_idp_public_key(),
            options={
                "verify_signature":True,
                "verify_iss": True,
                "verify_exp": True
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
async def get_user_info(payload:dict=Depends(get_payload)) -> User:
    #print(payload)
    client_id = payload.get("azp")
    try:
        return User(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            first_name=payload.get("given_name"),
            last_name=payload.get("family_name"),
            realm_roles=payload.get("realm_access", {}).get("roles",[]),
            client_roles=payload.get("resource_access", {}).get(client_id, {}).get("roles", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def verify_user_role(user: User = Depends(get_user_info)) -> bool:
    roles: list = user.realm_roles
    roles.extend(user.client_roles)
    #print(roles)
    return verify_role(roles, "USER")

def verify_admin_role(user: User = Depends(get_user_info)) -> bool:
    roles: list = user.realm_roles
    roles.extend(user.client_roles)
    #print(roles)
    return verify_role(roles, "ADMIN")

def verify_role(roles:list,role:str)->bool:
    try:
        roles.index(role)
        return True
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized action",
            headers={"WWW-Authenticate": "Bearer"},
        )
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from tortoise import Tortoise

import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
JWT_SECRET = 'iSystemKids_sdiKmetsySi'


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await models.UserModel.get(username=payload.get('username'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    return await models.User_Pydantic.from_tortoise_orm(user)


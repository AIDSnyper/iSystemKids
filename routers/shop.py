from fastapi import HTTPException, status, APIRouter, Depends
from utils import get_current_user

import models

router = APIRouter(tags=['Shop'])


@router.get('/all_products')
async def all_products():
    return await models.Shop_Pydantic.from_queryset(models.Shop.all())


@router.get('/me')
async def me(user: models.UserIn_Pydantic = Depends(get_current_user)):
    curr_d = user.balance_diamonds
    curr_t = user.balance_tokens
    return {'message': f'You have {curr_d} diamonds and {curr_t} tokens.'}


@router.post('/add_product')
async def add_product(product: models.ShopIn_Pydantic = Depends()):
    await models.Shop.create(**product.dict())
    raise HTTPException(status_code=status.HTTP_201_CREATED)


@router.post('/buy_product')
async def buy_product(id: int, user_id: int):
    user = await models.UserModel.get_or_none(id=user_id).values()
    product = await models.Shop.get_or_none(id=id).values()
    price_d = product['price_diamonds']
    price_t = product['price_tokens']
    curr_d = user['balance_diamonds']
    curr_t = user['balance_tokens']
    if curr_d >= price_d and curr_t >= price_t:
        diamonds = curr_d - price_d
        tokens = curr_t - price_t
        await models.UserModel.filter(id=user_id).update(balance_diamonds=diamonds, balance_tokens=tokens)
        return {'message': 'Product bought successfully'}
    else:
        return {'message': 'You do not have enough diamonds and tokens to but this product'}


@router.delete('/delete_product/{id}')
async def delete_product(id: int, curr: models.User_Pydantic = Depends(get_current_user)):
    if curr.role == "admin":
        await models.Shop.filter(id=id).delete()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Product deleted')
    else:
        return {'message': 'Permission denied!'}

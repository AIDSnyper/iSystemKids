import secrets
import jwt
from PIL import Image
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
import models
from routers import shop, lesson, homework, todo
from tortoise.contrib.fastapi import register_tortoise
from passlib.hash import bcrypt
from utils import oauth2_scheme, JWT_SECRET

app = FastAPI(title='iSystemKids')
app.mount('/static', StaticFiles(directory='static'), name='static')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await models.UserModel.get(username=payload.get('username'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    return await models.User_Pydantic.from_tortoise_orm(user)


async def authenticate_user(username: str, password: str):
    user = await models.UserModel.get(username=username)
    if not user and not user.verify_password(password):
        return False
    else:
        return user


@app.get('/users/me', tags=['User'])
async def get_user_curr(user: models.UserIn_Pydantic = Depends(get_current_user)):
    return user


@app.get('/admins', tags=['User'])
async def admins():
    return await models.User_Pydantic.from_queryset(models.UserModel.filter(role="admin"))


@app.get('/teachers', tags=['User'])
async def teachers():
    return await models.User_Pydantic.from_queryset(models.UserModel.filter(role="teacher"))


@app.get('/students', tags=['User'])
async def students():
    return await models.User_Pydantic.from_queryset(models.UserModel.filter(role="student"))


@app.get('/get_lessons', tags=['User'])
async def get_lessons(curr: models.User_Pydantic = Depends(get_current_user)):
    lessons = []
    curr_id = curr.id
    all_lessons = await models.Lesson_Pydantic.from_queryset(models.Lesson.all())
    for i in all_lessons:
        a = []
        students = i.students
        for j in range(0, len(students), 2):
            a.append(int(students[j]))
        if int(curr_id) in a:
            lessons.append(i)
    return lessons


@app.get('/diamonds', tags=['User'])
async def diamonds(curr: models.User_Pydantic = Depends(get_current_user)):
    balance = curr.balance_diamonds
    data = balance * 20

    return {'data': balance, 'data2': data}


@app.post('/create_user', tags=['User'])
async def create_user(user: models.UserIn_Pydantic = Depends(models.CreateUser)):
    FILEPATH = './static/users/'
    filename = user.avatar.filename
    extension = filename.split(".")[-1]05.6
    if extension not in ['png', 'jpg']:
        return {"error": 'File extension not allowed'}
    token_name = secrets.token_hex(10) + '.' + extension
    genereted_name = FILEPATH + token_name
    file_content = await user.avatar.read()
    with open(genereted_name, 'wb') as file:
        file.write(file_content)

    img = Image.open(genereted_name)
    img = img.resize(size=(200, 200))
    img.save(genereted_name)
    file.close()
    obj = models.UserModel(name=user.name, last_name=user.last_name, username=user.username, email=user.email,
                           role=user.role, password=bcrypt.hash(user.password), avatar=token_name)
    await obj.save()
    raise HTTPException(status_code=status.HTTP_201_CREATED)


@app.post('/token', tags=['User'])
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return {'error': 'Incorrect username or password'}
    obj = await models.UserOut_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(obj.dict(), JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


@app.post('/give_tokens', tags=['User'])
async def give_tokens(user_id: int, tokens_number: int, user: models.UserIn_Pydantic = Depends(get_current_user)):
    use = await models.UserModel.get_or_none(id=user_id).values()
    if use is not None:
        if user.role == "teacher" or user.role == "admin":
            if tokens_number > 0 and tokens_number <= 5:
                tokens = use['balance_tokens']
                a = tokens + tokens_number
                await models.UserModel.filter(id=user_id).update(balance_tokens=a)
                return {'message': 'Tokens have given!'}
            else:
                return {'message': 'You can give only 5 tokens'}
        else:
            return {'message': 'Permission denied'}
    else:
        return {'message': 'User not founded'}


@app.post('/give_diamonds', tags=['User'])
async def give_diamonds(user_id: int, diamonds_number: int, user: models.UserIn_Pydantic = Depends(get_current_user)):
    use = await models.UserModel.get_or_none(id=user_id).values()
    if use is not None:
        if user.role == "teacher" or user.role == "admin":
            if diamonds_number > 0 and diamonds_number <= 5:
                diamonds = use['balance_diamonds']
                a = diamonds + diamonds_number
                await models.UserModel.filter(id=user_id).update(balance_diamonds=a)
                return {'message': 'Diamonds have given!'}
            else:
                return {'message': 'You can give only 5 diamonds'}
        else:
            return {'message': 'Permission denied'}
    else:
        return {'message': 'User not founded'}


@app.post('/take_tokens', tags=['User'])
async def take_tokens(user_id: int, tokens_number: int, user: models.UserIn_Pydantic = Depends(get_current_user)):
    use = await models.UserModel.get_or_none(id=user_id).values()
    if use is not None:
        if user.role == "teacher" or user.role == "admin":
            tokens = use['balance_tokens']
            if tokens >= tokens_number:
                a = tokens - tokens_number
                await models.UserModel.filter(id=user_id).update(balance_tokens=a)
                return {'message': 'Tokens have taken!'}
            else:
                return {'message': 'There are not enough tokens'}
        else:
            return {'message': 'Permission denied'}
    else:
        return {'message': 'User not founded'}


@app.post('/take_diamonds', tags=['User'])
async def take_diamonds(user_id: int, diamonds_number: int, user: models.UserIn_Pydantic = Depends(get_current_user)):
    use = await models.UserModel.get_or_none(id=user_id).values()
    if use is not None:
        if user.role == "teacher" or user.role == "admin":
            diamonds = use['balance_diamonds']
            if diamonds >= diamonds_number:
                a = diamonds - diamonds_number
                await models.UserModel.filter(id=user_id).update(balance_diamonds=a)
                return {'message': 'Diamonds have taken!'}
            else:
                return {'message': 'There are not enough diamonds'}
        else:
            return {'message': 'Permission denied'}
    else:
        return {'message': 'User not founded'}


@app.delete('/delete_user', tags=['User'])
async def delete_user(curr: models.UserIn_Pydantic = Depends(get_current_user)):
    await models.UserModel().filter(username=curr.username).delete()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='User deleted')


app.include_router(shop.router)
app.include_router(homework.router)
app.include_router(todo.router)
app.include_router(lesson.router)

TORTOISE_ORM = {
    "connections": {
        "default": 'postgres://isystem:isystem@localhost/isystem'
    },
    "apps": {
        "models": {
            "models": ['aerich.models', 'models'],
            "default_connection": "default",
        },
    },
}
register_tortoise(
    app,
    modules={"models": ["models"]},
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True
)

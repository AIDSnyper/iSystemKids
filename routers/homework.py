import secrets
from datetime import datetime
from utils import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
import models

router = APIRouter(tags=["Homework"])


@router.get('/all_homeworks')
async def get_all_homeworks():
    return await models.Homework_Pydantic.from_queryset(models.Homework.all())


@router.post('/create_homework')
async def create_homework(hw: models.CreateHomework = Depends()):
    FILEPATH = './static/homeworks/'
    filename = hw.file.filename
    extension = filename.split(".")[-1]
    if extension not in ['txt']:
        return {"error": 'File extension not allowed'}
    token_name = secrets.token_hex(10) + '.' + extension
    genereted_name = FILEPATH + token_name
    file_content = await hw.file.read()
    with open(genereted_name, 'wb') as file:
        file.write(file_content)
    file.close()
    try:
        start_date = datetime.fromisoformat(hw.start_date)
        end_date = datetime.fromisoformat(hw.start_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format")
    model = models.Homework(title=hw.title, start_date=start_date, end_date=end_date, mark=hw.mark,
                            lesson=hw.lesson_id, file=str(genereted_name))
    await model.save()
    raise HTTPException(status_code=status.HTTP_201_CREATED)


@router.delete('/delete_homework/{id}')
async def delete_homework(id: int, curr: models.User_Pydantic = Depends(get_current_user)):
    hw = models.Homework.get_or_none(id=id)
    curr_role = curr.role
    if curr_role not in ['admin', 'teacher']:
        return {'message': 'Permission denied'}
    else:
        if hw is not None:
            await models.Homework.filter(id=id).delete()
            return {'message': 'Homework deleted'}

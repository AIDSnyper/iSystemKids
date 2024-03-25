from fastapi import APIRouter, Depends
import models
from utils import get_current_user

router = APIRouter()


@router.get('/get_todos', tags=['Todo'])
async def get_todos(curr: models.User_Pydantic = Depends(get_current_user)):
    curr_id = curr.id
    if curr.role == 'admin':
        return await models.Todo_Pydantic.from_queryset(models.TodoModel.all())
    else:
        return await models.Todo_Pydantic.from_queryset(models.TodoModel.filter(owner_id=curr_id))


@router.post('/create_todo', tags=['Todo'])
async def create_todo(todo: models.TodoSchema = Depends(), curr: models.User_Pydantic = Depends(get_current_user)):
    curr_id = curr.id
    todo_model = models.TodoModel(title=todo.title, description=todo.description, complated=todo.complated,
                                  owner_id=curr_id)
    await todo_model.save()
    return {'msg': 'Todo Created'}


@router.delete('/delete_todo', tags=['Todo'])
async def delete_todo(id: int, curr: models.User_Pydantic = Depends(get_current_user)):
    todo = await models.TodoModel.get_or_none(id=id).values()
    if todo['owner_id'] == curr.id or curr.role in ['admin']:
        await models.TodoModel.filter(id=id).delete()
        return {'msg': 'Todo Deleted'}
    else:
        return {'msg': 'You do not have permission to delete this todo'}

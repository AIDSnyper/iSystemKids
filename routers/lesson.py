from fastapi import APIRouter, Depends, Query
import models
from utils import get_current_user

router = APIRouter()


@router.get('/get_all_lessons', tags=['Lessons'])
async def get_all_lessons():
    return await models.Lesson_Pydantic.from_queryset(models.Lesson.all())


@router.get('/get_lesson/{id}', tags=['Lessons'])
async def get_all_lessons(id: int):
    lesson = await models.Lesson.get_or_none(id=id).values()
    if lesson is not None:
        return lesson
    else:
        return {'message': 'Lesson does not exist'}


@router.get('/get_students_lesson{id}', tags=['Lessons'])
async def get_students_lesson(id: int):
    lesson = await models.Lesson.get_or_none(id=id).values()
    s = str(lesson['students']).split(',')
    s.pop(-1)
    if lesson is None:
        return {'message': 'Lesson does not exist'}
    else:
        students = []
        for i in s:
            print(i)
            student = await models.UserModel.get_or_none(id=int(i)).values()
            students.append(student)
        return students


@router.get('/get_teachers/lessons/{id}', tags=['Lessons'])
async def get_teachers_lessons(teacher_id: int, curr: models.UserIn_Pydantic = Depends(get_current_user)):
    if curr.role == models.Role.admin or curr.role == models.Role.teacher:
        is_teacher = await models.UserModel.get_or_none(id=teacher_id).values()
        if is_teacher['role'] == models.Role.teacher:
            return await models.LessonOut_Pydantic.from_queryset(models.Lesson.filter(teacher=teacher_id))
        else:
            return {'message': 'The teacher does not exist'}
    else:
        return {'message': 'You are not teacher or admin!'}


@router.post('/create_lesson', tags=['Lessons'])
async def create_lesson(lesson: models.LessonIn_Pydantic = Depends(),
                        teacher_id: int = Query(description="ID of the teacher for the lesson"),
                        student_ids: list[int] = Query(description="List of student IDs for the lesson", min_items=1),
                        ):
    teacher = await models.UserModel.get_or_none(id=teacher_id).values()
    if teacher['role'] != 'teacher':
        return {'message': 'The teacher is not a teacher'}
    else:
        accepted_students = []
        for i in student_ids:
            student = await models.UserModel.get_or_none(id=i).values()
            if student is not None and student['role'] == 'student' and i not in accepted_students:
                accepted_students.append(i)
        all_of_students = ""
        for i in accepted_students:
            all_of_students += str(i)
            all_of_students += ","
        new_lesson = await models.Lesson.create(title=lesson.title, content=lesson.content, teacher=teacher['id'],
                                                students=all_of_students, start_date=lesson.start_date,
                                                end_date=lesson.end_date)
        return new_lesson


@router.post('/add_students', tags=['Lessons'])
async def add_student(lesson_id: int,
                      student_ids: list[int] = Query(description="List of student IDs for the lesson", min_items=1)):
    lesson = await models.Lesson.get_or_none(id=lesson_id).values()
    accepted_students = []
    for i in student_ids:
        s = await models.UserModel.get_or_none(id=i).values()
        if s is not None and s['role'] == 'student' and i not in accepted_students:
            accepted_students.append(i)
    if lesson is None:
        return {'message': 'Lesson does not exist'}
    else:
        studens_in_model = lesson['students']
        for i in accepted_students:
            if str(studens_in_model).count(str(i)) == 0:
                studens_in_model += str(i)
                studens_in_model += ","
        await models.Lesson.filter(id=lesson_id).update(students=studens_in_model)
        return await models.Lesson_Pydantic.from_queryset(models.Lesson.filter(id=lesson_id))


@router.delete('/delete_lesson', tags=['Lessons'])
async def delete_lesson(id: int, curr: models.User_Pydantic = Depends(get_current_user)):
    if curr.role != models.Role.admin:
        return {'message': 'Permission denied!'}
    else:
        await models.Lesson.filter(id=id).delete()
        return {'message': 'Lesson deleted'}

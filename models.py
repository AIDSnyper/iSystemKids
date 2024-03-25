from passlib.hash import bcrypt
from pydantic import BaseModel
from fastapi import UploadFile, File, Query
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class CreateUser(BaseModel):
    username: str
    name: str
    last_name: str
    email: str
    password: str
    avatar: UploadFile = File(...)
    role: Role


class UserModel(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=44, unique=True)
    name = fields.CharField(max_length=44)
    last_name = fields.CharField(max_length=44)
    email = fields.CharField(max_length=44)
    role = fields.CharField(max_length=44)
    balance_diamonds = fields.IntField(default=0)
    balance_tokens = fields.IntField(default=0)
    avatar = fields.CharField(max_length=404, null=True)
    password = fields.CharField(max_length=404)
    lessons = fields.ManyToManyRelation['Lesson']
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)


class TodoModel(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=44)
    description = fields.CharField(max_length=100)
    complated = fields.BooleanField(default=False)
    owner = fields.ForeignKeyField('models.UserModel', related_name='owner')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class TodoSchema(BaseModel):
    title: str
    description: str
    complated: bool


class Shop(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=44)
    price_tokens = fields.IntField()
    price_diamonds = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Lesson(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    students = fields.CharField(max_length=255, null=True)
    teacher = fields.CharField(max_length=44, null=True)
    start_date = fields.DateField()
    end_date = fields.DateField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class CreateHomework(BaseModel):
    title: str
    start_date: str
    end_date: str
    file: UploadFile = File(...)
    mark: int
    lesson_id: int


class Homework(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=44)
    start_date = fields.DateField()
    end_date = fields.DateField()
    file = fields.CharField(max_length=255)
    mark = fields.IntField()
    lesson = fields.CharField(max_length=222)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


User_Pydantic = pydantic_model_creator(UserModel, name='UserStudent')
UserOut_Pydantic = pydantic_model_creator(UserModel, name='UserStudentOut', exclude_readonly=True,
                                          exclude=('created_at', 'updated_at'))
UserIn_Pydantic = pydantic_model_creator(UserModel, name='UserStudentIn', exclude_readonly=True,
                                         exclude=('created_at', 'updated_at', 'role'))
Shop_Pydantic = pydantic_model_creator(Shop, name='Shop')
ShopIn_Pydantic = pydantic_model_creator(Shop, name='ShopIn', exclude_readonly=True,
                                         exclude=('created_at', 'updated_at'))
Lesson_Pydantic = pydantic_model_creator(Lesson, name='Lesson')
LessonOut_Pydantic = pydantic_model_creator(Lesson, name='LessonOut', exclude_readonly=True,
                                            include=('title', 'start_date', 'end_date'))
LessonIn_Pydantic = pydantic_model_creator(Lesson, name='LessonIn', exclude_readonly=True,
                                           exclude=('created_at', 'updated_at', 'teacher', 'students'))
Homework_Pydantic = pydantic_model_creator(Homework, name='Homework')
HomeworkIn_Pydantic = pydantic_model_creator(Homework, name='HomeworkIn', exclude_readonly=True,
                                             exclude=('created_at', 'updated_at'))
Todo_Pydantic = pydantic_model_creator(TodoModel, name='Todo')
TodoIn_Pydantic = pydantic_model_creator(TodoModel, name='TodoIn', exclude_readonly=True,
                                         exclude=('created_at', 'updated_at'))

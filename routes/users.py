from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

# from models.student_model import StudentModel, UpdateStudentModel
from models.student_model import StudentModel

router = APIRouter()

# @router.post("/", response_description="Create a new student", status_code=status.HTTP_201_CREATED, response_model=StudentModel)
# def create_student(request: Request, student: StudentModel = Body(...)):
#     student = jsonable_encoder(student)
#     new_student = request.app.database["students"].insert_one(student)
#     created_student = request.app.database["students"].find_one(
#         {"_id": new_student.inserted_id}
#     )
#     return created_student


@router.get("/", response_description="List all students", response_model=List[StudentModel])
def list_students(request: Request):
    temp = request.app
    # students = list(request.app.database["inventory_db"].find(limit=100))
    return temp


# @router.get("/{id}", response_description="Get a singe student by id", response_model=StudentModel)
# def find_student(id: str, request: Request):
#     if (student := request.app.database["students"].find_one({"_id": id})) is not None:
#         return student

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {id} not found")


# @router.put("/{id}", response_description="Update a book", response_model=Book)
# def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
#     book = {k: v for k, v in book.dict().items() if v is not None}

#     if len(book) >= 1:
#         update_result = request.app.database["books"].update_one(
#             {"_id": id}, {"$set": book}
#         )

#         if update_result.modified_count == 0:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

#     if (
#         existing_book := request.app.database["books"].find_one({"_id": id})
#     ) is not None:
#         return existing_book

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


# @router.delete("/{id}", response_description="Delete a book")
# def delete_book(id: str, request: Request, response: Response):
#     delete_result = request.app.database["books"].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         response.status_code = status.HTTP_204_NO_CONTENT
#         return response

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

# from fastapi import APIRouter
# from models.student_model import StudentModel, UpdateStudentModel
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import Response, JSONResponse
# from fastapi import Body, HTTPException, status
# from typing import List

# router = APIRouter()

# @router.post("/", response_description="Add new student", response_model=StudentModel)
# async def create_student(student: StudentModel = Body(...)):
#     student = jsonable_encoder(student)
#     new_student = await db["students"].insert_one(student)
#     created_student = await db["students"].find_one({"_id": new_student.inserted_id})
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)

# @router.get(
#     "/", response_description="List all students", response_model=List[StudentModel]
# )
# async def list_students():
#     students = await db["students"].find().to_list(1000)
#     return students

# @router.get(
#     "/{id}", response_description="Get a single student", response_model=StudentModel
# )
# async def show_student(id: str):
#     if (student := await db["students"].find_one({"_id": id})) is not None:
#         return student

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")


# @router.put("/{id}", response_description="Update a student", response_model=StudentModel)
# async def update_student(id: str, student: UpdateStudentModel = Body(...)):
#     student = {k: v for k, v in student.dict().items() if v is not None}

#     if len(student) >= 1:
#         update_result = await db["students"].update_one({"_id": id}, {"$set": student})

#         if update_result.modified_count == 1:
#             if (
#                 updated_student := await db["students"].find_one({"_id": id})
#             ) is not None:
#                 return updated_student

#     if (existing_student := await db["students"].find_one({"_id": id})) is not None:
#         return existing_student

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")


# @router.delete("/{id}", response_description="Delete a student")
# async def delete_student(id: str):
#     delete_result = await db["students"].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")
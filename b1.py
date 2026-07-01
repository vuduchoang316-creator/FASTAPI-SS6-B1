from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel,Field

app = FastAPI()

class CreateCourse(BaseModel):
    code: str 
    name: str 
    duration: int = Field(gt=0,description="Phải lớn hơn 0")
    fee: int = Field(ge=0,description="Phải hơn hơn hoặc bằng 0")
class UpdateCourse(BaseModel):
    code: str 
    name: str 
    duration: int = Field(gt=0,description="Phải lớn hơn 0")
    fee: int = Field(ge=0,description="Phải hơn hơn hoặc bằng 0")
courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

@app.get('/courses/{course_id}')
def get_detail(course_id:int):
    detail_course = [course for course in courses if course['id'] == course_id]
    if not detail_course:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy khóa học"
        )
    return {
        "message":"Thông tin chi tiết khóa học",
        "data":detail_course
    }

@app.get('/courses')
def find_course(
    keyword: str|None = None,
    min_fee: int |None = None,
    max_fee: int|None = None
):
    result = courses

    if keyword:
        result = [course for course in courses if keyword.lower() in course['code'].lower() or keyword.lower() in course['name'].lower()]
    
    if min_fee: 
        result = [course for course in courses if min_fee <= course['fee']]
    
    if max_fee:
        result = [course for course in courses if max_fee >= course['fee']]

    return {
        "message":"Danh sách thông tin khóa học",
        "data":result
    }
@app.post('/courses')
def create_course(create_course:CreateCourse):
    new_id = max((course['id'] for course in courses), default= 0) + 1
    new_code = create_course.code.upper()
    if any(new_code == course['code'] and new_id != course['id'] for course in courses):
        raise HTTPException(
            status_code=409,
            detail="Mã môn đã tồn tại"
        )
    courses.append(
        {"id":new_id,**create_course.dict()})
    return {
        "message":"Thêm thành công",
        "data":create_course
    }

@app.put('/courses/{course_id}')
def update_courses(course_id:int,update_course:UpdateCourse):
    for i,course in enumerate(courses):
        if course['id'] == course_id:
            if any(update_course.code == course['code'] and course_id != course['id'] for course in courses):
                raise HTTPException(
                    status_code=409,
                    detail="Mã môn đã tồn tại"
                )
            courses[i].update(update_course.dict())
            return {
                "message":"Cập nhật thành công",
                "data":update_course
            }
    raise HTTPException(
        status_code=404,
        detail="Course not found."
    )

@app.delete('/courses/{course_id}')
def delete_course(course_id:int):
    for course in courses:
        if course['id'] == course_id:
            courses.remove(course)
            return {
                "message":"Xóa khóa học thành công",
                "data":course
            }
    raise HTTPException(
        status_code=404,
        detail='Course not found.'
    )


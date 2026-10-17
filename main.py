# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel


# app = FastAPI(
#     title="Employee Management API",
#     description="Employee CRUD API using in-memory data",
#     version="1.0.0"
# )


# # -----------------------------
# # Pydantic Model
# # -----------------------------

# class Employee(BaseModel):
#     id: int
#     name: str
#     age: int
#     department: str
#     salary: float


# # -----------------------------
# # Temporary Employee Data
# # -----------------------------

# employees = [
#     Employee(
#         id=1,
#         name="Priyanka",
#         age=23,
#         department="IT",
#         salary=50000
#     ),
#     Employee(
#         id=2,
#         name="Rahul",
#         age=27,
#         department="Finance",
#         salary=65000
#     ),
#     Employee(
#         id=3,
#         name="Anitha",
#         age=25,
#         department="HR",
#         salary=48000
#     )
# ]


# # -----------------------------
# # Get All Employees
# # -----------------------------

# @app.get("/employees")
# def get_employees():
#     return employees


# # -----------------------------
# # Get Employee by ID
# # -----------------------------

# @app.get("/employees/{employee_id}")
# def get_employee(employee_id: int):

#     for employee in employees:
#         if employee.id == employee_id:
#             return employee

#     raise HTTPException(
#         status_code=404,
#         detail="Employee not found"
#     )


# # -----------------------------
# # Create Employee
# # -----------------------------

# @app.post("/employees")
# def create_employee(employee: Employee):

#     for existing_employee in employees:
#         if existing_employee.id == employee.id:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Employee ID already exists"
#             )

#     employees.append(employee)

#     return {
#         "message": "Employee created successfully",
#         "employee": employee
#     }


# # -----------------------------
# # Update Employee
# # -----------------------------

# @app.put("/employees/{employee_id}")
# def update_employee(
#     employee_id: int,
#     updated_employee: Employee
# ):

#     for index, employee in enumerate(employees):

#         if employee.id == employee_id:

#             employees[index] = updated_employee

#             return {
#                 "message": "Employee updated successfully",
#                 "employee": updated_employee
#             }

#     raise HTTPException(
#         status_code=404,
#         detail="Employee not found"
#     )


# # -----------------------------
# # Delete Employee
# # -----------------------------

# @app.delete("/employees/{employee_id}")
# def delete_employee(employee_id: int):

#     for index, employee in enumerate(employees):

#         if employee.id == employee_id:

#             deleted_employee = employees.pop(index)

#             return {
#                 "message": "Employee deleted successfully",
#                 "employee": deleted_employee
#             }

#     raise HTTPException(
#         status_code=404,
#         detail="Employee not found"
#     )

from fastapi import FastAPI, HTTPException
from bson import ObjectId

from models import Employee
from database import employees_collection

#created object for FastAPI
#added second comment in github firectly to check fetch command
app = FastAPI(
    title="Employee Management API",
    description="CRUD API using FastAPI and MongoDB",
    version="1.0.0"
)


@app.post("/employees")
def create_employee(employee: Employee):

    employee_data = employee.model_dump()

    result = employees_collection.insert_one(employee_data)

    return {
        "message": "Employee created successfully",
        "employee_id": str(result.inserted_id)
    }


@app.get("/employees")
def get_employees():

    employees = list(employees_collection.find())

    for employee in employees:
        employee["_id"] = str(employee["_id"])

    return employees

# get the details
@app.get("/employees/{employee_id}")
def get_employee(employee_id: str):

    employee = employees_collection.find_one(
        {"_id": ObjectId(employee_id)}
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employee["_id"] = str(employee["_id"])

    return employee


@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: str,
    employee: Employee
):

    result = employees_collection.update_one(
        {"_id": ObjectId(employee_id)},
        {"$set": employee.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee updated successfully"
    }


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):

    result = employees_collection.delete_one(
        {"_id": ObjectId(employee_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully"
    }


@app.get("/mongodb-test")
def mongodb_test():

    try:
        employees_collection.database.client.admin.command("ping")

        return {
            "message": "MongoDB connected successfully"
        }

    except Exception as e:

        return {
            "message": "MongoDB connection failed",
            "error": str(e)
        }

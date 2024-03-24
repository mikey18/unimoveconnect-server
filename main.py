from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
import models
import random
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from functions import hash_password, verify_password
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

#cors
origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#cors

# db
models.Base.metadata.create_all(bind=engine)
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
# db

class Create_User(BaseModel):
    firstname: str
    lastname: str
    matric_no: str
    email: str
    password: str

class Update_User(BaseModel):
    firstname: str
    lastname: str
    matric_no: str
    email: str

class Get_User(BaseModel):
    id: int
    firstname: str
    lastname: str
    matric_no: str
    wallet: Optional[int]  # Allow wallet to be nullable (None)
    email: str
    type: str

class Login_User(BaseModel):
    matric_no: str
    password: str

class Request_Ride(BaseModel):
    from_location: str
    to_location: str
    range: str
    date: str
    clas: str
    seat: int
    bag: int

class Message(BaseModel):
    message: str

class Create_Driver(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    platenumber: str

class Login_Driver(BaseModel):
    email: str
    password: str

class Get_Driver(BaseModel):
    id: int
    firstname: str
    lastname: str
    platenumber: str
    email: str
    type: str

class Update_Driver(BaseModel):
    firstname: str
    lastname: str
    platenumber: str
    email: str

# user
@app.post("/create_user")
def create_user(data: Create_User, db: Session = Depends(get_db)):
    email_exists_user = db.query(models.User).filter(models.User.email == data.email).first()
    email_exists_driver = db.query(models.Driver).filter(models.Driver.email == data.email).first()

    if email_exists_user or email_exists_driver:
        return {
            "status": 400,
            "msg": "email already exists"
        }
    matric_exists = db.query(models.User).filter(models.User.matric_no == data.matric_no).first()
    if matric_exists:
        return {
            "status": 400,
            "msg": "user with matric number alreay exists"
        }
    user_model = models.User()
    user_model.firstname = data.firstname
    user_model.lastname = data.lastname
    user_model.matric_no = data.matric_no
    user_model.email = data.email
    user_model.wallet = 500000
    user_model.password = hash_password(data.password)
    db.add(user_model)
    db.commit()

    user_data = Get_User(
        id=user_model.id,
        firstname=user_model.firstname,
        lastname=user_model.lastname,
        matric_no=user_model.matric_no,
        wallet=user_model.wallet,
        email=user_model.email,
        type='user'
    )
    return {
        "status": 200,
        "data": user_data
    }

@app.post("/login_user")
def login_user(data: Login_User, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.matric_no == data.matric_no).first()
    if user_model and verify_password(data.password, user_model.password):
        user_data = Get_User(
            id=user_model.id,
            firstname=user_model.firstname,
            lastname=user_model.lastname,
            matric_no=user_model.matric_no,
            wallet=user_model.wallet,
            email=user_model.email,
            type='user'
        )
        return {
            "status": 200,
            "data": user_data
        }
    else:
        return {
            "status": 400,
            "msg": "Invalid matric number or password"
        }

@app.put("/update_user")
def update_user(data: Update_User, user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is None:
        return {
            "status": 400,
            "msg": "user does not exist"
        }
    user_model.firstname = data.firstname
    user_model.lastname = data.lastname
    user_model.matric_no = data.matric_no
    user_model.email = data.email
    db.add(user_model)
    db.commit()

    user_data = Get_User(
        id=user_model.id,
        firstname=user_model.firstname,
        lastname=user_model.lastname,
        matric_no=user_model.matric_no,
        wallet=user_model.wallet,
        email=user_model.email,
        type='user'
    )
    return {
        "status": 200,
        "data": user_data
    }

@app.get("/initiate_ride")
def initiate_ride(user_id: int, db: Session = Depends(get_db)):
    ride_exists = db.query(models.Ride).filter(
        models.Ride.user_id == user_id,
        models.Ride.completed == False,
        models.Ride.driver_id.isnot(None)
    ).first()

    if ride_exists:
        return {
            "status": 400,
            "msg": "You already have a trip already"
        }
    
    ride_exists2 = db.query(models.Ride).filter(
        models.Ride.user_id == user_id,
        models.Ride.completed == False,
        models.Ride.driver_id.is_(None)
    ).first()
    
    if ride_exists2:
        db.delete(ride_exists2)
        db.commit()

    data = [
        {
            'id': 1,
            'name': 'Classic',
            'seat': 1,
            'bags': 3,
            'range': f'{random.randint(50, 100) * 10:,} - {random.randint(200, 400) * 10:,}'
        },
        {
            'id': 2,
            'name': 'Premium',
            'seat': 2,
            'bags': 6,
            'range': f'{random.randint(500, 1000) * 10:,} - {random.randint(1100, 1300) * 10:,}'
        },
        {
            'id': 3,
            'name': 'Premium X',
            'seat': 3,
            'bags': 8,
            'range': f'{random.randint(14000, 16000) * 10:,} - {random.randint(18000, 20000) * 10:,}'
        }
    ]
  
    return {
        "status": 200,
        "data": data
    }

# @app.get("/get_price_and_driver")
# def get_price_and_driver(range: str):
#     range_without_commas = range.replace(',', '')
#     lower, upper = map(int, range_without_commas.split(" - "))
#     random_number = random.randint(lower, upper)

#     return {
#         "status": 200,
#         "data": {
#             "driver": {
#                 "name": fake.name(),
#                 "platenumber": fake.license_plate(),
#                 "rating": fake.random_int(min=1, max=5),
#             },
#             "price": random_number
#         }
#     }
    

@app.post("/request_ride")
def request_ride(data: Request_Ride, user_id: int, db: Session = Depends(get_db)):
    ride_exists2 = db.query(models.Ride).filter(
        models.Ride.user_id == user_id,
        models.Ride.completed == False,
        models.Ride.driver_id.is_(None)
    ).first()
    
    if ride_exists2:
        db.delete(ride_exists2)
    
    range_without_commas = data.range.replace(',', '')
    lower, upper = map(int, range_without_commas.split(" - "))
    random_number = random.randint(lower, upper)

    ride_model = models.Ride()
    ride_model.user_id = user_id
    ride_model.from_location = data.from_location
    ride_model.to_location = data.to_location
    ride_model.price = random_number
    ride_model.date = data.date
    ride_model.clas = data.clas
    ride_model.seat = data.seat
    ride_model.bag = data.bag
    # ride_model.driver_name = data.driver_name
    # ride_model.driver_plate = data.driver_plate
    # ride_model.driver_rank = data.driver_rank
    db.add(ride_model)
    db.commit()

    ride_data = {
        "id": ride_model.id,
        "from_location": ride_model.from_location,
        "to_location": ride_model.to_location,
        "price": ride_model.price,
    }
    return {
        "status": 200,
        "data": ride_data
    }

@app.get("/poll_ride")
def poll_ride(user_id: int, db: Session = Depends(get_db)):
    ride = db.query(models.Ride).filter(
        models.Ride.user_id == user_id,
        models.Ride.completed == False,
        models.Ride.cancelled == False
    ).first()

    if ride.driver_id == None:
        return {
            "status": 400,
            "msg": "No driver has accepted"
        }
    else:
        user_model = db.query(models.User).filter(models.User.id == user_id).first()
        # user_model.wallet -= data.price
        # db.add(user_model)
        # db.commit()
        user_data = Get_User(
            id=user_model.id,
            firstname=user_model.firstname,
            lastname=user_model.lastname,
            matric_no=user_model.matric_no,
            wallet=user_model.wallet,
            email=user_model.email,
            type='user'
        )
        return {
            "status": 200,
            "msg": "Driver has accepted",
            "data": user_data
        }

@app.get("/fetch_rides")
def fetch_rides(user_id: int, db: Session = Depends(get_db)):
    ongoing = db.query(models.Ride).filter(models.Ride.user_id == user_id,
                                           models.Ride.driver_id != None,
                                        models.Ride.completed == False).first()
    previous = db.query(models.Ride).filter(models.Ride.user_id == user_id,
                                        models.Ride.completed == True).order_by(models.Ride.id.desc())
    if ongoing: 
        driver = {
            "name": f'{ongoing.driver.firstname} {ongoing.driver.lastname}',
            "platenumber": ongoing.driver.platenumber

        }
        ongoing_data = {
            "id": ongoing.id,
            "from_location": ongoing.from_location,
            "to_location": ongoing.to_location,
            "price": ongoing.price,
            "date": ongoing.date,
            "seat": ongoing.seat,
            "bag": ongoing.bag,
            "class": ongoing.clas,
            "driver": driver
        }
    else:
        ongoing_data = None
    prev = []
    for ride in previous:
        ride_data = {
            "id": ride.id,
            "from_location": ride.from_location,
            "to_location": ride.to_location,
            "price": ride.price,
            "date": ride.date,
            "time": ride.created_at
        }
        prev.append(ride_data)    
    return {
        "status": 200,
        "ongoing": ongoing_data,
        "previous": prev
    }

@app.post("/completed_ride")
def completed_ride(ride_id: int, user_id: int, db: Session = Depends(get_db)):
    ride = db.query(models.Ride).filter(models.Ride.id == ride_id,
                                        models.Ride.completed == False).first()
    if ride:
        ride.completed = True
        db.commit()
        ongoing = db.query(models.Ride).filter(models.Ride.user_id == user_id,
                                        models.Ride.completed == False).first()
        previous = db.query(models.Ride).filter(models.Ride.user_id == user_id,
                                            models.Ride.completed == True).order_by(models.Ride.id.desc())
        if ongoing: 
            ongoing_data = {
                "id": ongoing.id,
                "from_location": ongoing.from_location,
                "to_location": ongoing.to_location,
                "price": ongoing.price,
                "date": ongoing.date,
                "seat": ongoing.seat,
                "bag": ongoing.bag,
                "class": ongoing.clas
            }
        else:
            ongoing_data = None
        prev = []
        for ride in previous:
            ride_data = {
                "id": ride.id,
                "from_location": ride.from_location,
                "to_location": ride.to_location,
                "price": ride.price,
                "date": ride.date,
                "time": ride.created_at
            }
            prev.append(ride_data)    
        return {
            "status": 200,
            "ongoing": ongoing_data,
            "previous": prev
        }
    else:
        return {
            "status": 400,
            "message": "Failed"
        }

@app.post("/post_message")
def post_message(data: Message, user_id: int, db: Session = Depends(get_db)):
    msg = models.Message()
    msg.user_id = user_id
    msg.message = data.message
    db.add(msg)
    db.commit()

    return {
        "status": 200,
    }

# driver
@app.post("/create_driver")
def create_driver(data: Create_Driver, db: Session = Depends(get_db)):
    email_exists_user = db.query(models.User).filter(models.User.email == data.email).first()
    email_exists_driver = db.query(models.Driver).filter(models.Driver.email == data.email).first()

    if email_exists_user or email_exists_driver:
        return {
            "status": 400,
            "msg": "email already exists"
        }
  
    driver_model = models.Driver()
    driver_model.firstname = data.firstname
    driver_model.lastname = data.lastname
    driver_model.email = data.email
    driver_model.password = hash_password(data.password)
    driver_model.platenumber = data.platenumber
    db.add(driver_model)
    db.commit()

    driver_data = Get_Driver(
        id=driver_model.id,
        firstname=driver_model.firstname,
        lastname=driver_model.lastname,
        email=driver_model.email,
        platenumber=driver_model.platenumber,
        type='driver'
    )
    return {
        "status": 200,
        "data": driver_data
    }

@app.post("/login_driver")
def login_driver(data: Login_Driver, db: Session = Depends(get_db)):
    driver_model = db.query(models.Driver).filter(models.Driver.email == data.email).first()
    if driver_model and verify_password(data.password, driver_model.password):
        driver_data = Get_Driver(
            id=driver_model.id,
            firstname=driver_model.firstname,
            lastname=driver_model.lastname,
            email=driver_model.email,
            platenumber=driver_model.platenumber,
            type='driver'
        )
        return {
            "status": 200,
            "data": driver_data
        }
    else:
        return {
            "status": 400,
            "msg": "Invalid email or password"
        }

@app.put("/update_driver")
def update_driver(data: Update_Driver, driver_id: int, db: Session = Depends(get_db)):
    driver_model = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if driver_model is None:
        return {
            "status": 400,
            "msg": "Driver does not exist"
        }
    driver_model.firstname = data.firstname
    driver_model.lastname = data.lastname
    driver_model.platenumber = data.platenumber
    driver_model.email = data.email
    db.add(driver_model)
    db.commit()

    data = Get_Driver(
        id=driver_model.id,
        firstname=driver_model.firstname,
        lastname=driver_model.lastname,
        platenumber=driver_model.platenumber,
        email=driver_model.email,
        type='driver'
    )
    return {
        "status": 200,
        "data": data
    }

@app.get("/driver_poll_rides")
def fetch_rides(driver_id: int, db: Session = Depends(get_db)):
    ride = db.query(models.Ride).filter(models.Ride.driver_id == driver_id,
                                        models.Ride.completed == False,
                                        models.Ride.cancelled == False).first()
    if ride:
        user_data = {
            "firstname": ride.user.firstname,
            "lastname": ride.user.lastname,
            "matric_no": ride.user.matric_no
        }
        ride_data = {
            "id": ride.id,
            "user": user_data,
            "from_location": ride.from_location,
            "to_location": ride.to_location,
            "price": ride.price,
            "date": ride.date,
            "bag": ride.bag,
            "seat": ride.seat,
        }
        return {
            "status": 201,
            "message": "Ongoing trip",
            "data": ride_data
        }
    else:
        rides = db.query(models.Ride).filter(models.Ride.driver_id == None,
                                            models.Ride.completed == False).order_by(models.Ride.id.desc()).all()
        prev = []
        for ride in rides:
            ride_data = {
                "id": ride.id,
                "from_location": ride.from_location,
                "to_location": ride.to_location,
                "price": ride.price,
                "date": ride.date,
                "time": ride.created_at,
                "firstname": ride.user.firstname,
                "lastname": ride.user.lastname,
                "matric_no": ride.user.matric_no,
            }
            prev.append(ride_data)    
        return {
            "status": 200,
            "rides": prev,
        }

@app.post("/accept_ride")
def accept_ride(ride_id: int, driver_id: int, db: Session = Depends(get_db)):
    ride = db.query(models.Ride).filter(models.Ride.id == ride_id,
                                        models.Ride.driver_id == None,
                                        models.Ride.completed == False,
                                        models.Ride.cancelled == False).first()
    if ride:
        ride.driver_id = driver_id
        ride.user.wallet -= ride.price
        db.commit()
        user_data = {
            "firstname": ride.user.firstname,
            "lastname": ride.user.lastname,
            "matric_no": ride.user.matric_no
        }
        ride_data = {
            "id": ride.id,
            "user": user_data,
            "from_location": ride.from_location,
            "to_location": ride.to_location,
            "price": ride.price,
            "date": ride.date,
            "bag": ride.bag,
            "seat": ride.seat,
        }
        return {
            "status": 200,
            "message": "Driver assigned successfully",
            "data": ride_data
        }
    else:
        return {
            "status": 400,
            "message": "Failed"
        }

@app.get("/fetch_driver_rides")
def fetch_rides(driver_id: int, db: Session = Depends(get_db)):
    previous = db.query(models.Ride).filter(models.Ride.driver_id == driver_id,
                                        models.Ride.completed == True).order_by(models.Ride.id.desc()).all()
    prev = []
    for ride in previous:
        ride_data = {
            "id": ride.id,
            "from_location": ride.from_location,
            "to_location": ride.to_location,
            "price": ride.price,
            "date": ride.date,
            "time": ride.created_at
        }
        prev.append(ride_data)    
    return {
        "status": 200,
        "data": prev
    }

@app.post("/post_message2")
def post_message(driver_id: int, data: Message, db: Session = Depends(get_db)):
    msg = models.Message()
    msg.driver_id = driver_id
    msg.message = data.message
    db.add(msg)
    db.commit()

    return {
        "status": 200,
    }

# @app.post("/completed_cancel_ride_driver")
# def completed_ride(driver_id: int, action: str, db: Session = Depends(get_db)):
#     ride = db.query(models.Ride).filter(models.Ride.driver_id == driver_id,
#                                         models.Ride.completed == False,
#                                         models.Ride.cancelled == False).first()
#     if ride:
#         if action == "completed":
#             ride.completed = True
#             db.commit()
#             return {
#                 "status": 200,
#                 "message": "Driver completed ride"
#             }
#         else:
#             ride.cancelled = True
#             db.commit()
#             return {
#                 "status": 200,
#                 "message": "Driver cancelled ride"
#             }
#     else:
#         return {
#             "status": 400,
#             "message": "Failed"
#         }








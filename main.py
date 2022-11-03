from argon2.exceptions  import VerifyMismatchError
from fastapi            import FastAPI, HTTPException, Depends
from fastapi.security   import OAuth2PasswordRequestForm
from typing             import Union, List, Optional
from sqlalchemy.sql     import func
from sqlalchemy         import select
from sqlite3            import IntegrityError, DatabaseError
from datetime           import date, datetime
from dbs                import db, User, Food, FoodEaten, Exercise, ExerciseCompleted
from security           import AuthUser, create_access_token, get_current_user, ph, sha1_hash 
from models             import (
    ExerciseDone,
    ExerciseEntry,
    ExerciseItem,
    ExerciseUpdate,
    FoodEntry,
    FoodItem,
    FoodItemEaten,
    FoodUpdate,
    NewUserInfo, 
    UserInfo,
    UserMeasures
)

# Metadata
tags_metadata = [
    {
        "name": "Auth",
        "description": "User authentication"
    },
    {
        "name": "User",
        "description": "User creates and manages their account"
    },
    {
        "name": "Food Eaten",
        "description": "User manages their food eaten entries"
    },
    {
        "name": "Exercise Done",
        "description": "User manages their exercise completed entries"
    },
    {
        "name": "User Data",
        "description": "Manage user accounts"
    },
    {
        "name": "Food Data",
        "description": "Manage food data items in the cache"
    },
    {
        "name": "Exercise Data",
        "description": "Manage exercise data items in the cache"
    }
]

# FastAPI init
app = FastAPI(openapi_tags=tags_metadata)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Auth
@app.post("/login", tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_id = sha1_hash(form_data.username)
    user = await db.fetch_one(User.select().where(User.c.id == user_id))
    try:
        ph.verify(user.pass_hash, form_data.password)
    except (VerifyMismatchError, AttributeError) as e:
        print(e)
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}                                          # Standard wants this header
        )
    token = create_access_token({
        "sub": user_id
    })
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/current_user", response_model=AuthUser, tags=["Auth"])
async def get_current_user(user: AuthUser = Depends(get_current_user)):
    return user

# Per-user app endpoints
"""
201: User created successfully
409: Email already in use
422: Validation error
"""
@app.post("/user", response_model=UserInfo, tags=["User"], status_code=201)
async def add_user(new_user: NewUserInfo):     
    id = sha1_hash(new_user.email)
    try:
        await db.execute(
            User.insert().values(
                id=id,
                email=new_user.email,
                first_name=new_user.first_name,
                last_name=new_user.last_name,
                pass_hash=ph.hash(new_user.password),
                goal_id=new_user.goal_id,
                birthdate=new_user.birthdate,
                weight=new_user.weight,
                height=new_user.height,
                gender=new_user.gender
            )
        )
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail=f"The email address {new_user.email} is already in use by an account"
        )
    return await db.fetch_one(
        User.select().where(User.c.id == id)
    )

"""
200: Updated succesfully
401: No API key, user session token
403: User session token does not match the given user
404: User does not exist
422: Validation error
"""
@app.put("/user/{id}", response_model=UserInfo, tags=["User"])
async def update_user_measures(id: str, user_measures: UserMeasures, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.id == id and not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )
    
    if not await db.fetch_one(select(User.c.id).where(User.c.id == id)):
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    update_user = User.update().where(User.c.id == id)
    if user_measures.height:
        update_user = update_user.values(height=user_measures.height)
    if user_measures.weight:
        update_user = update_user.values(weight=user_measures.weight)
    await db.execute(update_user)
        
    return await db.fetch_one(
        User.select().where(User.c.id == id)
    )

"""
200: User found
401: No API key, user session token
403: User session token does not match the given user
404: User does not exist
422: Validation error
"""
@app.get("/user/{id}", response_model=UserInfo, tags=["User"])
async def get_user(id: str, auth_user: AuthUser = Depends(get_current_user)):    
    if not auth_user.id == id and not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    user = await db.fetch_one(User.select().where(User.c.id == id))
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )
    return user

"""
201: Created succesfully
401: No API key, user session token
403: User session token does not match the given user
404: User does not exist
409: Food entry already exists
422: Validation error
"""
@app.post("/food_eaten/{user_id}", response_model=FoodItemEaten, tags=["Food Eaten"], status_code=201)
async def create_food_eaten(user_id: str, item: FoodEntry, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.id == user_id and not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )


    if not await db.fetch_one(select([User.c.id]).where(User.c.id == user_id)):
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )
     
    food_id = sha1_hash(item.name)
    food_exists = await db.fetch_val(
        select([Food.c.id]).where(Food.c.id == food_id)
    )
    if not food_exists:
        await db.execute(
            Food.insert().values(
                id=food_id,
                name=item.name,
                calories=item.calories,
                total_fat=item.macros.total_fat,
                saturated_fat=item.macros.saturated_fat,
                cholesterol=item.macros.cholesterol,
                sodium=item.macros.sodium,
                carbohydrates=item.macros.carbohydrates,
                dietary_fiber=item.macros.dietary_fiber,
                sugars=item.macros.sugars,
                protein=item.macros.protein,
                serving_qty=item.serving_qty,
                serving_unit=item.serving_unit,
                serving_weight=item.serving_weight,
                image_url=item.image_url
            )
        )

    try:
        await db.execute(
            FoodEaten.insert().values(
                user_id=user_id,
                food_id=food_id,
                time_consumed=item.time_eaten,
                servings=item.num_servings
            )
        )
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=409, 
            detail=f"Food {food_id} already exists for user {user_id} at {item.time_eaten}"
        )

    return await db.fetch_one(
        FoodEaten.select().where(
            FoodEaten.c.user_id == user_id,
            FoodEaten.c.food_id == food_id,
            FoodEaten.c.time_consumed == item.time_eaten
        )
    )

"""
204: Deleted successfully
401: No API key, user session token
403: User session token does not match the given user
422: Validation error
"""
@app.delete("/food_eaten", tags=["Food Eaten"], status_code=204)
async def delete_food_eaten(uid: str, fid: str, time: datetime, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.id == uid and not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    await db.execute(
        FoodEaten.delete().where(
            FoodEaten.c.user_id == uid,
            FoodEaten.c.food_id == fid,
            FoodEaten.c.time_consumed == time
        )
    )
    
"""
200: Search successful
401: No API key, user session token
403: User session token does not match the given user
422: Validation error
"""
@app.get("/food_eaten", response_model=List[FoodItemEaten], tags=["Food Eaten"])
async def get_food_eaten(user_id: str, food_id: Optional[str] = None, time_consumed: Optional[Union[date, datetime]] = None, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.id == user_id and not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    select_food_items = FoodEaten.select().where(FoodEaten.c.user_id == user_id)
    if food_id:
        select_food_items = select_food_items.where(FoodEaten.c.food_id == food_id)
    if type(time_consumed) == datetime:
        select_food_items = select_food_items.where(FoodEaten.c.time_consumed == time_consumed)
    elif type(time_consumed) == date:
        select_food_items = select_food_items.where(
            func.date(func.datetime(FoodEaten.c.time_consumed, "localtime")) == time_consumed
        )
    return await db.fetch_all(
        select_food_items.order_by(FoodEaten.c.time_consumed.desc())
    )

"""
201: Created successfully
401: No API key, user session token
403: User session token does not match the given user
404: User does not exist
409: Exercise entry already exists
422: Validation error
"""
@app.post("/exercise_done/{user_id}", response_model=ExerciseDone, tags=["Exercise Done"], status_code=201)
async def create_exercise_done(user_id: str, item: ExerciseEntry, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.id == user_id and not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    if not await db.fetch_one(select([User.c.id]).where(User.c.id == user_id)):
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    exercise_id = sha1_hash(item.name)
    exercise_exists = await db.fetch_val(
        Exercise.select().where(Exercise.c.id == exercise_id)
    )
    if not exercise_exists:
        await db.execute(
            Exercise.insert().values(
                id=exercise_id,
                name=item.name,
                calories_per_hour=item.calories_per_hour
            )
        )

    try:
        await db.execute(
            ExerciseCompleted.insert().values(
                user_id=user_id,
                exercise_id=exercise_id,
                time_completed=item.time_completed,
                duration=item.duration
            )
        )
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=409, 
            detail=f"Exercise entry {exercise_id} for {user_id} at {item.time_completed} already exists"
        )

    return await db.fetch_one(
        ExerciseCompleted.select().where(
            ExerciseCompleted.c.user_id == user_id,
            ExerciseCompleted.c.exercise_id == exercise_id,
            ExerciseCompleted.c.time_completed == item.time_completed
        )
    )

"""
204: Deleted successfully
401: No API key, user session token
403: User session token does not match the given user
422: Validation error
"""
@app.delete("/exercise_done", tags=["Exercise Done"], status_code=204)
async def delete_exercise_done(uid: str, eid: str, time: datetime, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.id == uid and not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    await db.execute(
        ExerciseCompleted.delete().where(
            ExerciseCompleted.c.user_id == uid,
            ExerciseCompleted.c.exercise_id == eid,
            ExerciseCompleted.c.time_completed == time
        )
    )

"""
200: Search successful
401: No API key, user session token
403: User session token does not match the given user
422: Validation error
"""
@app.get("/exercise_done", response_model=List[ExerciseDone], tags=["Exercise Done"])
async def get_exercise_done(user_id: str, exercise_id: Optional[str] = None, time_completed: Optional[Union[date, datetime]] = None, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.id == user_id and not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    select_exercise_items = ExerciseCompleted.select().where(ExerciseCompleted.c.user_id == user_id)
    if exercise_id:
        select_exercise_items = select_exercise_items.where(ExerciseCompleted.c.exercise_id == exercise_id)
    if type(time_completed) == datetime:
        select_exercise_items = select_exercise_items.where(ExerciseCompleted.c.time_completed == time_completed)
    elif type(time_completed) == date:
        select_exercise_items = select_exercise_items.where(
            func.date(func.datetime(ExerciseCompleted.c.time_completed, "localtime")) == time_completed
        )
    return await db.fetch_all(
        select_exercise_items.order_by(ExerciseCompleted.c.time_completed.desc())
    )

# General app endpoints
"""
200: Search successful
422: Validation error
"""
@app.get("/food", response_model=List[FoodItem], tags=["Food Data"])
async def get_food_item(id: Optional[str] = None, name: Optional[str] = None):
    food_select = Food.select()
    if id:
        food_select = food_select.where(Food.c.id == id)
    elif name:
        food_select = food_select.where(Food.c.name.like(name))
    return await db.fetch_all(food_select.order_by(Food.c.name.desc()))

"""
200: Search successful
422: Validation error
"""
@app.get("/exercise", response_model=List[ExerciseItem], tags=["Exercise Data"])
async def get_exercise_item(id: Optional[str] = None, name: Optional[str] = None):
    exercise_select = Exercise.select()
    if id:
        exercise_select = exercise_select.where(Exercise.c.id == id)
    elif name:
        exercise_select = exercise_select.where(Exercise.c.name.like(name))
    return await db.fetch_all(exercise_select.order_by(Exercise.c.name.desc()))

# Admin endpoints
"""
204: Deleted successfully
401: No API key, user session token
403: Invalid API key
422: Validation error
"""
@app.delete("/user/{id}", tags=["User Data"], status_code=204)
async def delete_user(id: str, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    await db.execute(
        User.delete().where(User.c.id == id)
    )

"""
200: Search successful
401: No API key, user session token
403: Invalid API key
422: Validation error
"""
@app.get("/users", response_model=List[UserInfo], tags=["User Data"])
async def get_users(auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    return await db.fetch_all(
        User.select()
    )

"""
200: Updated succesfully
401: No API key, user session token
403: Invalid API key
404: Food does not exist
422: Validation error
"""
@app.put("/food/{id}", response_model=FoodItem, tags=["Food Data"])
async def update_food_item(id: str, update: FoodUpdate, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    if not await db.fetch_one(select([Food.c.id]).where(Food.c.id == id)):
        raise HTTPException(
            status_code=404,
            detail=f"Food {id} does note exist"
        )

    await db.execute(
        Food.update().where(Food.c.id == id).values(
            calories=update.calories,
            total_fat=update.total_fat,
            saturated_fat=update.saturated_fat,
            cholesterol=update.cholesterol,
            sodium=update.sodium,
            carbohydrates=update.carbohydrates,
            dietary_fiber=update.dietary_fiber,
            sugars=update.sugars,
            protein=update.protein,
            serving_qty=update.serving_qty,
            serving_unit=update.serving_unit,
            serving_weight=update.serving_weight,
            image_url=update.image_url
        )
    )
    return await db.fetch_one(
        Food.select().where(Food.c.id == id)
    )

"""
204: Deleted successfully
401: No API key, user session token
403: Invalid API key
422: Validation error
"""
@app.delete("/food/{id}", tags=["Food Data"], status_code=204)
async def delete_food_item(id: str, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    await db.execute(Food.delete().where(Food.c.id == id))

"""
200: Updated succesfully
401: No API key, user session token
403: Invalid API key
404: Food does not exist
422: Validation error
"""
@app.put("/exercise_item/{id}", response_model=ExerciseItem, tags=["Exercise Data"])
async def update_exercise_item(id: str, update: ExerciseUpdate, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )

    if not await db.fetch_one(select([Exercise.c.id]).where(Exercise.c.id == id)):
        raise HTTPException(
            status_code=404,
            detail=f"Exercise {id} does not exist"
        )

    await db.execute(
        Exercise.update().where(Exercise.c.id == id).values(
            calories_per_hour=update.calories_per_hour
        )
    )
    return await db.fetch_one(
        Exercise.select().where(Exercise.c.id == id)
    )

"""
204: Deleted successfully
401: No API key, user session token
403: Invalid API key
422: Validation error
"""
@app.delete("/exercise_item/{id}", tags=["Exercise Data"], status_code=204)
async def delete_exercise_item(id: str, auth_user: AuthUser = Depends(get_current_user)):
    if not auth_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized user"
        )
    
    await db.execute(Exercise.delete().where(Exercise.c.id == id))
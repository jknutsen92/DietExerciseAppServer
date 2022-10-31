from fastapi    import FastAPI
from typing     import Union, List, Optional
from datetime   import date, datetime
from hashlib    import sha1
from argon2     import PasswordHasher
from dbs        import db, User, Food, FoodEaten, Exercise, ExerciseCompleted
from models     import (
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

# Init dependenices
ph = PasswordHasher()
sha = sha1()

# Metadata
tags_metadata = [
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

# Per-user app endpoints
@app.post("/user", response_model=UserInfo, tags=["User"])
async def add_user(new_user: NewUserInfo):
    id = await db.execute(
        User.insert().values(
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email,
            pass_hash=ph.hash(new_user.password),
            goal_id=new_user.goal_id,
            birthdate=new_user.birthdate,
            weight=new_user.weight,
            height=new_user.height,
            gender=new_user.gender
        )
    )
    return await db.fetch_one(
        User.select().where(User.c.id == id)
    )

@app.put("/user/{id}", response_model=UserInfo, tags=["User"])
async def update_user_measures(id: int, user_measures: UserMeasures):
    #TODO: Ensure user is authorized for this id, check request headers for session token
    if user_measures.height:
        await db.execute(
            User.update().where(User.c.id == id).values(
                weight=user_measures.weight,
                height=user_measures.height
            )
        )
    else:
        await db.execute(
            User.update().where(User.c.id == id).values(
                weight=user_measures.weight,
                height=user_measures.height
            )
        )
    return await db.fetch_one(
        User.select().where(User.c.id == id)
    )

@app.get("/user/{id}", response_model=UserInfo, tags=["User"])
async def get_user(id: int):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    return await db.fetch_one(
        User.select().where(User.c.id == id)
    )

@app.post("/food_eaten/{user_id}", response_model=FoodItemEaten, tags=["Food Eaten"])
async def create_food_entry(user_id: int, item: FoodEntry):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    food_id = sha.update(item.name.encode("utf-8")).hexdigest()
    food_exists = await db.fetch_val(
        Food.select(1).where(Food.c.id == food_id)
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
    await db.execute(
        FoodEaten.insert().values(
            user_id=user_id,
            food_id=food_id,
            time_consumed=item.time_eaten,
            servings=item.num_servings
        )
    )
    return await db.fetch_one(
        FoodEaten.select().where(
            FoodEaten.c.user_id == user_id,
            FoodEaten.c.food_id == food_id,
            FoodEaten.c.time_consumed == item.time_eaten
        )
    )


@app.delete("/food_eaten", tags=["Food Eaten"])
async def delete_food_entry(uid: int, fid: str, time: datetime):
    #TODO: Ensure user is authorized for this id, check request headers for session token
    await db.execute(
        FoodEaten.delete().where(
            FoodEaten.c.user_id == uid,
            FoodEaten.c.food_id == fid,
            FoodEaten.c.time_consumed == time
        )
    )
    

@app.get("/food_eaten", response_model=List[FoodItemEaten], tags=["Food Eaten"])
async def get_food_items(user_id: int, food_id: Optional[str] = None, time_consumed: Optional[Union[date, datetime]] = None):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    select_food_items = FoodEaten.select().where(FoodEaten.c.user_id == user_id)
    if food_id:
        select_food_items = select_food_items.where(FoodEaten.c.food_id == food_id)
    if time_consumed:
        select_food_items = select_food_items.where(FoodEaten.c.time_consumed == time_consumed)
    return await db.fetch_all(
        select_food_items.order_by(FoodEaten.c.time_consumed.desc())
    )


@app.post("/exercise_done/{user_id}", response_model=ExerciseDone, tags=["Exercise Done"])
async def create_exercise_item(user_id: int, item: ExerciseEntry):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    exercise_id = sha.update(item.name.encode("utf-8")).hexdigest()
    exercise_exists = await db.fetch_val(
        Exercise.select(1).where(Exercise.c.id == exercise_id)
    )
    if not exercise_exists:
        await db.execute(
            Exercise.insert().values(
                id=exercise_id,
                name=item.name,
                calories_per_hour=item.calories_per_hour
            )
        )
    await db.execute(
        ExerciseCompleted.insert().values(
            user_id=user_id,
            exercise_id=exercise_id,
            time_completed=item.time_completed,
            duration=item.duration
        )
    )
    return await db.fetch_one(
        ExerciseCompleted.select().where(
            ExerciseCompleted.c.user_id == user_id,
            ExerciseCompleted.c.exercise_id == exercise_id,
            ExerciseCompleted.c.time_completed == item.time_completed
        )
    )

@app.delete("/exercise_done", tags=["Exercise Done"])
async def delete_food_entry(uid: int, eid: str, time: datetime):
    #TODO: Ensure user is authorized for this id, check request headers for session token
    await db.execute(
        ExerciseCompleted.delete().where(
            ExerciseCompleted.c.user_id == uid,
            ExerciseCompleted.c.exercise_id == eid,
            ExerciseCompleted.c.time_consumed == time
        )
    )

@app.get("/exercise_done", response_model=List[ExerciseDone], tags=["Exercise Done"])
async def get_food_items(user_id: int, exercise_id: Optional[str] = None, time_completed: Optional[Union[date, datetime]] = None):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    select_exercise_items = ExerciseCompleted.select().where(ExerciseCompleted.c.user_id == user_id)
    if exercise_id:
        select_exercise_items = select_exercise_items.where(ExerciseCompleted.c.exercise_id == exercise_id)
    if time_completed:
        select_exercise_items = select_exercise_items.where(ExerciseCompleted.c.time_completed == time_completed)
    return await db.fetch_all(
        select_exercise_items.order_by(ExerciseCompleted.c.time_completed.desc())
    )

# General app endpoints
@app.get("/food", response_model=List[FoodItem], tags=["Food Data"])
async def get_food_items(id: Optional[str] = None, name: Optional[str] = None):
    food_select = Food.select()
    if id:
        food_select = food_select.where(Food.c.id == id)
    elif name:
        food_select = food_select.where(Food.c.name.like(name))
    return await db.fetch_all(food_select.order_by(Food.c.name.desc()))

@app.get("/exercise", response_model=List[ExerciseItem], tags=["Exercise Data"])
async def get_exercise_item(id: Optional[str] = None, name: Optional[str] = None):
    #TODO: Error handling
    exercise_select = Exercise.select()
    if id:
        exercise_select = exercise_select.where(Exercise.c.id == id)
    elif name:
        exercise_select = exercise_select.where(Exercise.c.name.like(name))
    return await db.fetch_all(exercise_select.order_by(Exercise.c.name.desc()))

# Admin endpoints
@app.delete("/user/{id}", tags=["User Data"])
async def delete_user(id: int):
    # TODO: ensure user is an admin, check request headers for admin token
    # TODO: Error handling
    await db.execute(
        User.delete().where(User.c.id == id)
    )

@app.get("/users", response_model=List[UserInfo], tags=["User Data"])
async def get_users():
    # TODO: ensure user is an admin, check request headers for admin token
    return await db.fetch_all(
        User.select()
    )

@app.put("/food/{id}", response_model=FoodItem, tags=["Food Data"])
async def update_food_item(id: str, update: FoodUpdate):
    # TODO: ensure user is an admin, check request headers for admin token
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

@app.delete("/food/{id}", tags=["Food Data"])
async def delete_food_item(id: str):
    # TODO: ensure user is an admin, check request headers for admin token
    await db.execute(Food.delete().where(Food.c.id == id))

@app.put("/exercise_item/{id}", response_model=ExerciseItem, tags=["Exercise Data"])
async def update_exercise_item(id: str, update: ExerciseUpdate):
    # TODO: ensure user is an admin, check request headers for admin token
    await db.execute(
        Exercise.update().where(Exercise.c.id == id).values(
            calories_per_hour=update.calories_per_hour
        )
    )
    return await db.fetch_one(
        Exercise.select().where(Exercise.c.id == id)
    )

@app.delete("/exercise_item/{id}", tags=["Exercise Data"])
async def delete_exercise_item(id: str):
    # TODO: ensure user is an admin, check request headers for admin token
    await db.execute(Exercise.delete().where(Exercise.c.id == id))
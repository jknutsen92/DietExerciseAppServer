import time
from fastapi    import FastAPI, Depends
from typing     import Union
from datetime   import date, datetime
from hashlib    import sha1
from argon2     import PasswordHasher
from dbs        import db, User, Food, FoodEaten, Exercise, ExerciseCompleted
from models     import (
    ExerciseDone,
    ExerciseEntry,
    ExerciseItem,
    FoodEntry,
    FoodItem,
    FoodItemEaten,
    NewUserInfo, 
    UserInfo,
    UserMeasures
)

# Init dependenices
ph = PasswordHasher()
sha = sha1()

# FastAPI init
app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Per-user app endpoints
@app.post("/user", response_model=UserInfo)
async def add_user(new_user: NewUserInfo):
    id = await db.execute(
        User.insert().values(
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email,
            pash_hash=ph.hash(new_user.password),
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

@app.put("/user/{id}", response_model=UserInfo)
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

@app.get("/user/{id}", response_model=UserInfo)
async def get_user(id: int):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    return await db.fetch_one(
        User.select().where(User.c.id == id)
    )

@app.post("/new_food_entry/{user_id}", response_model=FoodItemEaten)
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


@app.delete("/delete_food_entry", response_model=None)
async def delete_food_entry(uid: int, fid: str, time: datetime):
    #TODO: Ensure user is authorized for this id, check request headers for session token
    await db.execute(
        FoodEaten.delete().where(
            user_id=uid,
            food_id=fid,
            time_consumed=time
        )
    )
    

@app.get("/food_items_eaten", response_model=[FoodItemEaten])
async def get_food_items(user_id: int, food_id: Union[str, None] = None, time_consumed: Union[date, datetime, None] = None):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    select_food_items = FoodEaten.select().where(FoodEaten.c.user_id == user_id)
    if food_id:
        select_food_items = select_food_items.where(FoodEaten.c.food_id == food_id)
    if time_consumed:
        select_food_items = select_food_items.where(FoodEaten.c.time_consumed == time_consumed)
    return await db.fetch_all(
        select_food_items.order_by(FoodEaten.c.time_consumed.desc())
    )
    


@app.post("/new_exercise_entry", response_model=ExerciseDone)
async def create_exercise_item(item: ExerciseEntry):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    pass


# General app endpoints
@app.get("/food_items", response_model=[FoodItem])
async def get_food_items():
    pass

@app.get("/food_item/{id}", response_model=FoodItem)
async def get_food_item(id: str):
    pass

@app.get("/exercise_items", response_model=[ExerciseItem])
async def get_exercise_items():
    pass

@app.get("/exercise_item/{id}", response_model=ExerciseItem)
async def get_exercise_item(id: str):
    pass

# Admin endpoints
@app.delete("/user/{id}", response_model=None)
async def delete_user(id: int):
    # TODO: ensure user is an admin, check request headers for admin token
    pass

@app.get("/users", response_model=[UserInfo])
async def get_users():
    # TODO: ensure user is an admin, check request headers for admin token
    return await db.fetch_all(
        User.select()
    )

@app.put("/food_item/{id}", response_model=FoodItem)
async def update_food_item(id: str):
    # TODO: ensure user is an admin, check request headers for admin token
    pass

@app.delete("/food_item/{id}", response_model=None)
async def delete_food_item(id: str):
    # TODO: ensure user is an admin, check request headers for admin token
    pass

@app.put("/exercise_item/{id}", response_model=ExerciseItem)
async def update_exercise_item(id: str):
    # TODO: ensure user is an admin, check request headers for admin token
    pass

@app.delete("/exercise_item/{id}", response_model=None)
async def delete_exercise_item(id: str):
    # TODO: ensure user is an admin, check request headers for admin token
    pass
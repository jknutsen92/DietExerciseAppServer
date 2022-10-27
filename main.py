from fastapi    import FastAPI, Depends
from typing     import List, Union
from datetime   import date, datetime
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

# FastAPI init
app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Example endpoints
@app.get("/", response_model=str)
async def welcome():
    return "Hello, client!"

@app.post("/item/", response_model=Item)
async def create_item(details: ItemDetails):
    insert = items.insert().values(
        name=details.name,
        description=details.description,
        owner_id=details.owner_id
    )
    id = await db.execute(insert)
    
    select = items.select().where(items.c.id == id)
    return await db.fetch_one(select)


@app.get("/all_items/", response_model=List[Item])
async def get_all_items():
    select = items.select()
    return await db.fetch_all(select)

@app.get("/item/{item_id}", response_model=Item)
async def get_item(item_id: int):
    select = items.select().where(items.c.id == item_id)
    return await db.fetch_one(select)

@app.put("/item/{item_id}", response_model=Item)
async def update_item(item_id: int, details: ItemDetails):
    update = items.update().where(items.c.id == item_id).values(
        name=details.name,
        description=details.description,
        owner_id=details.owner_id
    )
    id = await db.execute(update)

    select = items.select().where(items.c.id == id)
    return await db.fetch_one(select)

@app.delete("/item/{item_id}", response_model=int)
async def delete_item(item_id: int):
    delete = items.delete().where(items.c.id == item_id)
    return await db.execute(delete)


# Per-user app endpoints
@app.post("/user", response_model=UserInfo)
async def add_user(new_user: NewUserInfo):
    pass

@app.put("/user/{id}", response_model=UserInfo)
async def update_user_measures(id: int, user_measures: UserMeasures):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    pass

@app.get("/user/{id}", response_model=UserInfo)
async def get_user(id: int):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    pass

@app.post("/new_food_entry", response_model=FoodItemEaten)
async def create_food_entry(item: FoodEntry):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    pass

@app.delete("/delete_food_entry", response_model=None)
async def delete_food_entry(user_id: int, food_id: str, time_consumed: datetime):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    pass

@app.get("/food_items_eaten", response_model=[FoodItemEaten])
async def get_food_items(user_id: int, food_id: Union[str, None] = None, time_consumed: Union[datetime, None] = None):
    #TODO: Ensure user is authorized for this id, check request headers for session token 
    pass

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
    pass

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
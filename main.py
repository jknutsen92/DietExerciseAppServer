from fastapi    import FastAPI, Depends
from pydantic   import BaseModel
from typing     import Optional, List
from dbs        import db, items

# Data Validation
class Item(BaseModel):
    id:             int
    name:           str
    description:    Optional[str]
    owner_id:       int

class ItemDetails(BaseModel):
    name:           str
    description:    Optional[str]
    owner_id:       int


# FastAPI Init
app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# FastAPIs
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
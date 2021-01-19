import databases
import sqlalchemy
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.config import Config
from starlette.routing import Route

config = Config('.env')
DATABASE_URL = config('DATABASE_URL')

metadata = sqlalchemy.MetaData()

contacts = sqlalchemy.Table(
    "contacts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("number", sqlalchemy.String),
)

database = databases.Database(DATABASE_URL)

async def get_list_of_contacts(request):
    query = contacts.select()
    results = await database.fetch_all(query)
    content = [{
        "name": result['name'],
        "number": result["number"]
    } for result in results ]

    return JSONResponse(content)


async def add_contact(request):
    data = await request.json()
    query = contacts.insert().values(
        name=data["name"],
        number=data["number"]
    )
    await database.execute(query)
    return JSONResponse({
        "name": data["name"],
        "number": data["number"]
    })


async def get_one_contact(request, id):
    query = contacts.select().where(contacts["id"]==id)
    results = await database.fetch_all(query)
    content = [{
        "name": result['name'],
        "number": result["number"]
    } for result in results ]

    return JSONResponse(content)


async def delete_contact(request, id):
    data = await request.json()
    query = contacts.delete().where(contacts["id"==id]).values(
        name=data["name"],
        number=data["number"]
    )
    await database.execute(query)
    return JSONResponse({
        "name": data["name"],
        "number": data["number"]
    })


async def update_contact(request, id):
    data = await request.json()
    query = contacts.update().where(contacts["id"==id]).values(
        name=data["name"],
        number=data["number"]
    )
    await database.execute(query)
    return JSONResponse({
        "name": data["name"],
        "number": data["number"]
    })


routes = [
    Route("/contacts", endpoint=get_list_of_contacts, methods=["GET"]),
    Route("/contacts", endpoint=add_contact, methods=["POST"]),
    Route("/contacts/{id}", endpoint=get_one_contact, methods=["GET"]),
    Route("/contacts/{id}", endpoint=delete_contact, methods=["DELETE"]),
    Route("/contacts/{id}", endpoint=update_contact, methods=["UPDATE"])
]

app = Starlette(
    routes=routes,
    on_startup=[database.connect],
    on_shutdown=[database.disconnect]
)
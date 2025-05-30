# api.py
import os
import datetime
from typing import List, Optional, Dict

from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# ─── Setup ──────────────────────────────────────────────────────────────────────

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")  
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()
projects_col = db["projects"]
folders_col  = db["folders"]
pages_col    = db["pages"]

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# ─── FastAPI App ────────────────────────────────────────────────────────────────

app = FastAPI(title="NeuroProject Manager API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Models ─────────────────────────────────────────────────────────────────────

class ProjectBase(BaseModel):
    title: str
    description: str

class Project(ProjectBase):
    id: PyObjectId
    created_date: datetime.datetime
    last_updated: datetime.datetime

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime.datetime: lambda dt: dt.isoformat()
        }

class FolderBase(BaseModel):
    name: str
    parent_id: Optional[PyObjectId] = None

class Folder(FolderBase):
    id: PyObjectId
    project_id: PyObjectId
    pages: List[PyObjectId] = []
    subfolders: List[PyObjectId] = []

    class Config:
        json_encoders = {ObjectId: str}

class PageBase(BaseModel):
    title: str
    content: str

class Page(PageBase):
    id: PyObjectId
    folder_id: PyObjectId

    class Config:
        json_encoders = {ObjectId: str}

# ─── Project CRUD ────────────────────────────────────────────────────────────────

@app.post("/projects/", response_model=Project, status_code=201)
async def create_project(p: ProjectBase):
    now = datetime.datetime.utcnow()
    doc = p.dict()
    doc.update({"created_date": now, "last_updated": now})
    res = await projects_col.insert_one(doc)
    proj = await projects_col.find_one({"_id": res.inserted_id})
    proj["id"] = proj.pop("_id")
    return proj

@app.get("/projects/", response_model=List[Project])
async def list_projects():
    out = []
    async for proj in projects_col.find({}):
        proj["id"] = proj.pop("_id")
        out.append(proj)
    return out

@app.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str = Path(...)):
    oid = ObjectId(project_id)
    proj = await projects_col.find_one({"_id": oid})
    if not proj:
        raise HTTPException(404, "Project not found")
    proj["id"] = proj.pop("_id")
    return proj

@app.put("/projects/{project_id}", response_model=Project)
async def update_project(
    project_id: str = Path(...),
    p: ProjectBase = Body(...)
):
    oid = ObjectId(project_id)
    now = datetime.datetime.utcnow()
    update_data = p.dict()
    update_data["last_updated"] = now
    res = await projects_col.update_one({"_id": oid}, {"$set": update_data})
    if res.matched_count == 0:
        raise HTTPException(404, "Project not found")
    proj = await projects_col.find_one({"_id": oid})
    proj["id"] = proj.pop("_id")
    return proj

@app.delete("/projects/{project_id}")
async def delete_project(project_id: str = Path(...)):
    oid = ObjectId(project_id)
    res = await projects_col.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(404, "Project not found")
    return {"status": "deleted"}

# ─── Folder CRUD ────────────────────────────────────────────────────────────────

@app.post(
    "/projects/{project_id}/folders/",
    response_model=Folder,
    status_code=201
)
async def create_folder(
    project_id: str = Path(...),
    data: FolderBase = Body(...)
):
    proj_oid = ObjectId(project_id)
    doc = data.dict()
    doc.update({"project_id": proj_oid, "pages": [], "subfolders": []})
    res = await folders_col.insert_one(doc)
    f = await folders_col.find_one({"_id": res.inserted_id})
    f["id"] = f.pop("_id")
    return f

@app.get("/projects/{project_id}/folders/", response_model=List[Folder])
async def list_folders(project_id: str = Path(...)):
    proj_oid = ObjectId(project_id)
    out = []
    async for f in folders_col.find({"project_id": proj_oid}):
        f["id"] = f.pop("_id")
        out.append(f)
    return out

@app.get("/folders/{folder_id}", response_model=Folder)
async def get_folder(folder_id: str = Path(...)):
    oid = ObjectId(folder_id)
    f = await folders_col.find_one({"_id": oid})
    if not f:
        raise HTTPException(404, "Folder not found")
    f["id"] = f.pop("_id")
    return f

@app.put("/folders/{folder_id}", response_model=Folder)
async def update_folder(
    folder_id: str = Path(...),
    data: FolderBase = Body(...)
):
    oid = ObjectId(folder_id)
    update_data = data.dict(exclude_unset=True)
    res = await folders_col.update_one({"_id": oid}, {"$set": update_data})
    if res.matched_count == 0:
        raise HTTPException(404, "Folder not found")
    f = await folders_col.find_one({"_id": oid})
    f["id"] = f.pop("_id")
    return f

@app.delete("/folders/{folder_id}")
async def delete_folder(folder_id: str = Path(...)):
    oid = ObjectId(folder_id)
    res = await folders_col.delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(404, "Folder not found")
    return {"status": "deleted"}

# ─── Page CRUD ─────────────────────────────────────────────────────────────────

@app.post(
    "/folders/{folder_id}/pages/",
    response_model=Page,
    status_code=201
)
async def create_page(
    folder_id: str = Path(...),
    data: PageBase = Body(...)
):
    f_oid = ObjectId(folder_id)
    doc = data.dict()
    doc["folder_id"] = f_oid
    res = await pages_col.insert_one(doc)
    p = await pages_col.find_one({"_id": res.inserted_id})
    p["id"] = p.pop("_id")
    await folders_col.update_one(
        {"_id": f_oid},
        {"$push": {"pages": res.inserted_id}}
    )
    return p

@app.get("/folders/{folder_id}/pages/", response_model=List[Page])
async def list_pages(folder_id: str = Path(...)):
    f_oid = ObjectId(folder_id)
    out = []
    async for p in pages_col.find({"folder_id": f_oid}):
        p["id"] = p.pop("_id")
        out.append(p)
    return out

@app.get("/pages/{page_id}", response_model=Page)
async def get_page(page_id: str = Path(...)):
    oid = ObjectId(page_id)
    p = await pages_col.find_one({"_id": oid})
    if not p:
        raise HTTPException(404, "Page not found")
    p["id"] = p.pop("_id")
    return p

@app.put("/pages/{page_id}", response_model=Page)
async def update_page(
    page_id: str = Path(...),
    data: PageBase = Body(...)
):
    oid = ObjectId(page_id)
    update_data = data.dict(exclude_unset=True)
    res = await pages_col.update_one({"_id": oid}, {"$set": update_data})
    if res.matched_count == 0:
        raise HTTPException(404, "Page not found")
    p = await pages_col.find_one({"_id": oid})
    p["id"] = p.pop("_id")
    return p

@app.delete("/pages/{page_id}")
async def delete_page(page_id: str = Path(...)):
    oid = ObjectId(page_id)
    page = await pages_col.find_one({"_id": oid})
    if not page:
        raise HTTPException(404, "Page not found")
    await folders_col.update_one(
        {"_id": page["folder_id"]},
        {"$pull": {"pages": oid}}
    )
    await pages_col.delete_one({"_id": oid})
    return {"status": "deleted"}

# app/api/file.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
import os
from app.api.deps import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/files", tags=["files"])

# 如果 uploads 文件夹不存在则自动创建
if not os.path.exists(settings.STORAGE_PATH):
    os.makedirs(settings.STORAGE_PATH)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    file_location = f"{settings.STORAGE_PATH}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    return {"filename": file.filename, "message": "File uploaded successfully"}

@router.get("/download/{filename}")
async def download_file(filename: str, current_user=Depends(get_current_user)):
    file_location = f"{settings.STORAGE_PATH}/{filename}"
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_location, media_type="application/octet-stream", filename=filename)

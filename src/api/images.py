import shutil

from fastapi import APIRouter, UploadFile

from src.api.dependencies import DBDep

router = APIRouter(prefix='/images', tags=['Фото'])


@router.post("")
def upload_image(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

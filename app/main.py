import gradio as gr
from fastapi import FastAPI, UploadFile, Depends
from .database import engine, get_db
from sqlalchemy.orm import Session
from .models import Base, IdentityCard
from .crud import (
    save_uploaded_file,
    create_upload_directory,
    save_inference_result_to_json,
    save_identity_card_from_json,
    show_inference_result,
    delete_existing_png_files,
    create_json_file,
    get_latest_path,
    delete_content_in_json
    
)
from typing import Annotated, List
from .schemas import IdentityCardRequest, IdentityCardResponse
from .gradio_ui import create_gradio_ui

app = FastAPI()

Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/identity_cards/save_file/")
async def save_file(file: UploadFile):
    file_dir = create_upload_directory()
    delete_existing_png_files(file_dir)
    file_full_path = save_uploaded_file(file, file_dir)
    return {"message": file_full_path}


@app.get("/identity_cards/show_inference_results/", response_model=IdentityCardRequest)
async def show_inference_results():

    save_dir = "app/upload_file"

    result = show_inference_result()
    json_file_path = get_latest_path(file_type="json")
    if not json_file_path:        
        json_file_path = create_json_file(save_dir)
    else:
        delete_content_in_json(json_file_path)
    save_inference_result_to_json(result, json_file_path)
    return result


@app.post(
    "/identity_cards/save_inference_results/", response_model=IdentityCardResponse
)
async def save_inference_results(db: db_dependency):
    identity_card = save_identity_card_from_json()
    db.add(identity_card)
    db.commit()
    db.refresh(identity_card)

    return identity_card


@app.get(
    "/identity_cards/get_inference_results", response_model=List[IdentityCardResponse]
)
async def get_inference_results(db: db_dependency):
    results = db.query(IdentityCard).all()
    return results


# 1. Call the function from gradio_ui.py to get the Gradio Blocks object
gradio_app_instance = create_gradio_ui()

# 2. Mount the Gradio app to your FastAPI app at the /gradio path
#    Now, when you go to http://127.0.0.1:8000/gradio, you'll see the Gradio UI.
app = gr.mount_gradio_app(app, gradio_app_instance, path="/gradio")
from transformers import ViTForImageClassification, ViTImageProcessor
from typing import Sequence, Annotated
import torch
from PIL import Image
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, Depends
from pathlib import Path
import uvicorn

app = FastAPI()

def load_file(file: UploadFile):
    return Image.open(file.file)

UploadImage = Annotated[Image.Image, Depends(load_file)]
class ImageClassificationResponse(BaseModel):
    """Response for image classification"""
    label: str
    note: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "label": "healthy",
                    'note': "everything is fine"
                }
            ]
        }
    }

class ImageClassification(ViTForImageClassification):
    def inference(self, embeddings: torch.Tensor):
        with torch.no_grad():
            logits = self(embeddings).logits

        return logits.argmax(-1).item()


model_path = (Path(__file__).parent / 'model').absolute()
model: ImageClassification = ImageClassification.from_pretrained(model_path)
processor: ViTImageProcessor = ViTImageProcessor.from_pretrained(model_path)

@app.post('/diagnosis',response_model=ImageClassificationResponse)
async def diagnosis(image: UploadImage):
    embeddings = processor((image, ), return_tensors="pt")
    predict = model.inference(embeddings['pixel_values'])
    health_status = model.config.id2label[predict]
    return ImageClassificationResponse(label=health_status)




if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
    # image = Image.open(Path(__file__).parent / 'img.png')
    # embeddings = processor((image, ), return_tensors="pt")
    # predict = model.inference(embeddings['pixel_values'])
    # health_status = model.config.id2label[predict]

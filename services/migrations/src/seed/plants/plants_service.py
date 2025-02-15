import requests
from googletrans import Translator
from diffusers import StableDiffusionPipeline
import torch
from sqlmodel.ext.asyncio.session import AsyncSession
from db import Plant, Family, Genius, Rank, Plan
from uuid import uuid4
import asyncio

API_KEY = "SO5Ml5rY4LilkG5lRzoQBGNSUvfZ-gtlzCiENs8eVBY"
HUGGIN_FACE_TOKEN="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"
BASE_URL = "https://trefle.io/api/v1/plants"

class Plants:
  def __init__(self, db: AsyncSession):
    self.db = db
    self.translator = Translator()
    # self.pipe = StableDiffusionPipeline.from_pretrained(
    #   "CompVis/stable-diffusion-v1-4",
    #   use_auth_token=HUGGIN_FACE_TOKEN
    # )
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # self.pipe.to(device)

  def fetch_plants(self, page=1):
    """ Получает данные о растениях из Trefle API """
    params = {"token": API_KEY, "page": page, "per_page": 100}
    response = requests.get(BASE_URL, params=params)
    return response.json().get("data", []) if response.status_code == 200 else []

  async def translate_data(self, plants_data):
    """ Асинхронно переводит названия растений на русский """
    async def translate_text(text):
      if text:
        translation = await self.translator.translate(text, src="en", dest="ru")
        return translation.text
      return text

    tasks = [translate_text(plant.get("common_name", "")) for plant in plants_data]
    translated_names = await asyncio.gather(*tasks)

    for plant, translated_name in zip(plants_data, translated_names):
      plant["common_name"] = translated_name

    return plants_data

  async def save_to_db(self, plants_data):
    """ Сохраняет растения в базу данных """
    for plant_data in plants_data:
      family = Family(name=plant_data.get("family"))
      genius = Genius(name=plant_data.get("genus"))
      rank = Rank(name=plant_data.get("rank"))
      plan = Plan(day=1, action="Полив", note="Поливать раз в неделю")

      plant = Plant(
        name=plant_data.get("common_name"),
        bibliography=plant_data.get("bibliography"),
        slug=plant_data.get("slug"),
        year=plant_data.get("year"),
        family=family,
        genius=genius,
        rank=rank,
        plan=plan,
      )

      self.db.add_all([family, genius, rank, plan, plant])

    await self.db.commit()

  # def generate_images(self, plants_data):
  #   """ Генерирует изображения для растений и обновляет записи в БД """
  #   for plant_data in plants_data:
  #     plant_name = plant_data.get("common_name")
  #     image = self.pipe(plant_name).images[0]
  #     image_path = f"images/{plant_name}.png"
  #     image.save(image_path)

  #     # Обновление базы данных с изображением
  #     plant = self.db.query(Plant).filter_by(name=plant_name).first()
  #     if plant:
  #       plant.image_url = image_path
  #       self.db.commit()

  async def run(self):
    """ Запускает весь процесс автоматизации """
    plants_data = self.fetch_plants()
    plants_data = await self.translate_data(plants_data)
    await self.save_to_db(plants_data)
    # self.generate_images(plants_data)
    return "Завершено!"

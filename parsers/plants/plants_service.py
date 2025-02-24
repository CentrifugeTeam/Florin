import requests
from googletrans import Translator
from diffusers import StableDiffusionPipeline
import torch
from sqlmodel.ext.asyncio.session import AsyncSession
from db import Plant, Family, Genius, Rank, Plan
from uuid import uuid4
import asyncio
from sqlalchemy.future import select


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

  async def fetch_plants(self, total_pages=5, per_page=20):
    """ Получает и переводит данные о растениях из Trefle API """
    all_plants = []

    for page in range(1, total_pages + 1):
      params = {"token": API_KEY, "page": page, "per_page": per_page}
      response = requests.get(BASE_URL, params=params)

      if response.status_code == 200:
        all_plants.extend(response.json().get("data", []))
      else:
        print(f"Ошибка при получении данных: {response.status_code}")

    return await self.translate_data(all_plants)

  async def translate_data(self, plants_data):
    """ Асинхронно переводит все ключевые данные растений на русский """
    
    async def translate_text(text):
      if text:
        translation = await self.translator.translate(text, src="en", dest="ru")
        return translation.text
      return text

    tasks = []
    for plant_data in plants_data:
      if isinstance(plant_data, dict):
        tasks.append(
          asyncio.gather(
            translate_text(plant_data.get("common_name", "")),
            translate_text(plant_data.get("family", "")),
            translate_text(plant_data.get("genus", "")),
            translate_text(plant_data.get("rank", ""))
          )
        )

    all_translations = await asyncio.gather(*tasks)

    for plant_data, translations in zip(plants_data, all_translations):
      plant_data["common_name"], plant_data["family"], plant_data["genus"], plant_data["rank"] = translations
    return plants_data

  async def save_to_db(self, plants_data):
    """ Сохраняет растения в базу данных """
    for plant_data in plants_data:
      family_name = plant_data.get("family")
      genus_name = plant_data.get("genus")
      rank_name = plant_data.get("rank")

      family = await self.get_or_create(Family, name=family_name)
      genius = await self.get_or_create(Genius, name=genus_name)
      rank = await self.get_or_create(Rank, name=rank_name)

      # План на 90 дней (это можно улучшить через ML)
      plan = Plan(day=1, action="Полив", note="Поливать раз в неделю")

      plant = Plant(
        name = plant_data.get("common_name"),
        bibliography=plant_data.get("bibliography"),
        slug=plant_data.get("slug"),
        year=plant_data.get("year"),
        image_url=plant_data["image_url"],
        family_id=family.id,
        genius_id=genius.id,
        rank_id=rank.id,
        plan=plan,
      )

      # если имя цветка не изветна то скип
      if not plant.name:
        continue 

      self.db.add(plan)
      self.db.add(plant)

    await self.db.commit()

  async def get_or_create(self, model, **kwargs):
    instance = await self.db.execute(select(model).filter_by(**kwargs))
    instance = instance.scalars().first()
    
    if instance:
      return instance
    
    instance = model(**kwargs)
    self.db.add(instance)
    
    try:
      await self.db.commit()
    except Exception:
      await self.db.rollback()
      raise
    
    return instance

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
    plants_data = await self.fetch_plants()
    await self.save_to_db(plants_data)
    # self.generate_images(plants_data)
    return "Завершено!"

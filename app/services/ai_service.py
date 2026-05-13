from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def generate_story(child_name: str, product_name: str, child_age: int) -> str:
    prompt = f"""
    Génère une histoire courte et amusante pour un enfant de {child_age} ans.
    L'enfant s'appelle {child_name} et est le héros de l'histoire.
    L'histoire doit être en rapport avec le produit : {product_name}.
    L'histoire doit être positive, éducative et parler de nutrition de façon ludique.
    Maximum 150 mots.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents={"text":"dis bonjour"}
    )
    return response.text

async def generate_quiz(product_name: str, child_age: int) -> str:
    prompt = f"""
    Génère un quiz de 3 questions simples et amusantes pour un enfant de {child_age} ans.
    Le quiz doit porter sur le produit : {product_name} et sur la nutrition en général.
    Chaque question doit avoir 3 choix de réponses (A, B, C) avec la bonne réponse indiquée.
    Adapte le vocabulaire à l'âge de l'enfant.
    Maximum 150 mots.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    return response.text
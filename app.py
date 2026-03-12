import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- 1. НАСТРОЙКА ИИ ---
# Твой временный ключ вшит прямо сюда (с защитой от пробелов)
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')

PROMPT = """Ты — строгий профессиональный нутрициолог. Я отправляю тебе фотографию блюда или продукта. 
Твоя задача проанализировать фото и выдать ответ строго по следующей структуре:

1. 🍽️ Название блюда: (кратко).
2. ⚖️ Оценка порции: (укажи примерный вес порции на фото в граммах, на который ты будешь опираться при расчете).
3. 📊 КБЖУ на порцию с фото: (Калории, Белки, Жиры, Углеводы — дай максимально точные цифры именно для этого визуального объема).
4. 🥗 Ингредиенты: (просто перечисли, из чего состоит блюдо, без рецепта и шагов приготовления).
5. ⚠️ Аллергены: (выдели все возможные скрытые и явные аллергены: лактоза, глютен, орехи, морепродукты, яйца, мед и т.д. Если их нет, напиши "Явных аллергенов не обнаружено").

Отвечай четко по списку, без вступительных и прощальных фраз."""

# --- 2. ИНТЕРФЕЙС ---
st.title("🍔 AI Калькулятор калорий")
st.write("Загрузи фото еды или сделай снимок, а нейросеть всё посчитает!")

tab1, tab2 = st.tabs(["📁 Загрузить фото", "📸 Сделать снимок"])

with tab1:
    uploaded_file = st.file_uploader("Выбери картинку...", type=["jpg", "jpeg", "png"])

with tab2:
    camera_photo = st.camera_input("Сфоткай еду прямо сейчас")

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
elif camera_photo is not None:
    image = Image.open(camera_photo)

if image is not None:
    st.image(image, caption="Твое блюдо", width="stretch")
    
    # --- 3. КНОПКА И АНАЛИЗ ---
    if st.button("🪄 Проанализировать блюдо"):
        with st.spinner("Нейросеть анализирует фото..."):
            try:
                response = model.generate_content([PROMPT, image])
                st.success("Готово!")
                st.write(response.text)
            except Exception as e:

                st.error(f"Произошла ошибка: {e}")


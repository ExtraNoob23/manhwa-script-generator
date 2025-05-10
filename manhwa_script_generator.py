import streamlit as st
import openai
from PIL import Image
import base64
import io

# إعداد واجهة Streamlit
st.set_page_config(page_title="مانهاوا سكربت توليد تلقائي", layout="centered")
st.title("🧠📖 توليد سكربت مانهاوا تلقائيًا")
st.markdown("ارفع صورة مانهاوا، وسيقوم الذكاء الاصطناعي بفهمها وكتابة سكربت سردي تلقائي")

# إدخال مفتاح API
api_key = st.text_input("أدخل مفتاح OpenAI API", type="password")

# رفع صورة
uploaded_file = st.file_uploader("ارفع صورة مانهاوا (JPEG/PNG)", type=["jpg", "jpeg", "png"])

# دالة لتحويل الصورة إلى Base64
def image_to_base64(img_bytes):
    return base64.b64encode(img_bytes).decode("utf-8")

# دالة توليد السكربت
def generate_script(api_key, image_bytes):
    base64_image = image_to_base64(image_bytes)

    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "افهم محتوى هذه الصورة من مانهاوا واكتب سردًا دراميًا مناسبًا كأنك بتحكيها على يوتيوب باللهجة العربية الفصحى أو المصرية."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=1000
    )

    return response.choices[0].message['content']

# عند الضغط على الزر
if uploaded_file and api_key:
    image_bytes = uploaded_file.read()
    with st.spinner("جارٍ تحليل الصورة وتوليد السكربت..."):
        try:
            script_text = generate_script(api_key, image_bytes)
            st.success("✅ تم توليد السكربت بنجاح")
            st.text_area("📜 السكربت الناتج:", script_text, height=400)
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
elif uploaded_file and not api_key:
    st.warning("يرجى إدخال مفتاح OpenAI API أولاً")

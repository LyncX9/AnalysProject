import streamlit as st
import nbformat
import base64

# -------------------------------
# Fungsi untuk membaca output notebook
# -------------------------------
def load_notebook_outputs(nb_path):
    try:
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        outputs = []
        for cell in nb.cells:
            if cell.cell_type == "code" and 'outputs' in cell:
                for output in cell['outputs']:
                    if output.output_type == "stream":
                        outputs.append(('text', output.text))
                    elif output.output_type == "execute_result":
                        if 'text/plain' in output.data:
                            outputs.append(('text', output.data['text/plain']))
                    elif output.output_type == "display_data":
                        if 'text/plain' in output.data:
                            outputs.append(('text', output.data['text/plain']))
                        if 'image/png' in output.data:
                            img_data = base64.b64decode(output.data['image/png'])
                            outputs.append(('image', img_data))
        return outputs
    except Exception as e:
        st.error(f"Gagal membaca notebook: {e}")
        return []

# -------------------------------
# Fungsi untuk menampilkan output dengan styling gelap
# -------------------------------
def display_outputs(outputs):
    for tipe, content in outputs:
        if tipe == 'text':
            if len(content) > 300:
                st.markdown(
                    f"""
                    <div style='background-color:#1e1e1e; color:#f1f1f1;
                    padding:15px; border-radius:10px;
                    border:1px solid #444; overflow-x:auto;
                    font-family: monospace; white-space: pre;
                    max-height:350px'>
                    {content}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(
                    f"""
                    <div style='background-color:#2b2b2b; color:#f1f1f1;
                    padding:10px; border-radius:8px; font-family: monospace'>
                    {content}
                    </div>
                    """, unsafe_allow_html=True)
        elif tipe == 'image':
            st.image(content, use_column_width=True)

# -------------------------------
# Dummy Sentiment Prediction
# -------------------------------
def predict_sentiment(text):
    if not text.strip():
        return "Netral", 0.0
    elif "jelek" in text.lower():
        return "Negatif", 90.0
    elif "bagus" in text.lower():
        return "Positif", 95.0
    else:
        return "Netral", 60.0

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Visualisasi + Sentimen", layout="wide")
st.markdown("<h1 style='color:#00f7ff;'>📘 Visualisasi Analisis & Sentimen Komentar YouTube</h1>", unsafe_allow_html=True)

st.subheader("📊 Visualisasi & Analisis Sebelumnya")

outputs = load_notebook_outputs("Anlyss4.ipynb")
if outputs:
    display_outputs(outputs)
else:
    st.warning("Tidak ada output yang ditampilkan. Pastikan notebook telah dijalankan dan disimpan.")

st.markdown("---")
st.subheader("✍️ Analisis Sentimen Langsung")

user_input = st.text_area("Masukkan komentar:", height=100, placeholder="Contoh: Video ini sangat bermanfaat!")

if st.button("Prediksi Sentimen"):
    hasil, confidence = predict_sentiment(user_input)
    st.success(f"**Hasil Sentimen:** {hasil}")
    st.info(f"**Tingkat Keyakinan:** {confidence:.2f}%")

import streamlit as st
import qrcode
from io import BytesIO
import time

# ---------- QR Generator Function ----------
def gen_url_qr(upi_id, amount=""):
    upi_url = f"upi://pay?pa={upi_id}"
    if amount.strip():
        upi_url += f"&am={amount}&cu=INR"

    qr = qrcode.make(upi_url)

    buf = BytesIO()
    qr.save(buf, format="PNG")
    byte_im = buf.getvalue()

    return byte_im, upi_url


# ---------- Page Config ----------
st.set_page_config(page_title="PayQR", page_icon="💳", layout="centered")

# ---------- Custom CSS for Responsive UI & Animations ----------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #1f1c2c, #928dab);
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
        text-align: center;
        animation: fadeInDown 1s ease-in-out;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #f1f1f1;
        text-align: center;
        margin-bottom: 20px;
        animation: fadeInUp 1s ease-in-out;
    }
    @keyframes fadeInDown {
        from {opacity: 0; transform: translateY(-20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    @keyframes fadeInUp {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .stTextInput input {
        border-radius: 10px;
        padding: 10px;
    }
    .stButton button {
        background: linear-gradient(90deg, #ff512f, #dd2476);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: transform 0.2s ease-in-out;
    }
    .stButton button:hover {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- UI ----------
st.markdown("<div class='main-title'>💳 PayQR</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Generate a UPI QR code that works with <b>GPay, PhonePe, Paytm</b></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    upi_id = st.text_input("Enter UPI ID", placeholder="example@upi")
with col2:
    amount = st.text_input("Enter Amount (Optional)", placeholder="100")

# ---------- Generate Button ----------
if st.button("✨ Generate QR Code"):
    if not upi_id.strip():
        st.warning("⚠️ Please enter a valid UPI ID.")
    else:
        with st.spinner("Generating your QR Code..."):
            time.sleep(1.5)  # Smooth loading animation
            try:
                byte_im, upi_url = gen_url_qr(upi_id, amount)

                st.image(byte_im, caption="📲 Scan this QR to Pay", use_container_width=True)

                st.download_button(
                    label="⬇️ Download QR Code",
                    data=byte_im,
                    file_name=f"{upi_id}_qr.png",
                    mime="image/png"
                )

                st.success("✅ QR Code generated successfully!")
                st.code(upi_url, language='text')

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

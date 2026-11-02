%%writefile app.py
import streamlit as st
import json
import os

st.set_page_config(page_title="সবজি বাজার ও লাইভ কাস্টমার কেয়ার", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4fdf4; }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #1b5e20; color: white; }
    h1 { color: #2e7d32; }
    </style>
""", unsafe_allow_html=True)

PUBLIC_CHAT_FILE = "public_chat.json"
PRIVATE_CHAT_FILE = "private_chat.json"
ADMIN_PASSWORD = "A1#MASAG"

def load_data(file_path, is_dict=False):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if is_dict and isinstance(data, dict):
                    return data
                elif not is_dict and isinstance(data, list):
                    return data
            except:
                pass
    return {} if is_dict else []

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

st.sidebar.title("🌿 মোড নির্বাচন করুন")
app_mode = st.sidebar.radio(
    "কোথায় যেতে চান?",
    ["🛒 পাবলিক চ্যাট (সবাই দেখবে)", "🔒 প্রাইভেট প্রতিনিধি প্যানেল (কাস্টমার কেয়ার)"]
)

if "pub_user_name" not in st.session_state:
    st.session_state.pub_user_name = ""
if "priv_user_name" not in st.session_state:
    st.session_state.priv_user_name = ""

if app_mode == "🛒 পাবলিক চ্যাট (সবাই দেখবে)":
    st.title("🛒 তাজা সবজি বাজার - লাইভ চ্যাট ও ইনবক্স")
    st.markdown("##### বাজারের সবার সাথে উন্মুক্ত চ্যাট করুন অথবা কাস্টমার কেয়ারে সরাসরি গোপন মেসেজ পাঠান।")

    tab1, tab2 = st.tabs(["📢 সবার সাথে উন্মুক্ত চ্যাট", "💬 কাস্টমার কেয়ারে সরাসরি (প্রাইভেট) মেসেজ"])

    with tab1:
        st.subheader("পাবলিক চ্যাট রুম")
        
        if not st.session_state.pub_user_name:
            with st.form("pub_name_form"):
                n_input = st.text_input("আপনার নাম লিখুন (চ্যাট শুরু করতে):")
                n_btn = st.form_submit_button("নাম সেভ করুন")
                if n_btn and n_input:
                    st.session_state.pub_user_name = n_input
                    st.rerun()
        else:
            st.success(f"👋 স্বাগতম, **{st.session_state.pub_user_name}**! নিচে সরাসরি বার্তা লিখুন:")
            
            pub_messages = load_data(PUBLIC_CHAT_FILE, is_dict=False)
            chat_box = st.container(height=300)
            with chat_box:
                if not pub_messages:
                    st.info("এখনো কোনো পাবলিক মেসেজ নেই।")
                for msg in pub_messages:
                    st.markdown(f"**🌿 {msg['sender']}**: {msg['text']}")

            user_msg = st.chat_input("আপনার বার্তা এখানে লিখুন...")
            if user_msg:
                pub_messages.append({"sender": st.session_state.pub_user_name, "text": user_msg})
                save_data(PUBLIC_CHAT_FILE, pub_messages)
                st.rerun()

    with tab2:
        st.subheader("কাস্টমার কেয়ারের সাথে গোপন চ্যাট (ইনবক্স)")
        
        if not st.session_state.priv_user_name:
            with st.form("priv_name_form"):
                p_input = st.text_input("আপনার নাম লিখুন (গোপন ইনবক্সের জন্য):")
                p_btn = st.form_submit_button("ইনবক্স ওপেন করুন")
                if p_btn and p_input:
                    st.session_state.priv_user_name = p_input
                    st.rerun()
        else:
            st.success(f"🔒 গোপন ইনবক্স ({st.session_state.priv_user_name}) - এখানে পাঠানো বার্তা শুধু অ্যাডমিন দেখতে পাবেন।")
            
            customer_inboxes = load_data(PRIVATE_CHAT_FILE, is_dict=True)
            my_name = st.session_state.priv_user_name
            
            if my_name not in customer_inboxes:
                customer_inboxes[my_name] = []
                
            my_chat_box = st.container(height=250)
            with my_chat_box:
                if not customer_inboxes[my_name]:
                    st.info("আপনার ইনবক্সে কোনো কথোপকথন নেই। আপনার প্রশ্ন বা অর্ডার নিচে লিখুন।")
                for chat in customer_inboxes[my_name]:
                    if chat["sender"] == "অ্যাডমিন (প্রতিনিধি)":
                        st.markdown(f"<div style='text-align: left; background-color: #d1e7dd; padding: 10px; border-radius: 10px; margin: 5px; color: #0f5132;'><b>অ্যাডমিন:</b> {chat['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: right; background-color: #cfe2ff; padding: 10px; border-radius: 10px; margin: 5px; color: #084298;'><b>আপনি ({chat['sender']}):</b> {chat['text']}</div>", unsafe_allow_html=True)

            priv_msg = st.chat_input("আপনার গোপন মেসেজ এখানে লিখুন...")
            if priv_msg:
                customer_inboxes[my_name].append({"sender": my_name, "text": priv_msg})
                save_data(PRIVATE_CHAT_FILE, customer_inboxes)
                st.rerun()

elif app_mode == "🔒 প্রাইভেট প্রতিনিধি প্যানেল (কাস্টমার কেয়ার)":
    st.title("🛠️ কাস্টমার কেয়ার - প্রতিনিধি প্যানেল")
    
    password = st.sidebar.text_input("প্রতিনিধি পাসওয়ার্ড দিন:", type="password")
    if password != ADMIN_PASSWORD:
        st.warning("⚠️ এটি অত্যন্ত সুরক্ষিত জোন। প্রবেশ করতে সঠিক পাসওয়ার্ড দিন।")
        st.stop()
    
    st.sidebar.success("✅ অ্যাডমিন প্যানেল আনলক হয়েছে!")
    st.markdown("গ্রাহকদের পাঠানো সমস্ত ব্যক্তিগত ইনবক্স মেসেজ নিচে দেখতে পাবেন এবং সরাসরি উত্তর দিতে পারবেন।")

    customer_inboxes = load_data(PRIVATE_CHAT_FILE, is_dict=True)

    if not customer_inboxes:
        st.info("বর্তমানে কোনো গ্রাহকের প্রাইভেট ইনবক্স মেসেজ নেই।")
    else:
        customer_names = list(customer_inboxes.keys())
        chosen_customer = st.selectbox("গ্রাহক নির্বাচন করুন:", customer_names)

        if chosen_customer:
            st.markdown(f"### 👤 {chosen_customer}-এর সাথে লাইভ চ্যাট")
            
            admin_chat_box = st.container(height=300)
            with admin_chat_box:
                for chat in customer_inboxes[chosen_customer]:
                    if chat["sender"] == "অ্যাডমিন (প্রতিনিধি)":
                        st.markdown(f"<div style='text-align: right; background-color: #d1e7dd; padding: 10px; border-radius: 10px; margin: 5px; color: #0f5132;'><b>আপনি (অ্যাডমিন):</b> {chat['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: left; background-color: #f8d7da; padding: 10px; border-radius: 10px; margin: 5px; color: #842029;'><b>{chat['sender']}:</b> {chat['text']}</div>", unsafe_allow_html=True)

            admin_reply = st.chat_input("এই গ্রাহককে উত্তর লিখুন...")
            if admin_reply:
                customer_inboxes[chosen_customer].append({"sender": "অ্যাডমিন (প্রতিনিধি)", "text": admin_reply})
                save_data(PRIVATE_CHAT_FILE, customer_inboxes)
                st.rerun()
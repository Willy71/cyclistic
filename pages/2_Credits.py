import streamlit as st
import smtplib
from email.mime.text import MIMEText

# Place name on page, icon and expand to canvas
st.set_page_config(
    page_title="Credits",
    page_icon="📪",
    layout="wide"
)

# We reduced the empty space at the beginning of the streamlit
reduce_space ="""
            <style type="text/css">
            /* Remueve el espacio en el encabezado por defecto de las apps de Streamlit */
            div[data-testid="stAppViewBlockContainer"]{
                padding-top:30px;
            }
            </style>
            """
# We load reduce_space
st.html(reduce_space)

def center_image(image, width):
    # Apply CSS style to center the image with Markdown
    st.markdown(
        f'<div style="display: flex; justify-content: center;">'
        f'<img src="{image}" width="{width}">'
        f'</div>',
        unsafe_allow_html=True
    )
    
def center_text(text, size, color):
    st.markdown(f"<h{size} style='text-align: center; color: {color}'>{text}</h{size}>",
            unsafe_allow_html=True)
    
def text(text, size, color):
    st.markdown(f"<h{size} style='text-align: left; color: {color}'>{text}</h{size}>",
            unsafe_allow_html=True)
    
def center_text_link(link_text, link_url, size, color):
    text_html = f"<h{size} style='text-align: center; color: {color}'><a href='{link_url}' style='text-decoration: none;' target='_blank'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{link_text}</a></h{size}>"
    st.markdown(text_html, unsafe_allow_html=True)

def left_text_link(link_text, link_url, size, color):
    text_html = f"<h{size} style='text-align: left; color: {color}'><a href='{link_url}' style='text-decoration: none;' target='_blank'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{link_text}</a></h{size}>"
    st.markdown(text_html, unsafe_allow_html=True)
    
def center_image_link(image, link, name, width):
    st.markdown(
        f"""
        <style>
            .image-enlace {{
                cursor: pointer;
                transition: transform 0.3s;
            }}
        </style>
        <div style="display: flex; justify-content: center;">
            <a href="{image}" target="_blank">
                <img class="image-enlace" src="{image}" width="{width}" alt="{name}">
            </a>
        </div>
        <h5 style='text-align: center;'><a href='{link}' target="_blank">{name}</a></h5>
        """,
        unsafe_allow_html=True  
    )
    
def photo_link(alt_text, img_url, link_url, img_width):
    markdown_code = f'''
    <div style="text-align: center;">
        <a href="{link_url}" target="_blank">
            <img src="{img_url}" alt="{alt_text}" width="{img_width}px">
        </a>
    </div>
    '''
    st.markdown(markdown_code, unsafe_allow_html=True)

st.write("#")

center_text("Work made", 1, 'white')
center_text("by", 1, 'white')
center_text("Guillermo Cerato", 1, 'white')

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#e1e615;" /> """, unsafe_allow_html=True)
               
center_text("My social networks", 2, 'white')
with st.container():    
    col41, col42, col43 = st.columns(3)
    with col41:
        center_image("https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/189_Kaggle_logo_logos-512.png", 80)
        center_text_link("Kaggle", "https://www.kaggle.com/willycerato", 6, 'white')
    with col42:
        center_image("https://cdn.pixabay.com/photo/2022/01/30/13/33/github-6980894_1280.png", 80)
        center_text_link("Github", "https://github.com/Willy71", 6, 'white')
    with col43:
        center_image("https://img.freepik.com/vetores-premium/logotipo-quadrado-do-linkedin-isolado-no-fundo-branco_469489-892.jpg", 80)
        center_text_link("Linkedin", "https://www.linkedin.com/in/willycerato",  6, 'white')
    st.caption("")
    col44, col45, col46 = st.columns(3)
    with col44:
        center_image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/2023_Facebook_icon.svg/50px-2023_Facebook_icon.svg.png", 80)
        center_text_link("Facebook", "https://www.facebook.com/guillermo.cerato", 6, 'white')
    with col45:
        center_image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Instagram_logo_2022.svg/150px-Instagram_logo_2022.svg.png", 80)
        center_text_link("Instagram", "https://www.instagram.com/willycerato", 6 ,'white')
    with col46:
        center_image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/120px-WhatsApp.svg.png", 80)
        center_text_link("Whatsapp", "https://wa.me/5542991657847", 6, 'white')

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#e1e615;" /> """, unsafe_allow_html=True)
center_text_link("My portfolio", "https://guillermocerato.streamlit.app", 2, "blue")

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#e1e615;" /> """, unsafe_allow_html=True)
center_text('Send an email 💌', 1, 'white')

with st.container():
    co01, co02, co03 = st.columns([2, 4, 2])
    with co02:
        # Taking inputs
        email_sender = 'gcerato@gmail.com'
        email_receiver = 'gcerato@gmail.com'
        email = st.text_input("Email")
        subject = st.text_input('Subject')
        body = st.text_area('Body')
        total = ("Cyclistic for Coursera  \n" + body + "\n" + email)

        if st.button("Send Email"):
            try:
                msg = MIMEText(total)
                msg['From'] = email_sender
                msg['To'] = email_receiver
                msg['Subject'] = subject

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(st.secrets["email"]["gmail"], st.secrets["email"]["password"])
                server.sendmail(email_sender, email_receiver, msg.as_string())
                server.quit()
        
                st.success('Email sent successfully! 🚀')
            except Exception as e:
                st.error(f"Failed to send email: {e}")
               
st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#e1e615;" /> """, unsafe_allow_html=True)
with st.container():
    col51, col52, col53, col54 = st.columns([4,0.5,1,0.5])
    with col51:
        center_text("Website made with Streamlit framework", 2, 'white')   
    with col53:            
        photo_link('', "https://i.postimg.cc/cJhYJnqx/streamlit-logo.jpg", 'https://streamlit.io/', 120)
               
with st.container():
    col55, col56, col57, col58 = st.columns([4,0.5,1,0.5])
    with col55:
        st.text("")
        center_text("Programmed with Python for Guillermo Cerato", 2, 'blue')
    with col57:
        photo_link('', "https://i.postimg.cc/9Q3yg2th/python.png", 'https://www.python.org', 120)
            
st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#e1e615;" /> """, unsafe_allow_html=True)

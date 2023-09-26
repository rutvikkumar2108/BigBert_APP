#!/usr/bin/env python
# coding: utf-8

# In[14]:

pip install easyocr

import base64
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import easyocr as ocr
import wikipedia
import re
import matplotlib.pyplot as plt
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from wordcloud import WordCloud, STOPWORDS


img=Image.open('logo.jpg')
profile_image=Image.open('https://github.com/rutvikkumar2108/BigBert_APP/blob/main/WhatsApp%20Image%202023-07-24%20at%2010.04.18.jpeg')
qr_image=Image.open('https://github.com/rutvikkumar2108/BigBert_APP/blob/main/WhatsApp%20Image%202023-07-24%20at%2010.08.59.jpeg')

st.set_page_config(page_title='BigBert', page_icon=img)

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("https://github.com/rutvikkumar2108/BigBert_APP/blob/main/WhatsApp%20Image%202023-07-25%20at%2009.25.14.jpeg")
img2= get_img_as_base64("https://github.com/rutvikkumar2108/BigBert_APP/blob/main/WhatsApp%20Image%202023-07-24%20at%2016.55.49.jpeg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
background-size: 150%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-size: 300%;
background-position: center; 
background-repeat: no-repeat;
background-attachment: local;
}}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

def load_model():
    reader=ocr.Reader(['en'])
    return reader

def model(question,text):
    model_name = "deepset/roberta-base-squad2"
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {'question':question,'context':text}
    result = nlp(QA_input)
    return result['answer']

rad=st.sidebar.radio('Navigation',['Home','Contribute to Dataset','About Us'])

st.set_option('deprecation.showPyplotGlobalUse',False)
      
# this is the main function in which we define our webpage 
def main():
    
    if rad=='Home':
        st.title("BIGBERT")
        col=st.sidebar.selectbox('select a column',['wikipedia page','Upload Image'])
        
        # here we define some of the front end elements of the web page like 
        # the font and background color, the padding and the text to be displayed
        html_temp = """
        <div style ="background-color:yellow;padding:13px">
        <h1 style ="color:black;text-align:center;">Get Answer of your Question </h1>
        </div>
        """
      
        # this line allows us to display the front end aspects we have 
        # defined in the above code
        st.markdown(html_temp, unsafe_allow_html = True)
        context=[]
        
        if col=='Upload Image':
            # the following lines create text boxes in which the user can enter 
            # the data required to make the prediction
            image = st.file_uploader(label="CONTEXT_IMAGE", type=["jpg",'png','jpeg'])
            reader=load_model()
            
            if image is not None:
                input_image=Image.open(image)
                st.write('Your Image')
                st.image(input_image,width=800)
                result=reader.readtext(np.array(input_image))
                for text in result:
                    context.append(text[1])
                context=' '.join(context[0:])
                
            else:
                st.write('upload an Image')
        if col=='wikipedia page':
        
            text_message_1 = st.text_input("Topic Name", "Type Here")
            if text_message_1!='Type Here':
                context=wikipedia.summary(text_message_1, sentences=200)
                
        if context:
            text = re.sub(r'==.*?==+' , '', context)
            text = text.replace('\n','')
            wordcloud = WordCloud(width = 3000, height=2000, random_state=1, background_color='salmon',\
                          colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(text)
            st.write('WordCloud')
            plt.imshow(wordcloud)
            st.pyplot()       
        
        text_message = st.text_input("QUESTION", "Type Here")
        
        if st.checkbox('You accept the T&C',value=False):
            st.write('Thank You')
        # the below line ensures that when the button called 'Predict' is clicked, 
        # the prediction function defined above is called to make the prediction 
        # and store it in the variable answer
    
        if st.button("Predict"):
            with st.spinner(" AI at Work!"):
                answer=model(text_message,context)
                st.write(answer) 
            st.success('Here you go!')
            
    elif rad=='Contribute to Dataset':
        st.title("BIGBERT")
        col=st.sidebar.selectbox('select a column',['wikipedia page','Upload Image'])
        
        # here we define some of the front end elements of the web page like 
        # the font and background color, the padding and the text to be displayed
        html_temp = """
        <div style ="background-color:yellow;padding:13px">
        <h1 style ="color:black;text-align:center;">Give Answer of your Question </h1>
        </div>
        """
      
        # this line allows us to display the front end aspects we have 
        # defined in the above code
        st.markdown(html_temp, unsafe_allow_html = True)
        context=[]
        
        if col=='Upload Image':
            # the following lines create text boxes in which the user can enter 
            # the data required to make the prediction
            image = st.file_uploader(label="CONTEXT_IMAGE", type=["jpg",'png','jpeg'])
            reader=load_model()
            
            if image is not None:
                input_image=Image.open(image)
                st.write('Your Image')
                st.image(input_image,width=800)
                result=reader.readtext(np.array(input_image))
                for text in result:
                    context.append(text[1])
                context=' '.join(context[0:])
            else:
                st.write('upload an Image')
    
        if col=='wikipedia page':
            
            text_message_2 = st.text_input("Topic Name", "Type Here")
            if text_message_2!='Type Here':
                context=wikipedia.summary(text_message_2, sentences=200)
            
        if context:
            text = re.sub(r'==.*?==+' , '', context)
            text = text.replace('\n','')
            wordcloud = WordCloud(width = 3000, height=2000, random_state=1, background_color='salmon',\
                          colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(text)
            st.write('WordCloud')
            plt.imshow(wordcloud)
            st.pyplot()
        
        text_message = st.text_input("QUESTION", "Type Here")
        
        text_answer= st.text_input('ANSWER','Type Here')
        
        # the below line ensures that when the button called 'SAVE' is clicked, 
        # the function will store the data. 
    
        if st.checkbox('You accept the T&C',value=False):
            st.write('Thank You')
    
        if st.button("SAVE"):
            with st.spinner(" AI at Work!"):
                st.write('Saved')
            st.success('Here you go!')
    elif rad=='About Us':
        
        st.title("About Us")
        st.header('RUTVIK KUMAR')
        st.image(profile_image,width=400)
        st.markdown("I am creating this Web Application to express my interest in the ML/DL and AI.Previously, I held an internship at GOJEK where I have worked as a data Scientist and as a data analyist for Henry Harvin analytics. I have also secured 2nd position in a Hackathon conducted by the Tredence Analytics.I’ve worked on projects like food preparation time estimation, Financial Analytics Loan Approval Prediction, and Analysing the Attrition Rate of a Company. Right now I am a 5th-year Dual Degree student at IIT Bhubaneswar. Apart from this, I enjoy playing football and have an interest in the stock market.After graduation, hope to work for an agency like yours to grow my experience, serve clients and eventually start my own agency. With the right opportunities and experience working with prominent clients, I believe that I can achieve my goal.I would like the opportunity to meet with you and discuss the opportunities you have available. Please let me know if you have any questions or would like to see specific work samples.")
        st.image(qr_image,width=100)
        st.markdown('please Scan the above QR Code to know more about me')
        
         
 
     
if __name__=='__main__':
    main()






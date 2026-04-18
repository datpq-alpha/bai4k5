import streamlit as st
import pandas as pd
import google.generativeai as genai

# Cấu hình API
genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])

# Lấy model text
model = genai.GenerativeModel('gemini-2.5-flash')
# DL
csv_content = '''Mien,San_luong,Nam,Don_vi_tinh
Bắc,150000,2025,tấn
Trung,100000,2025,tấn
Nam,200000,2025,tấn
'''
with open('pro5.4.csv', 'w', encoding='utf-8') as f:
    f.write(csv_content)
df = pd.read_csv('pro5.4.csv')
st.title('Sản lượng lúa thu hoạch 3 miền năm 2025')
st.subheader('Bảng DL gốc:')
st.dataframe(df)
df_chart = pd.DataFrame({
    'category':df['Mien'],
    'value':df['San_luong'],
    'order':[1,2,3]
})
st.subheader('Biểu đồ tròn:')
st.vega_lite_chart(
    df_chart,
    {
        'mark': {'type':'arc'},
        'encoding':{
            'theta':{'field':'value', 'type':'quantitative',
              'scale':{'range': [2.35619, 8.63937]}      },
            'color':{
                'field':'category',
                'type':'nominal',
                'scale':{
                    'domain':['Bắc','Trung',"Nam"],
                    'range':["#416D9D", "#674028", "#DEAC58"]
                }, 'legend':{'title':'Miền'}
            }, 'order': {'field': 'order'}
        }
    }
)

prompt = f"""
Đóng vai chuyên gia phân tích Dữ liệu chuyên nghiệp, hãy phân tích bộ dữ liệu sau: {csv_content}. Giọng văn thân thiện, chuyên nghiệp, 150 - 200 từ
"""
try:
    r = model.generate_content(prompt)
    st.info(r.text)
except Exception as e:
    st.error('AI-errored: ' + str(e))

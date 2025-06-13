import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

masha_data = {
    "название": [
        "Арт",
        "3д персонаж 1",
        "3д персонаж 2",
        "Выбор 1",
        "До/после 1",
        "Герои 1",
        "Выбор 2",
        "До/после 2",
        "Выбор 3",
        "До/после 3",
        "Герои 2",
        "Выбор 4",
        "До/после 4",
        "Герои 3"
    ],
    "формат": [
        "статья", "статья", "статья",
        "видео", "видео", "видео",
        "видео", "видео", "видео",
        "видео", "видео", "видео",
        "видео", "видео"
    ],
    "платформа": [
        "dtf", "dtf", "dzen",
        "youtube", "youtube", "youtube",
        "pinterest", "pinterest", "tiktok",
        "tiktok", "tiktok", "dzen",
        "dzen", "dzen"
    ],
    "просмотры": [1569, 2116, 8, 1911, 1274, 70, 38, 35, 139, 140, 118, 19, 19, 57],
    "вовлеченность": [0.03, 0.07, 0.25, 0.32, 0.41, 0.11, 0.09, 0.03, 0.04, 0.09, 0.08, 0.05, 0.11, 0.05],
    "реакции": [4, 13, 2, 10, 12, 5, 6, 3, 2, 2, 4, 0, 2, 0],
    "фидбек": [1, 8, 0, 3, 4, 3, 0, 0, 0, 0, 1, 0, 0, 0]
}

df = pd.DataFrame(masha_data)


st.set_page_config(page_title='Дашборд', layout='wide')

# Фирменные цвета
bg_color = '#000000'
text_color = '#FFFFFF'
main_color = '#a91b1b'
alt_color1 = '#C62828'
alt_color2 = '#777777'
font = 'DejaVu Sans'

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: '{font}', sans-serif; }}
    h1, h2, h3, h4, h5, h6 {{ color: {text_color}; font-family: '{font}', sans-serif; }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Аналитика публикаций Red Utopia Sadness")

# Фильтр по платформе
platforms = df['платформа'].unique()
selected_platforms = st.multiselect("Платформы", options=platforms, default=list(platforms))

# Фильтр по формату
formats = df['формат'].unique()
selected_formats = st.multiselect("Форматы", options=formats, default=list(formats))

# Фильтр по просмотрам
min_views, max_views = int(df['просмотры'].min()), int(df['просмотры'].max())
selected_range = st.slider("Диапазон просмотров", min_views, max_views, (min_views, max_views))

# Применяем фильтры
filtered_df = df[
    df['платформа'].isin(selected_platforms) &
    df['формат'].isin(selected_formats) &
    df['просмотры'].between(*selected_range)
]


st.subheader("Детальные данные по выбранным публикациям")
st.dataframe(filtered_df.style.set_properties(**{
    'background-color': bg_color,
    'color': text_color,
    'font-family': font
}))



if not filtered_df.empty:
    views_by_platform = filtered_df.groupby('платформа')['просмотры'].sum().reset_index()
    fig = px.bar(
        views_by_platform,
        x='платформа', y='просмотры',
        color_discrete_sequence=[main_color],
        labels={'платформа': 'Платформа', 'просмотры': 'Просмотры'},
        title='Суммарные просмотры по платформам'
    )
    fig.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(family=font, color=text_color),
        xaxis=dict(title_font=dict(color=text_color), tickfont=dict(color=text_color)),
        yaxis=dict(title_font=dict(color=text_color), tickfont=dict(color=text_color))
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Нет данных для выбранных фильтров.")


import plotly.express as px




platform_views = filtered_df.groupby('платформа')['просмотры'].sum().reset_index()
fig2 = px.pie(
    platform_views,
    names='платформа',
    values='просмотры',
    color_discrete_sequence=['#a91b1b', '#C62828', '#777777', '#FFFFFF'],
    title='Доли просмотров по платформам'
)
fig2.update_traces(textfont_size=16, textinfo='percent+label', marker=dict(line=dict(color='#000000', width=2)))
fig2.update_layout(
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    font=dict(family='DejaVu Sans', color='#FFFFFF'),
    title_font=dict(color='#FFFFFF')
)
st.plotly_chart(fig2, use_container_width=True)





if not filtered_df.empty:
    fig = px.scatter(
        filtered_df,
        x='просмотры', y='вовлеченность',
        color='платформа',
        size='реакции',
        color_discrete_sequence=[main_color, alt_color1, alt_color2, text_color],
        hover_data=['название'],
        labels={'просмотры': 'Просмотры', 'вовлеченность': 'Вовлечённость'},
        title='Просмотры vs Вовлечённость (размер — реакции)'
    )
    fig.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(family=font, color=text_color),
        xaxis=dict(title_font=dict(color=text_color), tickfont=dict(color=text_color)),
        yaxis=dict(title_font=dict(color=text_color), tickfont=dict(color=text_color)),
        legend=dict(font=dict(color=text_color))
    )
    st.plotly_chart(fig, use_container_width=True)




st.markdown("---")
st.markdown("© Мария Семак, 2025")

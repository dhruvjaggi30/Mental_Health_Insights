import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Mental Health Insights Explorer", layout="wide")

# Load datasets
datasets = {
    "Personality Disorders": pd.read_csv("personality_disorder_survey.csv"),
    "Panic Disorder": pd.read_csv("panic_disorder_survey_large.csv"),
    "Specific Phobia": pd.read_csv("balanced_specific_phobia_dataset.csv"),
    "PTSD": pd.read_csv("ptsd_survey_dataset.csv"),
    "Dissociative Disorder": pd.read_csv("dissociative_disorder_dataset.csv"),
    "Sexual Dysfunction": pd.read_csv("sexual_dysfunction_survey.csv"),
    "Psychosis": pd.read_csv("psychosis_disorder_dataset.csv"),
    "Eating Disorders": pd.read_csv("anorexia-bulimia-nervosa-estimated-cases.csv"),
    "Anxiety vs Depression": pd.read_csv("Dataset with Anxiety and depression.csv")
}

descriptions = {
    "Personality Disorders": "Long-term patterns of behavior and inner experiences that differ significantly from cultural expectations.",
    "Panic Disorder": "Sudden episodes of intense fear triggering physical symptoms without real danger.",
    "Specific Phobia": "Excessive, persistent fear of specific objects or situations.",
    "PTSD": "A psychiatric disorder that may occur in people who have experienced or witnessed a traumatic event.",
    "Dissociative Disorder": "Involves problems with identity, memory, or perception caused by trauma or stress.",
    "Sexual Dysfunction": "Problems during any stage of the sexual response cycle preventing satisfaction.",
    "Psychosis": "Loss of contact with reality involving hallucinations or delusions.",
    "Eating Disorders": "Mental health conditions marked by an obsession with food and body shape.",
    "Anxiety vs Depression": "A comparison of the prevalence of anxiety and depression disorders by country.",
    "Substance Use Disorder": "Persistent use of substances despite harmful consequences, affecting daily functioning."
}

# Sidebar
st.sidebar.title("🧠 Mental Health")
disorder = st.sidebar.selectbox("Select a disorder", list(datasets.keys()) + ["Substance Use Disorder"])

# Main content
st.title("Mental Health Insights Explorer")
st.caption("Visualize global mental health trends interactively.")

if disorder:
    st.subheader(disorder)
    st.info(descriptions.get(disorder, ""))

    if disorder == "Substance Use Disorder":
        data = {
            'Substance': ['Alcohol', 'Cannabis', 'Opioids', 'Sedatives', 'Inhalants', 'Cocaine', 'ATS', 'Hallucinogens'],
            'Children & Adolescents Prevalence (%)': [1.3, 0.9, 1.8, 0.58, 1.17, 0.06, 0.18, 0.07],
            'Adults Prevalence (%)': [17.1, 3.3, 2.1, 1.21, 0.58, 0.11, 0.18, 0.13]
        }
        df = pd.DataFrame(data)
        fig = go.Figure(data=[
            go.Bar(name='Children & Adolescents', x=df['Substance'], y=df['Children & Adolescents Prevalence (%)'], marker_color='cornflowerblue'),
            go.Bar(name='Adults', x=df['Substance'], y=df['Adults Prevalence (%)'], marker_color='darkorange')
        ])
        fig.update_layout(barmode='group', title='💊 Substance Use Disorder Prevalence by Age Group',
                          xaxis_title='Substance Type', yaxis_title='Prevalence (%)', height=500)
        st.plotly_chart(fig, use_container_width=True)

    elif disorder == "Personality Disorders":
        df = datasets[disorder]
        df = df[df["Personality Disorder"] == 1]
        total = df.shape[0]
        grouped = df.groupby(['Cluster', 'Disorder Type', 'Country']).size().reset_index(name='Count')
        grouped['Percentage'] = round((grouped['Count'] / total) * 100, 2)
        fig = px.sunburst(grouped, path=['Cluster', 'Disorder Type', 'Country'], values='Percentage', color='Cluster',
                          title='🌍 Personality Disorders by Cluster', color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    elif disorder == "Panic Disorder":
        df = datasets[disorder]
        df = df[df['Panic Disorder'] == 1]
        counts = df['Country'].value_counts().reset_index()
        counts.columns = ['Country', 'Panic Cases']
        fig = px.pie(counts, names='Country', values='Panic Cases',
                     title='🌍 Panic Disorder Cases by Country', color_discrete_sequence=px.colors.sequential.Reds)
        fig.update_traces(textinfo='label+percent+value')
        st.plotly_chart(fig, use_container_width=True)

    elif disorder == "Specific Phobia":
        df = datasets[disorder]
        df = df[df["Diagnosed"] == 1]
        grouped = df.groupby(['Phobia Type', 'Gender']).size().reset_index(name='Count')
        grouped['Percentage'] = grouped.groupby('Phobia Type')['Count'].transform(lambda x: round(x / x.sum() * 100, 2))
        fig = px.bar(grouped, x="Phobia Type", y="Percentage", color="Gender", barmode="group",
                     title="😨 Specific Phobias by Gender", color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    elif disorder == "PTSD":
        df = datasets[disorder]
        df = df[df["PTSD Diagnosed"] == 1]
        facet_data = df.groupby(['Country', 'Trigger Type', 'Gender']).size().reset_index(name='Count')
        facet_data['Percentage'] = facet_data.groupby('Country')['Count'].transform(lambda x: round((x / x.sum()) * 100, 2))
        fig = px.bar(facet_data, x='Trigger Type', y='Percentage', color='Gender', facet_col='Country',
                     title='📊 PTSD Triggers by Country and Gender', color_discrete_sequence=px.colors.qualitative.Set2, height=500)
        st.plotly_chart(fig, use_container_width=True)

    elif disorder == "Dissociative Disorder":
        df = datasets[disorder]
        df = df[df["Diagnosed"] == 1]
        df = df[df['Gender'].isin(['Male', 'Female'])]
        bubble_data = df.groupby(['Gender', 'Age Group', 'Main Problem Faced']).size().reset_index(name='Count')
        bubble_data['Percentage'] = round((bubble_data['Count'] / bubble_data['Count'].sum()) * 100, 2)
        fig = px.scatter(bubble_data, x='Gender', y='Age Group', size='Percentage', color='Main Problem Faced',
                         hover_name='Main Problem Faced', size_max=60, title='🌀 Dissociative Symptoms by Gender & Age', height=600)
        st.plotly_chart(fig, use_container_width=True)

    elif disorder == "Sexual Dysfunction":
        df = datasets[disorder]
        counts = df.groupby(['Country', 'Type']).size().reset_index(name='Count')
        total = counts['Count'].sum()
        counts['Percentage'] = round((counts['Count'] / total) * 100, 2)
        fig = px.sunburst(counts, path=["Country", "Type"], values="Count", title="💔 Sexual Dysfunction Types by Country",
                          color="Country", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

    elif disorder == "Psychosis":
        df = datasets[disorder]
        df = df[df['Diagnosed'] == 1]
        grouped = df.groupby(['Country', 'Gender']).size().reset_index(name='Count')
        grouped['Percentage'] = (grouped['Count'] / grouped.groupby('Country')['Count'].transform('sum')) * 100
        grouped['Percentage'] = grouped['Percentage'].round(2)
        fig = px.choropleth(grouped, locations="Country", locationmode="country names", color="Percentage",
                            facet_col="Gender", color_continuous_scale="Plasma",
                            title="🌍 Psychosis by Gender Across Countries", projection="natural earth", height=500)
        st.plotly_chart(fig, use_container_width=True)

    elif disorder == "Eating Disorders":
        df = datasets[disorder].rename(columns={
            'Current number of cases of anorexia nervosa, in both sexes aged all ages': 'Anorexia',
            'Current number of cases of bulimia nervosa, in both sexes aged all ages': 'Bulimia'
        })
        df_long = df.melt(id_vars=['Entity', 'Code', 'Year'], value_vars=['Anorexia', 'Bulimia'],
                          var_name='Disorder_Type', value_name='Case_Count')
        df_long['Disorder_Type'] = df_long['Disorder_Type'].map({
            'Anorexia': 'Undereating', 'Bulimia': 'Overeating'
        })
        fig = px.bar(df_long, x="Year", y="Case_Count", color="Disorder_Type", barmode="group",
                     title="🍽️ Overeating vs Undereating Cases Over Time", color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    elif disorder == "Anxiety vs Depression":
        df = datasets[disorder][['Country', 'Anxiety Disorders - % of Population', 'Depressive Disorders - % of Population']]
        df = df.rename(columns={
            'Anxiety Disorders - % of Population': 'Anxiety',
            'Depressive Disorders - % of Population': 'Depression'
        })
        df_long = df.melt(id_vars='Country', var_name='Disorder', value_name='Percentage')
        fig = px.bar(df_long, x='Country', y='Percentage', color='Disorder', barmode='group',
                     title='😟 Anxiety vs Depression Prevalence by Country', color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(xaxis_tickangle=-45, height=600)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No chart available.")

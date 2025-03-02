import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed.csv')
    df['City'] = df['City'].str.strip().str.lower()  
    return df

df = load_data()

# Streamlit UI
st.markdown(
    "<h1 style='text-align: center;'>🏆 Place Ranking System by City Name</h1>", 
    unsafe_allow_html=True
)
city = st.text_input("🔍 Enter Your City Name")

# Recommendation Function
def recommend_places(city, top_n=5):
    city_places = df[df['City'] == city.strip().lower()].copy()

    if city_places.empty:
        return None  

    # Sort places by ranking
    city_places = city_places.sort_values(by='Ranking Score', ascending=False)

    return city_places[['Name', 'City', 'Ranking Score', 'Google review rating',
                        'time needed to visit in hrs', 'Entrance Fee in INR', 'Significance']].head(top_n)

# Display Recommendations
if st.button("🔍 Show Recommendations"):
    results = recommend_places(city)

    if results is None:
        st.warning(f"❌ No places found for '{city.title()}'. Try a different city!")
    else:
        st.success(f"✅ Top {len(results)} places found in {city.title()}")
        st.dataframe(
            results.rename(columns={
                'Google review rating': 'Rating',
                'time needed to visit in hrs': 'Time (hrs)',
                'Entrance Fee in INR': 'Fee'
            }),
            column_config={
                "Ranking Score": st.column_config.ProgressColumn(
                    format="%.2f", min_value=0, max_value=1.0
                )
            },
            hide_index=True
        )


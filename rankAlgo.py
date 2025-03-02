import pandas as pd

data = pd.read_csv('processed.csv')

# Ranking Algorithm
def calculate_score(row):
    return (
        0.25 * row['Normalized Rating'] +
        0.30 * row['Normalized Time'] +
        0.15 * row['Normalized Fee'] +
        0.10 * row['Normalized Reviews'] +
        0.05 * row['Airport Score'] +
        0.10 * row['Weekend Availability Score'] +  
        0.05 * row['Significance Score'] +  
        0.05 * row['Type Score']
    )

data['Ranking Score'] = data.apply(calculate_score, axis=1)
df = data.sort_values(by='Ranking Score', ascending=False)


#Recommendation System
def recommend_places(city, top_n=5):
    city_places = df[df['City'].str.lower() == city.lower()].copy()
    if city_places.empty:
        return f"No places found for {city}."

    city_places = city_places.sort_values(by='Ranking Score', ascending=False)
    
    return city_places[['Name', 'City', 'Ranking Score', 'Google review rating',
                        'time needed to visit in hrs', 'Entrance Fee in INR', 'Significance']].head(top_n)
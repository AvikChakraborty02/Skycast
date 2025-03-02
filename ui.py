import streamlit as st
import geonamescache
import apps 
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Skycast⛅",  # Tab title
    page_icon="⛅",            # Favicon (can use a path to an image file or an emoji)
    layout="wide",             # Layout of the app (either "centered" or "wide")
    initial_sidebar_state="expanded"  # Sidebar state ("expanded" or "collapsed")
)

# Sidebar
st.sidebar.header("About Us")
st.sidebar.write("Skycast is a web application where you can query about weather reports of a particular location and you will get the current weather report of that location.")
st.sidebar.write("Want to know about weather? Go Skycast and ask...")
st.sidebar.markdown("""<hr>""",unsafe_allow_html=True)
st.sidebar.header("Contact Us")

# Your social media URLs
facebook_url = "https://www.facebook.com/share/15b3wweLft/"
instagram_url = "https://www.instagram.com/ig_mr.starkop/profilecard/?igsh=ZDFjNGtpdW9iaGpn"
linkedin_url = "https://www.linkedin.com/in/avik-chakraborty-61493824b"

# Include the Font Awesome CDN link to display icons
st.sidebar.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
""", unsafe_allow_html=True)

# HTML + CSS to create the icons with hover effect
st.sidebar.markdown(f"""
    <style>
        .social-icon {{
            font-size: 20px;
            margin: 0 10px;
            text-decoration: none;
            color: white;
            transition: transform 0.3s ease, color 0.3s ease;
        }}

        .social-icon:hover {{
            transform: scale(1.2);
        }}

        .social-icon-facebook:hover {{
            color: #3b5998; /* Facebook blue */
        }}

        .social-icon-instagram:hover {{
            color: #e1306c; /* Instagram pink */
        }}

        .social-icon-linkedin:hover {{
            color: #0077b5; /* LinkedIn blue */
        }}
    </style>

    <div style="text-align: center;">
        <a href="{facebook_url}" class="social-icon social-icon-facebook" target="_blank">
            <i class="fab fa-facebook"></i>
        </a>
        <a href="{instagram_url}" class="social-icon social-icon-instagram" target="_blank">
            <i class="fab fa-instagram"></i>
        </a>
        <a href="{linkedin_url}" class="social-icon social-icon-linkedin" target="_blank">
            <i class="fab fa-linkedin"></i>
        </a>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
            <br>
            <p style="line-height:0.8;">Developed By,</p>
            <p style="line-height:0.8;">Avik Chakraborty 😎</p>
            """,unsafe_allow_html=True)   

# Title
st.title("Skycast⛅")

# Geo Cities Names
gc = geonamescache.GeonamesCache()
cities = gc.get_cities()
city_names=['']
for city in cities.values():
    city_name=city['name']
    city_country=city['countrycode']
    city_names.append(city_name+","+city_country)

# Search Box    
select_city=st.selectbox("Search a City",city_names)
select_unit=st.selectbox("Select a Unit",['Metric','Scientific','Fahrenheit'])

# Check if the selectbox has a value selected
if select_city == "" or select_unit=="":
    # Disable the button if no option is selected
    button_disabled = True
    st.warning("Please select an option before clicking the button.")
else:
    # Enable the button if an option is selected
    button_disabled = False

# Unit Descriptions
# Create 3 columns
col1, col2, col3 = st.columns(3)

# Define the content of each card
with col1:
    st.markdown("""
        <div style="border: 1px solid white; padding: 20px; border-radius: 10px; background-color: #1d252d;">
            <h3>Metric</h3>
            <p style="line-height:0.8">Temperature: Celsius</p>
        	<p style="line-height:0.8">Wind Speed/Visibility: Kilometers/Hour</p>
	        <p style="line-height:0.8">Pressure: MB - Millibar</p>
	        <p style="line-height:0.8">Precip: MM - Millimeters</p>
        	<p style="line-height:0.8">Total Snow: CM - Centimeters</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="border: 1px solid white; padding: 20px; border-radius: 10px; background-color: #1d252d;">
            <h3>Scientific</h3>
            <p style="line-height:0.8">Temperature: Kelvin</p>
        	<p style="line-height:0.8">Wind Speed/Visibility: Kilometers/Hour</p>
	        <p style="line-height:0.8">Pressure: MB - Millibar</p>
	        <p style="line-height:0.8">Precip: MM - Millimeters</p>
        	<p style="line-height:0.8">Total Snow: CM - Centimeters</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style="border: 1px solid white; padding: 20px; border-radius: 10px; background-color: #1d252d;">
            <h3>Fahrenheit</h3>
            <p style="line-height:0.8">Temperature: Fahrenheit</p>
        	<p style="line-height:0.8">Wind Speed/Visibility: Miles/Hour</p>
	        <p style="line-height:0.8">Pressure: MB - Millibar</p>
	        <p style="line-height:0.8">Precip: IN - Inches</p>
        	<p style="line-height:0.8">Total Snow: IN - Inches</p>
        </div>
    """, unsafe_allow_html=True)
st.markdown("""<br>""",unsafe_allow_html=True)
# Query Button
if st.button("Get Weather Report",disabled=button_disabled):
    with st.spinner("Fetching weather reports..."):
        response=apps.get_response(select_city,select_unit)
        if response.get("success")==None:

            st.header(f"Weather Report of {select_city}")
            st.markdown("""<hr>""",unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)

            # Column 1
            with col1:
                # Getting Values
                image=response.get("current").get("weather_icons")
                image_url=image[0]
                temperature=str(response.get("current").get("temperature"))
                desc=response.get("current").get("weather_descriptions")
                description=desc[0]
                feelslike=str(response.get("current").get("feelslike"))

                # Formatting temparature
                if select_unit=="Metric":
                    temperature+="°C"
                elif select_unit=="Scientific":
                    temperature+="K"
                elif select_unit=="Fahrenheit":
                    temperature+="°F"

                # Formatting feelslike
                if select_unit=="Metric":
                    feelslike+="°C"
                elif select_unit=="Scientific":
                    feelslike+="K"
                elif select_unit=="Fahrenheit":
                    feelslike+="°F"

                st.markdown(f"""
                    <div style="border: 1px solid white; padding: 20px; border-radius: 10px; background-color: #1d252d;">
                        <h5>Weather Details ☁️:</h5>
                        <div style="text-align: center;">
                            <img src="{image_url}" alt="Weather image" style="border-radius: 5px; margin: auto;">
                        </div>
                        <br>
                        <p style="line-height:0.8">Temperature: {temperature}</p>
                        <p style="line-height:0.8">Weather Condition: {description}</p>
                        <p style="line-height:0.8">Feels Like: {feelslike}</p>         
                    </div>""",unsafe_allow_html=True)
            
            # Column 2
            with col2:
                # Getting Values
                name=response.get("location").get("name")
                country=response.get("location").get("country")
                region=response.get("location").get("region")
                lat=response.get("location").get("lat")
                lon=response.get("location").get("lon")
                localtime=response.get("location").get("localtime")
                utc_offset=response.get("location").get("utc_offset")

                st.markdown(f"""
                    <div style="border: 1px solid white; padding: 20px; border-radius: 10px; background-color: #1d252d;">
                        <h5>Location Details 📍:</h5>
                        <p style="line-height:0.8">Name: {name}</p>
                        <p style="line-height:0.8">Country: {country}</p>
                        <p style="line-height:0.8">Region: {region}</p>
                        <p style="line-height:0.8">Latitude: {lat}</p>
                        <p style="line-height:0.8">Longitude: {lon}</p>
                        <p style="line-height:0.8">Local Time: {localtime}</p>
                        <p style="line-height:0.8">UTC Offset: {utc_offset}</p>          
                    </div>""",unsafe_allow_html=True)
            
            # column 3:
            with col3:
                # Getting Values
                wind_speed=str(response.get("current").get("wind_speed"))
                wind_degree=response.get("current").get("wind_degree")
                wind_direction=response.get("current").get("wind_dir")
                humidity=response.get("current").get("humidity")
                pressure=response.get("current").get("pressure")
                precip=str(response.get("current").get("precip"))

                # Formatting Wind Speed
                if select_unit=="Metric" or select_unit=="Scientific":
                    wind_speed+=" km/hr"
                elif select_unit=="Fahrenheit":
                    wind_speed+=" miles/hr"

                # Formatting Precipitation
                if select_unit=="Metric" or select_unit=="Scientific":
                    precip+=" mm"
                elif select_unit=="Fahrenheit":
                    precip+=" in"

                st.markdown(f"""
                    <div style="border: 1px solid white; padding: 20px; border-radius: 10px; background-color: #1d252d;">
                        <h5>Wind Details 🍃:</h5>
                        <p style="line-height:0.8">Wind Speed: {wind_speed}</p>
                        <p style="line-height:0.8">Wind Degree: {wind_degree}</p>
                        <p style="line-height:0.8">Wind Direction: {wind_direction}</p>
                        <p style="line-height:0.8">Humidity: {humidity}%</p>
                        <p style="line-height:0.8">Pressure: {pressure} mb</p>
                        <p style="line-height:0.8">Precipitation: {precip}</p>         
                    </div>""",unsafe_allow_html=True)
                
            # column 4
            with col4:
                # Getting Values
                cloudcover=response.get("current").get("cloudcover")
                visibility=str(response.get("current").get("visibility"))
                uvindex=response.get("current").get("uv_index")

                # Formatting Visibility
                if select_unit=="Metric" or select_unit=="Scientific":
                    visibility+=" km"
                elif select_unit=="Fahrenheit":
                    visibility+=" miles"

                st.markdown(f"""
                    <div style="border: 1px solid white; padding: 20px; border-radius: 10px; background-color: #1d252d;">
                        <h5>More Details:</h5>
                        <p style="line-height:0.8">Cloud Cover: {cloudcover}%</p>
                        <p style="line-height:0.8">Visibility: {visibility}</p>
                        <p style="line-height:0.8">UV Index: {uvindex}</p>        
                    </div>""",unsafe_allow_html=True)
            
            col1,col2,col3=st.columns(3)
            with col1:
                pass
            with col2:
                st.markdown("""<br>""",unsafe_allow_html=True)
                html=apps.generate_dynamic_html(name,country,region,lat,lon,localtime,utc_offset,image_url,temperature,description,feelslike,wind_speed,wind_degree,wind_direction,humidity,pressure,precip,cloudcover,visibility,uvindex)
                pdf_data=apps.convert_html_to_pdf(html)
                if pdf_data:
                    st.download_button(
                        label="Download as PDF",
                        data=pdf_data,
                        file_name='Weather Report.pdf',
                        mime='application/pdf'
                    )      
                else:
                    st.error("Failed to generate PDF")
            with col3:
                pass

        elif response.get("success")==False:
            st.error(str(response["error"]["code"])+" : "+response["error"]["type"]+" - "+response["error"]["info"])           
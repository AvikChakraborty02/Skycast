import requests
import os
import io
from xhtml2pdf import pisa
from dotenv import load_dotenv
import streamlit as st

def get_response(city_name,metric):

    # Access your API key from the secrets
    api_key = st.secrets["api_keys"]["WEATHER_API_KEY"]

    url = "https://api.weatherstack.com/current?access_key="+api_key+"&query="
    # splitting the city name and country
    temp_list=city_name.split(",") 

    # getting the city name only
    city=temp_list[0] 
    
    # concating the city name with the url for query parameter
    url+=city

    # if metric is given by default it is metric
    if metric:
        if metric=='Metric':
            url+="&units=m"
        elif metric=='Scientific':
            url+="&units=s"
        elif metric=='Fahrenheit':
            url+="&units=f"

    response=requests.get(url)
    return (response.json())

def convert_html_to_pdf(html_string):
    # Create a BytesIO buffer to write the PDF
    pdf_buffer = io.BytesIO()
    
    # Create PDF from HTML string and write it to the buffer
    pisa_status = pisa.CreatePDF(html_string, dest=pdf_buffer)
    
    # Move the cursor back to the start of the BytesIO buffer
    pdf_buffer.seek(0)
    
    # Check if there was an error while creating the PDF
    if pisa_status.err:
        return None  # Return None if there was an error generating the PDF
    
    # Return the PDF content as bytes
    return pdf_buffer.read()  # Return the actual PDF content as bytes
    

def generate_dynamic_html(name,country,region,lat,lon,localtime,utc_offset,image_url,temperature,description,feelslike,wind_speed,wind_degree,wind_direction,humidity,pressure,precip,cloudcover,visibility,uvindex):
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather Report</title>
    </head>
    <body>
        <h1 style="text-align: center;font-family: 'Times New Roman', Times, serif;">Skycast</h1>
        <hr>
        <h3>Location Details:</h3>
        <hr>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Name: {name}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Country: {country}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Region: {region}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Latitude: {lat}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Longitude: {lon}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Local Time: {localtime}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">UTC Offset: {utc_offset}</p>
        <hr>
        <h3>Temperature Details:</h3> 
        <hr>
        <div style="text-align: center;">
            <img src="{image_url}" alt="Weather image" style="border-radius: 5px; margin: auto;">
        </div>
        <br>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Temperature: {temperature}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Weather Condition: {description}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Feels Like: {feelslike}</p>
        <hr>
        <h3>Wind Details:</h3>
        <hr>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Wind Speed: {wind_speed}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Wind Degree: {wind_degree}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Wind Direction: {wind_direction}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Humidity: {humidity}%</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Pressure: {pressure} mb</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Precipitation: {precip}</p>
        <hr>
        <h3>More Details:</h3>
        <hr>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Cloud Cover: {cloudcover}%</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">Visibility: {visibility}</p>
        <p style="line-height:0.6;font-family: 'Times New Roman', Times, serif;">UV Index: {uvindex}</p> 
        <h1 style="text-align:end;font-family: 'Times New Roman', Times, serif;">Developed By Avik Chakraborty</h1>
    </body>
    </html>
    '''
    return html



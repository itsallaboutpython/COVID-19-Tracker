"""
Project Name: COVID-19 Tracker
Project Developer:
    - The Special Coder
Project Description:
    This project uses tkinter and matplotlib library to create an application that can create graphs of 'confirmed cases', 'confirmed deaths' and
    'confirmed recoveries' of COVID-19 patients across the world or of one of the few countries mentioned in the code.
    The graph also forecasts future cases based on daily increases in confirmed cases, deaths and recoveries.
    The motive behind creating the project is to spread awareness aout the criticality of this disease and at the same time show the extent of 
    efforts being made by various countries in eradicating COVID-19.

"""

# Importing required packages
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
import pandas as pd 
import random
import math
import time
import datetime
import operator 
import warnings
import tkinter as tk
from tkinter import Label
from  tkinter import Button
import tkinter.font as Font
from tkinter import ttk
import urllib.request
from tkinter import messagebox
import requests
plt.style.use('fivethirtyeight')

# Initiating tkinter GUI
root = tk.Tk()
root.title("COVID-19 Graph Based Tracker")
root.geometry("500x500")
root.configure(bg='black')

# Function to show popup in case if computer is not connected to the internet
def popup_close():
    messagebox.showerror(title = "No Internet Connection", message = "Active internet connection is required to update data. Kindly connect to a network and try again")
    exit(0)

# Check for internet connection
url = "https://google.com"
timeout = 5
try:
    request = requests.get(url, timeout = timeout)
except Exception:
    popup_close()

# Global Variables
# Fetch data from net in thee form of CSV
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recoveries_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
latest_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/09-11-2020.csv')

window = 7
cols = confirmed_df.keys()
confirmed = confirmed_df.loc[:, cols[4]:cols[-1]]
deaths = deaths_df.loc[:, cols[4]:cols[-1]]
recoveries = recoveries_df.loc[:, cols[4]:cols[-1]]
dates = confirmed.keys()
world_cases = []
total_deaths = [] 
mortality_rate = []
recovery_rate = [] 
total_recovered = [] 
total_active = [] 


for i in dates:
    # Calculating sum of cases 
    confirmed_sum = confirmed[i].sum()
    death_sum = deaths[i].sum()
    recovered_sum = recoveries[i].sum()
    
    # Add total sums to lists
    world_cases.append(confirmed_sum)
    total_deaths.append(death_sum)
    total_recovered.append(recovered_sum)
    
    # Calculate rates
    mortality_rate.append(death_sum/confirmed_sum)
    recovery_rate.append(recovered_sum/confirmed_sum)

# Function to calculate increase and return list
def daily_increase(data):
    d = [] 
    for i in range(len(data)):
        if i == 0:
            d.append(data[0])
        else:
            d.append(data[i]-data[i-1])
    return d 

# Function to calculate average
def moving_average(data, window_size):
    moving_average = []
    for i in range(len(data)):
        if i + window_size < len(data):
            moving_average.append(np.mean(data[i:i+window_size]))
        else:
            moving_average.append(np.mean(data[i:len(data)]))
    return moving_average


# Confirmed cases
world_daily_increase = daily_increase(world_cases)
world_confirmed_avg= moving_average(world_cases, window)
world_daily_increase_avg = moving_average(world_daily_increase, window)

# Deaths
world_daily_death = daily_increase(total_deaths)
world_death_avg = moving_average(total_deaths, window)
world_daily_death_avg = moving_average(world_daily_death, window)


# Recoveries
world_daily_recovery = daily_increase(total_recovered)
world_recovery_avg = moving_average(total_recovered, window)
world_daily_recovery_avg = moving_average(world_daily_recovery, window)


# Active 
world_active_avg = moving_average(total_active, window)
days_since_1_22 = np.array([i for i in range(len(dates))]).reshape(-1, 1)
world_cases = np.array(world_cases).reshape(-1, 1)
total_deaths = np.array(total_deaths).reshape(-1, 1)
total_recovered = np.array(total_recovered).reshape(-1, 1)


# Forecast info
days_in_future = 10
future_forcast = np.array([i for i in range(len(dates)+days_in_future)]).reshape(-1, 1)
adjusted_dates = future_forcast[:-10]

# Creating future dates
start = '1/22/2020'
start_date = datetime.datetime.strptime(start, '%m/%d/%Y')
future_forcast_dates = []
for i in range(len(future_forcast)):
    future_forcast_dates.append((start_date + datetime.timedelta(days=i)).strftime('%m/%d/%Y'))

adjusted_dates = adjusted_dates.reshape(1, -1)[0]

# Function to plot graph of world confirmed cases in line graph
def world_confirmed_cases_linegraph():
    plt.figure(figsize=(10, 5))
    plt.plot(adjusted_dates, world_cases)
    plt.plot(adjusted_dates, world_confirmed_avg, linestyle='dashed', color='orange')
    plt.title('# of Coronavirus Cases Over Time', size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.legend(['Worldwide Coronavirus Cases', 'Moving Average {} Days'.format(window)], prop={'size': 15})
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of world confirmed deaths in line graph
def world_death_cases_linegraph():
    plt.figure(figsize=(10, 5))
    plt.plot(adjusted_dates, total_deaths)
    plt.plot(adjusted_dates, world_death_avg, linestyle='dashed', color='orange')
    plt.title('# of Coronavirus Deaths Over Time', size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.legend(['Worldwide Coronavirus Deaths', 'Moving Average {} Days'.format(window)], prop={'size': 15})
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of world confirmed recovery in line graph
def world_recovery_cases_linegraph():
    plt.figure(figsize=(10, 5))
    plt.plot(adjusted_dates, total_recovered)
    plt.plot(adjusted_dates, world_recovery_avg, linestyle='dashed', color='orange')
    plt.title('# of Coronavirus Recoveries Over Time', size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.legend(['Worldwide Coronavirus Recoveries', 'Moving Average {} Days'.format(window)], prop={'size': 15})
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of world confirmed cases in bar graph
def world_confirmed_cases_bargraph():
    plt.figure(figsize=(10, 5))
    plt.bar(adjusted_dates, world_daily_increase)
    plt.plot(adjusted_dates, world_daily_increase_avg, color='orange', linestyle='dashed')
    plt.title('World Daily Increases in Confirmed Cases', size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.legend(['Moving Average {} Days'.format(window), 'World Daily Increase in COVID-19 Cases'], prop={'size': 15})
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of world confirmed deaths in bar graph
def world_death_cases_bargraph():
    plt.figure(figsize=(10, 5))
    plt.bar(adjusted_dates, world_daily_death)
    plt.plot(adjusted_dates, world_daily_death_avg, color='orange', linestyle='dashed')
    plt.title('World Daily Increases in Confirmed Deaths', size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.legend(['Moving Average {} Days'.format(window), 'World Daily Increase in COVID-19 Deaths'], prop={'size': 15})
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of world confirmed recoveries in bar graph
def world_recovery_cases_bargraph():
    plt.figure(figsize=(10, 5))
    plt.bar(adjusted_dates, world_daily_recovery)
    plt.plot(adjusted_dates, world_daily_recovery_avg, color='orange', linestyle='dashed')
    plt.title('World Daily Increases in Confirmed Recoveries', size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.legend(['Moving Average {} Days'.format(window), 'World Daily Increase in COVID-19 Recoveries'], prop={'size': 15})
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of a country's confirmed cases in bar graph
def country_plot_confirmed_bargraph(x, y1, y2, y3, y4, country):
    confirmed_avg = moving_average(y1, window)
    confirmed_increase_avg = moving_average(y2, window)
    death_increase_avg = moving_average(y3, window)
    recovery_increase_avg = moving_average(y4, window)

    plt.figure(figsize=(10, 5))
    plt.bar(x, y2)
    plt.plot(x, confirmed_increase_avg, color='red', linestyle='dashed')
    plt.legend(['Moving Average {} Days'.format(window), '{} Daily Increase in Confirmed Cases'.format(country)], prop={'size': 15})
    plt.title('{} Daily Increases in Confirmed Cases'.format(country), size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of a country's confirmed cases in line graph
def country_plot_confirmed_linegraph(x, y1, y2, y3, y4, country):
    confirmed_avg = moving_average(y1, window)
    confirmed_increase_avg = moving_average(y2, window)
    death_increase_avg = moving_average(y3, window)
    recovery_increase_avg = moving_average(y4, window)

    plt.figure(figsize=(10, 5))
    plt.plot(x, y2)
    plt.plot(x, confirmed_increase_avg, color='red', linestyle='dashed')
    plt.legend(['Moving Average {} Days'.format(window), '{} Daily Increase in Confirmed Cases'.format(country)], prop={'size': 15})
    plt.title('{} Daily Increases in Confirmed Cases'.format(country), size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of a country's confirmed deaths in bar graph
def country_plot_death_bargraph(x, y1, y2, y3, y4, country):
    confirmed_avg = moving_average(y1, window)
    confirmed_increase_avg = moving_average(y2, window)
    death_increase_avg = moving_average(y3, window)
    recovery_increase_avg = moving_average(y4, window)

    plt.figure(figsize=(10, 5))
    plt.bar(x, y3)
    plt.plot(x, death_increase_avg, color='red', linestyle='dashed')
    plt.legend(['Moving Average {} Days'.format(window), '{} Daily Increase in Confirmed Deaths'.format(country)], prop={'size': 15})
    plt.title('{} Daily Increases in Deaths'.format(country), size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of a country's confirmed cases in line graph
def country_plot_death_linegraph(x, y1, y2, y3, y4, country): 
    confirmed_avg = moving_average(y1, window)
    confirmed_increase_avg = moving_average(y2, window)
    death_increase_avg = moving_average(y3, window)
    recovery_increase_avg = moving_average(y4, window)

    plt.figure(figsize=(10, 5))
    plt.plot(x, y3)
    plt.plot(x, death_increase_avg, color='red', linestyle='dashed')
    plt.legend(['Moving Average {} Days'.format(window), '{} Daily Increase in Confirmed Deaths'.format(country)], prop={'size': 15})
    plt.title('{} Daily Increases in Deaths'.format(country), size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of a country's confirmed recoveries in bar graph
def country_plot_recovery_bargraph(x, y1, y2, y3, y4, country):
    confirmed_avg = moving_average(y1, window)
    confirmed_increase_avg = moving_average(y2, window)
    death_increase_avg = moving_average(y3, window)
    recovery_increase_avg = moving_average(y4, window)

    plt.figure(figsize=(10, 5))
    plt.bar(x, y4)
    plt.plot(x, recovery_increase_avg, color='red', linestyle='dashed')
    plt.legend(['Moving Average {} Days'.format(window), '{} Daily Increase in Confirmed Recoveries'.format(country)], prop={'size': 15})
    plt.title('{} Daily Increases in Recoveries'.format(country), size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()

# Function to plot graph of a country's confirmed recoveries in line graph
def country_plot_recovery_linegraph(x, y1, y2, y3, y4, country):
    confirmed_avg = moving_average(y1, window)
    confirmed_increase_avg = moving_average(y2, window)
    death_increase_avg = moving_average(y3, window)
    recovery_increase_avg = moving_average(y4, window)

    plt.figure(figsize=(10, 5))
    plt.plot(x, y4)
    plt.plot(x, recovery_increase_avg, color='red', linestyle='dashed')
    plt.legend(['Moving Average {} Days'.format(window), '{} Daily Increase in Confirmed Recoveries'.format(country)], prop={'size': 15})
    plt.title('{} Daily Increases in Recoveries'.format(country), size=15)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel('# of Cases', size=15)
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.show()
      
# Utility function for getting country's cases, deaths, and recoveries        
def get_country_info(country_name):
    country_cases = []
    country_deaths = []
    country_recoveries = []  
    
    for i in dates:
        country_cases.append(confirmed_df[confirmed_df['Country/Region']==country_name][i].sum())
        country_deaths.append(deaths_df[deaths_df['Country/Region']==country_name][i].sum())
        country_recoveries.append(recoveries_df[recoveries_df['Country/Region']==country_name][i].sum())
    return (country_cases, country_deaths, country_recoveries)
    
# Function to call graph creation functions based on country name and graph type  
def country_confirmed_graph(country_name, graph):
    country_info = get_country_info(country_name)
    country_cases = country_info[0]
    country_deaths = country_info[1]
    country_recoveries = country_info[2]
    
    country_daily_increase = daily_increase(country_cases)
    country_daily_death = daily_increase(country_deaths)
    country_daily_recovery = daily_increase(country_recoveries)
    
    if graph == "Bar":
        country_plot_confirmed_bargraph(adjusted_dates, country_cases, country_daily_increase, country_daily_death, country_daily_recovery, country_name)
    elif grapgh == "Line":
        country_plot_confirmed_linegraph(adjusted_dates, country_cases, country_daily_increase, country_daily_death, country_daily_recovery, country_name)
    
# Function to call graph creation functions based on country name and graph type 
def country_death_graph(country_name, graph):
    country_info = get_country_info(country_name)
    country_cases = country_info[0]
    country_deaths = country_info[1]
    country_recoveries = country_info[2]
    
    country_daily_increase = daily_increase(country_cases)
    country_daily_death = daily_increase(country_deaths)
    country_daily_recovery = daily_increase(country_recoveries)
    
    if graph == "Bar":
        country_plot_death_bargraph(adjusted_dates, country_cases, country_daily_increase, country_daily_death, country_daily_recovery, country_name)
    elif grapgh == "Line":
        country_plot_death_linegraph(adjusted_dates, country_cases, country_daily_increase, country_daily_death, country_daily_recovery, country_name)
    
# Function to call graph creation functions based on country name and graph type 
def country_recovery_graph(country_name, graph):
    country_info = get_country_info(country_name)
    country_cases = country_info[0]
    country_deaths = country_info[1]
    country_recoveries = country_info[2]
    
    country_daily_increase = daily_increase(country_cases)
    country_daily_death = daily_increase(country_deaths)
    country_daily_recovery = daily_increase(country_recoveries)
    
    if graph == "Bar":
        country_plot_recovery_bargraph(adjusted_dates, country_cases, country_daily_increase, country_daily_death, country_daily_recovery, country_name)
    elif grapgh == "Line":
        country_plot_recovery_linegraph(adjusted_dates, country_cases, country_daily_increase, country_daily_death, country_daily_recovery, country_name)
    

# Check the values listed in dropdown menus when user click button
def check_value():
    if str(data_type_dropdown.get()) == "World":
        if str(category_type_dropdown.get()) == "Confirmed Cases":
            if str(graph_type_dropdown.get()) == "Bar":
                world_confirmed_cases_bargraph()
            else:
                world_confirmed_cases_linegraph()
        elif str(category_type_dropdown.get()) == "Confirmed Death":
            if str(graph_type_dropdown.get()) == "Bar":
                world_death_cases_bargraph()
            else:
                world_death_cases_linegraph()
        elif str(category_type_dropdown.get()) == "Confirmed Recoveries":
            if str(graph_type_dropdown.get()) == "Bar":
                world_recovery_cases_bargraph()
            else:
                world_recovery_cases_linegraph()
    else:
        if str(category_type_dropdown.get()) == "Confirmed Cases":
            country_confirmed_graph(str(data_type_dropdown.get()), str(graph_type_dropdown.get()))
        elif str(category_type_dropdown.get()) == "Confirmed Death":
            country_death_graph(str(data_type_dropdown.get()), str(graph_type_dropdown.get()))
        elif str(category_type_dropdown.get()) == "Confirmed Recoveries":
            country_recovery_graph(str(data_type_dropdown.get()), str(graph_type_dropdown.get()))


# Title of the GUI
title_font = Font.Font(family = "Lucida Grande", size=20)
title_label = tk.Label(root, text = "COVID-19 Graph Based Tracker", font = title_font, foreground='yellow', background='black')
title_label.place(relx=0.1, rely=0.1)

# Area type label
area_type_font = Font.Font(family="Lucida Grande", size = 15)
area_type_label = tk.Label(root, text = "Enter area type: ", font = area_type_font, foreground='yellow', background='black')
area_type_label.place(relx = 0.08, rely = 0.3)

# Graph type label
graph_type_font = Font.Font(family="Lucida Grande", size = 15)
graph_type_label = tk.Label(root, text = "Enter graph type: ", font = graph_type_font, foreground='yellow', background='black')
graph_type_label.place(relx = 0.08, rely = 0.45)

# Category type label
category_type_font = Font.Font(family = "Lucida Grande", size = 15)
category_type_label = tk.Label(root, text = "Enter category type", font = category_type_font, foreground='yellow', background='black')
category_type_label.place(relx = 0.08, rely = 0.6)

# Data type dropdown
var_data = tk.StringVar()
data_type_dropdown = ttk.Combobox(root, width = 27, textvariable = var_data, foreground='black', background='yellow')
data_type_dropdown['values'] = ('World', 'US', 'Russia', 'India', 'Brazil', 'South Africa', 'China', 'Italy',
             'Germany', 'Spain', 'France', 'United Kingdom', 'Peru', 'Mexico', 'Colombia', 'Saudi Arabia', 'Iran', 'Bangladesh',
            'Pakistan')
data_type_dropdown.place(relx = 0.5, rely = 0.3)
data_type_dropdown.current(0)

# Graph type dropdown
var_graph = tk.StringVar()
graph_type_dropdown = ttk.Combobox(root, width = 27, textvariable = var_graph, foreground='black', background='yellow')
graph_type_dropdown['values'] = ('Line', 'Bar')
graph_type_dropdown.place(relx = 0.5, rely = 0.45)
graph_type_dropdown.current(0)

# Category type dropdown
var_category = tk.StringVar()
category_type_dropdown = ttk.Combobox(root, width = 27, textvariable = var_category, foreground='black', background='yellow')
category_type_dropdown['values'] = ('Confirmed Cases', 'Confirmed Death', 'Confirmed Recoveries')
category_type_dropdown.place(relx = 0.5, rely = 0.6)
category_type_dropdown.current(0)

# Show Graph
show_graph_button = Button(root, text = "Show Graph", command = check_value, foreground='black', background='yellow')
show_graph_button.configure(width=10, activebackground="#33B5E3")
show_graph_button.place(relx = 0.4, rely = 0.75)

# Quit Button
quit_button = Button(root, text = "Quit", command = quit, foreground='black', background='yellow')
quit_button.configure(width=10, activebackground="#33B5E3")
quit_button.place(relx = 0.4, rely = 0.85)

# Main loop
root.mainloop()
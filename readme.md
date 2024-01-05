# Sunny Day 2 Project 

## Table of contents
1. [Genaral Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Collaboration](#collaboration)
5. [Note](#note)

## General Info 
This project is intended to present itself as a concluding exercise in the Python course:
[Advanced Python Programming: Build 10 OOP Applications](https://www.udemy.com/course/the-python-pro-course/).

In this exercise I tried to put into practice some of the concepts from the course, from creating
of databases through python developing web pages (with Flask) and using API.

The project recalls the last exercise of the course, where a call was being made 
to a weather Website through API to get tomorrow's weather data, in contrast this
project calls up past weather data from a website through API and a Machine Learning model (LSTM) 
is trained on this historical data to make predictions about tomorrow.

The *DATA* folder is missing in the github repository, but with the db.py file it is easy to rebuild it. I
pre-trained models are on the **ROME** data for the last __7 days__. :it:

### Project Information
The project is still under development and many improvements 
can be made.

## Tecnologies
The project was built with 
1. Computer features 
   * Machine: arm64
   * Platform: macOS-13.0-arm64-arm-64bit
2. Peculiar features of libraries:
   * Tensorflow 2.15.0
   * The other libraries used can be found within the [requirements.txt](https://github.com/schisanoluca99/Sunnyday2/blob/main/requirements.txt)


## Installation
If you want to install and use the project:

From the terminal go to the directory where you want to take the project, then:
```commandline
git clone https://github.com/schisanoluca99/Sunnyday2
```
Also recommended is the use of a virtual environment 
```bash
path/to/python -m venv venv
pip install -r requirements.txt
python sunnyday2.py
```

## Collaboration
I sincerely thank @Ardit Sulce for the teachings.

[<img src='https://simpleicons.org/icons/linkedin.svg' width='25'>](https://www.linkedin.com/in/schisanoluca) 
[<img src='https://simpleicons.org/icons/instagram.svg' width='25'>](https://www.instagram.com/schisanoluca/)
[<img src='https://simpleicons.org/icons/github.svg' width='25'>](https://github.com/schisanoluca99)

## Note
> [!NOTE]  
> The pre-trained models are on Rome data from 2016 to 2023, 
> it is likely that using past Rome data to predict temperatures in America may lead to
> to poorer results.

> [!TIP]
> You can create new tables on that db and decide to train the model on 
> new cities or even multiple cities together, this is the first version 
> and it is kept simple and basic for that reason.

> [!IMPORTANT]
> The goal of the project was not to have the most exact results possible but to 
> to try to put into practice as many lessons as possible learned during the course on
> [udemy](https://www.udemy.com/course/the-python-pro-course/).
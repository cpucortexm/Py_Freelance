# WebScraping SecurityCamera

## Problem Statement

> "Build an app that selected a security camera based on features the customer wants.
> 
> For example: Do you want night vision? Yes/No, Do you want Panning, Tilting, Zooming? Y/N
> 
> The customer will answer a series of questions and the app will suggest 1-2 cameras that best fit their needs.
> 
> Prefer to be coded in Python."
> 
> Tip: Select the cameras first from e-Commerce site. Then, write down different features of these cameras. Based on your data,
> come up with different questions.
> Now, write a Python script that iteratively restricts the set of user restrictions by asking the user one question
> after another.


> Feature lists can be from below (Technical Details)
> 1. Night vision
> 2. HDD
> 3. color
> 4. Resolution-1080
> 5. Pan
> 6. Tilt
> 7. outdoor
> 8. channels-2
> 9. mount wall


## Dependencies
Create a python virtual env before installing these requirements as follows

```
$ python3 -m venv <location/venv>

$ cd < location >

$ . venv/bin/activate

$ (venv) pip install -r Requirements.txt
 
```
**Running the app on terminal**

```
$ python3 camera_webscraping

```
It will show a list of features that are enabled by default. 

Deselect what is not needed and press **Done**.

It processes the link from ecommerce site, for home security cameras and displays the cameras to buy on terminal and csv file camera_list.csv
from django.shortcuts import render, redirect
from products.models import Product,Category
from accounts.models import Cart, Cart_item
from home.models import *
from django.contrib.auth.models import User

import requests
import googlemaps
from geopy.geocoders import ArcGIS
from geopy.geocoders import Nominatim
from geopy import distance
from math import sin, cos, sqrt, atan2

import folium
import openrouteservice
import operator
from functools import reduce

# Create your views here.



def home(request):
    products=Product.objects.filter(is_listed=True ,is_category_listed=True).order_by('product_name')
    # cart=Cart.objects.get(user=request.user)
    # cart_items=Cart_item.objects.get(cart=cart)
    # print(cart_items)
    # print(item.is_added)
    # for i in cart_items:
    #     if i.is_added==True:
    #         print('added')

    # geolocator = Nominatim(user_agent="hi")
    # location = geolocator.geocode("calicut")
    # location2 = geolocator.geocode("ernakulam")

    
    # print(location.address)
    # print(location2.address)
    # print((location.latitude, location.longitude))
    # print((location2.latitude, location2.longitude))
    # wellington =(location.latitude, location.longitude)
    # salamanca =(location2.latitude, location2.longitude)
    # print(distance.distance(wellington, salamanca).km, 'km')

    # calc_distance(location.latitude, location.longitude,location2.latitude, location2.longitude)


    # openroute(location.latitude, location.longitude,location2.latitude, location2.longitude)

    # origin = (location.latitude, location.longitude)
    # destination = (location2.latitude, location2.longitude)
    # api_key = "5b3ce3597851110001cf62485f8ae68db77d4d23bc5337f52a297b93"
    # route = get_route(origin, destination, api_key)

    # if route:
    #     # Initialize the map
    #     m = folium.Map(location=[9.5187367, 76.88763986495363], zoom_start=13)

    #     # Extract the route coordinates
    #     route_coords = route['routes'][0]['geometry']['coordinates']

    #     # Plot the route on the map
    #     folium.PolyLine(locations=route_coords, color='blue').add_to(m)

    #     # Display the map
    #     m.save('route_map.html')
    #     print("Map saved as route_map.html")
    # else:
    #     print("Failed to get route.")


    context={
        'products':products,
        'categories':Category.objects.filter(is_listed=True).order_by('category_name'),
        # 'cart':cart
        'banners':Banner.objects.all().order_by('order'),
        'is_authenticated':request.user.is_authenticated
        }
    banners=Banner.objects.all()

    return render(request, 'home/home.html',context)


def search(request):
    if request.method=='POST':
        search=request.POST.get('search')
        products_by_search = Product.objects.filter(product_name__istartswith=search).order_by('price')
    return render(request,'shop.html',{'products':products_by_search})

def calc_distance(lat1,lon1,lat2,lon2):
    R = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c


    location = float(lat1), float(lon1)
    location2 = float(lat2), float(lon2)

    m = folium.Map(location=location, width=800, height=400)

    folium.Marker(location, popup="The postcode brought me here").add_to(m)
    folium.Marker(location2, popup="The postcode brought me here").add_to(m)


def openroute(lat1, lon1, lat2, lon2):
    client = openrouteservice.Client(key='5b3ce3597851110001cf62485f8ae68db77d4d23bc5337f52a297b93')
    coords = [[lat1, lon1], [lat2, lon2]]
    route = client.directions(coordinates=coords, profile='driving-car',format='geojson' )



def get_route(origin, destination, api_key):
    client = openrouteservice.Client(key=api_key)
    coords= (origin, destination)
    route = client.directions(coords, profile='driving-car', optimize_waypoints=True)
    return route









def geocode():
    city = 'Kottayam'
    country = 'India'
    address = "1600+Pennsylvania+Ave+NW,Washington,DC,USA"
    gmaps=googlemaps.Client(key='AIzaSyAKzmg_lrgm17NQFZVOj-v5ZZQ72b-DhRI')
    result=gmaps.geocode(address)
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % address

    r = requests.get(url)
    if r.status_code == 200:
        result = r.json()
        if 'results' in result and len(result['results']) > 0:
            lat = float(result['results'][0]['geometry']['location']['lat'])
            lng = float(result['results'][0]['geometry']['location']['lng'])
"""
Old School Runescape API Wrapper
Created By: Thalweg
Version: 0.1
Date: 1/30/2019
"""
import requests
import json

# Base url for OSRS API
base_url = "http://services.runescape.com/m=itemdb_oldschool"
# Item Endpoint for OSRS API
item_endpoint = "/api/catalogue/detail.json?item="
#Graph Endpoint for OSRS API
graph_endpoint = "/api/graph/"


class Item(object):
    # This method returns the json data from the OSRS API query
    def getItemData(self, itemID):
        return requests.get(base_url + item_endpoint + str(itemID)).json()

    # Whenever a new instance of the class is created it will get data based on ID.
    def __init__(self, itemID):
        self.itemID = itemID
        self.data = self.getItemData(itemID)
    
    # The following methods deal with parsing out the individual pieces of data
    # from the json data structre. 
    def getIconURL(self):
        return self.data['item']['icon']
    
    def getLargeIconURL(self):
        return self.data['item']['icon_large']

    def getName(self):
        return self.data['item']['name']

    def getDescription(self):
        return self.data['item']['description']

    def getCurrentPrice(self):
        return self.data['item']['current']['price']
    
    def getTodayTrend(self):
        return self.data['item']['today']['trend']
    
    def getMembersOnly(self):
        return self.data['item']['members']

    def get30DayTrend(self):
        return (self.data['item']['day30']['trend'] + " ({})".format(self.data['item']['day30']['change']))

    def get90DayTrend(self):
        return (self.data['item']['day90']['trend'] + " ({})".format(self.data['item']['day90']['change']))
    
    def get180DayTrend(self):
        return (self.data['item']['day180']['trend'] + " ({})".format(self.data['item']['day180']['change']))
    
    # This method uses the graph endpoint to get the json data for daily prices 
    # over the last 180 days, As well as the average prices for the current day.
    def getGraphData(self):
        return requests.get(base_url + graph_endpoint + str(self.itemID) + ".json").json()
    
    # Returns the data in its raw json format
    def getData(self):
        return self.data
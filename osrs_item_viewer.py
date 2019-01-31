"""
Old School Runescape Item Viewer
Version: 0.1
Date: 1/31/2019
Author: Thalweg
"""
from tkinter import Tk, BOTH, END, CENTER
from tkinter.ttk import Frame, Button, Label, Entry
from PIL import Image, ImageTk
from io import BytesIO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
from datetime import timedelta
import osrs_api
import requests

class Example(Frame):
    # This is the URL to the defualt icon that will appear before any item is selected.
    defaultIconURL = "https://support.runescape.com/hc/article_attachments/360002434025/App_Icon-Circle.png"
    
    def __init__(self):
        super().__init__()

        self.initUI()
   
    def initUI(self):
        # Set the window title.
        self.master.title("OSRS Item Lookup")

        # Call the methods to center the window on screen & create grid within frame
        self.centerWindow()
        self.makeGrid()

        # Create all of the Label & Entry widgets contained within the frame
        self.nameLabel = Label(self, text="Name: ")
        self.name = Entry(self)
        self.descLabel = Label(self, text="Description: ")
        self.description = Entry(self)
        self.priceLabel = Label(self, text="Price: ")
        self.price = Entry(self)
        self.idLabel = Label(self, text="Item ID: ")
        self.itemID = Entry(self)

        # Setting the default icon image
        self.iconImg = self.getImage(self.defaultIconURL)
        self.icon = Label(self, image = self.iconImg)
        self.icon.image = self.iconImg

        # Creating the Button to fetch data via API.
        self.getData = Button(self, text="Get Data", command = lambda: self.getItem(self.itemID.get()))

        # Creating the frame that will contain MatPlotLib fig
        self.plotFrame = Frame(self)

        # Placing all of the widgets within the grid
        self.nameLabel.grid(row = 0, columnspan = 1, sticky = 'nsew')
        self.name.grid(row = 0, column = 1, columnspan = 14, sticky = 'nsew')
        self.descLabel.grid(row = 1, columnspan = 1, sticky = 'nsew')
        self.description.grid(row = 1, column = 1, columnspan = 14, sticky = 'nsew')
        self.icon.grid(row = 0, column = 15, rowspan = 3, columnspan = 5)
        self.priceLabel.grid(row = 2, columnspan = 1, sticky = 'nsew')
        self.price.grid(row = 2, column = 1, columnspan = 14, sticky = 'nsew')
        self.idLabel.grid(row = 19, columnspan = 1, sticky = 'nsew')
        self.itemID.grid(row = 19, column = 1, columnspan = 9, sticky = 'nsew')
        self.getData.grid(row = 19, column = 10, columnspan = 10, sticky = 'nsew')
        self.plotFrame.grid(row = 3, rowspan = 16, columnspan = 20, sticky = 'nsew')

        # Set the frame to expand and fill as the window is resized.
        self.pack(fill = BOTH, expand = 1)

    # This method will create a plot based on data fed in as a dictionary.
    def plot(self, data):

        # Destory all the children in the plotFrame widget, this allows for the
        # plot to update whenver a new item is selected.
        for widget in self.plotFrame.winfo_children():
            widget.destroy()

        # Place X & Y values into their own respective lists
        x = list(data.keys())
        y = list(data.values())

        # This is the starting day for the time data recieved from the server. 
        # The time values in the server are represented as milliseconds from Jan.
        # 1, 1970. The following converts all of those times in milliseconds to a datetime.
        day = datetime.date(1970, 1, 1)
        x[:] = [day + timedelta(days = (int(item) / ((1000*60*60*24)))) for item in x]

        # Create and size the figure to the plotframe size.
        f = Figure(figsize=(self.plotFrame.winfo_width() / 100, self.plotFrame.winfo_height() / 100), dpi=100)
        # Add 1 subplot on a 1 x 1 grid.
        a = f.add_subplot(111)
        # Format x_axis date
        f.autofmt_xdate()
        # Plot date and price values
        a.plot(x, y)
        
        # Create canvas for figure to reside on, set parent to plot frame, then
        # Draw the canvas and pack it in plotFrame.
        self.canvas = FigureCanvasTkAgg(f, self.plotFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand = 1)

    # This method interfaces with the OSRS API and retrieves data, updates data
    # in GUI.
    def getItem(self, itemIDNum):
        # Create new instance of Item with provided ID number.
        newItem = osrs_api.Item(itemIDNum)

        # Clear out the entry widgets if anything is any them.
        self.name.delete(0, END)
        self.description.delete(0, END)
        self.price.delete(0, END)

        # Insert the name, description and price of item in entry widgets.
        self.name.insert(0, newItem.getName())
        self.description.insert(0, newItem.getDescription())
        self.price.insert(0, newItem.getCurrentPrice())

        # Get the items icon url and set the icon to the new items image.
        self.iconImg2 = self.getImage(newItem.getLargeIconURL())
        self.icon.configure(image = self.iconImg2)
        self.icon.image = self.iconImg2
        
        # Call the plot method with the new items daily price data
        self.plot(newItem.getGraphData()['daily'])

    def centerWindow(self):

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        w = sw / 2
        h = 0.75 * sh

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
 
    def makeGrid(self):
        for x in range(0, 20):
            self.columnconfigure(x, weight = 1)
        for i in range(0, 20):
            self.rowconfigure(i, weight = 1, minsize = 20)
    
    def getImage(self, URL):
        imageRequest = requests.get(URL)
        return ImageTk.PhotoImage(Image.open(BytesIO(imageRequest.content)).resize((97,97)))

def main():
    root = Tk()
    ex = Example()
    root.mainloop()

if __name__=='__main__':
    main()
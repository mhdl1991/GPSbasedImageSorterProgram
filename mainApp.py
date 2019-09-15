"""
#GPS-BASED IMAGE SORTING SCRIPT

MADE USING PYTHON 3.6

THIS REQUIRES THE FOLLOWING LIBRARIES IN ORDER TO WORK:
    
    * EXTERNAL PACKAGES (INSTALL USING pip install <package_name> IN COMMAND LINE)
        * numpy
        * pandas
        * exifread
    
    * DEFAULT PACKAGES (SHOULD COME WITH PYTHON 3 INSTALLATION)
        * shutil
        * os
        * datetime
        
HOW TO USE IT:

    * EDIT THE ReferecePoints.csv FILE TO INCLUDE THE NAME, LATITUDE AND LONGTITUDE OF YOUR REFERENCE POINTS
    * PUT ALL THE IMAGES YOU WISH TO SORT IN THE input FOLDER, WITH NO SUBFOLDERS
    * MAKE SURE AN output FOLDER EXISTS (WILL IMPLEMENT METHOD TO AUTOMATICALLY CREATE AN output FOLDER LATER)
    * OPEN COMMAND PROMPT TO DIRECTORY THAT CODE IS SAVED IN
    * USE THE COMMAND python mainApp.py
    * PRESS "SORT IMAGES NOW"
    
HOW IT WORKS:
    
    * READS THE REFERENCE POINTS IN ReferencePoints.csv
    * GETS A LIST OF THE IMAGE FILES IN input
    * READS THE EXIF DATA OF EACH IMAGE TO ACQUIRE THE GPS COORDINATES
    * GETS THE CLOSEST POSSIBLE REFERENCE POINT TO EACH IMAGE
    * COPIES THE IMAGE FROM 
        input/imagename.jpg 
      TO 
        output/location/location_date_x.jpg 
    
"""


import fileSorting as fs
import tkinter as tk
import tkinter.ttk as ttk
import csv



def run():
    """
    This command does the important thing
    """
    fs.output_images_to_new_folder(input_path = fs.IMAGES_UNSORTED_PATH, output_path = fs.IMAGES_SORTED_PATH)


#Create a window with a few buttons 
window = tk.Tk()

#Widgets
descriptive_label = tk.Label(window, text = "GPS COORDINATE-BASED IMAGE SORTING TOOL")
descriptive_label.grid(row = 0, column = 2) 

referencepoints_label = tk.Label(window, text = "LIST OF REFERENCE POINTS:")
referencepoints_label.grid(row = 2, column = 2) 

#Reference points as a Treeview    
frame = tk.Frame(window)
tree_refs = ttk.Treeview(frame, columns = ("Location", "Latitude", "Longtitude") )

ysb = ttk.Scrollbar(frame, orient='vertical', command=tree_refs.yview)
xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree_refs.xview)
tree_refs.configure(yscroll=ysb.set, xscroll=xsb.set)

tree_refs.heading('Location', text="Location")
tree_refs.heading('Latitude', text="Latitude")
tree_refs.heading('Longtitude', text="Longtitude")

tree_refs.column('#0', stretch=tk.NO, minwidth=0, width=0)
tree_refs.column('#1', stretch=tk.NO, minwidth=0, width=200)
tree_refs.column('#2', stretch=tk.NO, minwidth=0, width=200)
tree_refs.column('#3', stretch=tk.NO, minwidth=0, width=200)


tree_refs.grid()
ysb.grid(row=0, column=1, sticky='ns')
xsb.grid(row=1, column=0, sticky='ew')
frame.grid(row = 3, column = 2)

#insert contents of REFERENCE_POINTS_PATH into Treeview
with open(fs.REFERENCE_POINTS_PATH) as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        location = row['Location']
        lat = row['Latitude']
        lon = row['Longtitude']
        tree_refs.insert("", 0, values=(location, lat, lon))
    

#This button does the important thing
testbutton1 = tk.Button(window, text = "SORT IMAGES NOW", command = run)
testbutton1.grid(row = 4, column = 2)


window.mainloop()
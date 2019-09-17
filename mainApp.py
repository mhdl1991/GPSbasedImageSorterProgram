import fileSorting as fs
import imageEXIFdataManip as imex
import tkinter as tk
import tkinter.ttk as ttk
import csv

def run(d, v):
    """
    This command does the important thing
    """
    #default value
    d_num = fs.DISTANCE_LIMIT
    #if d (text from the field) is not blank, turn it into a float
    if not d == "": d_num = float(d)
    
    d_calc = imex.get_distance_lat_long_haversine
    if v == 1:
        d_calc = imex.get_distance_lat_long_vicenty_inverse
        
    
    #run the sorting algorithm
    fs.output_images_to_new_folder(input_path = fs.IMAGES_UNSORTED_PATH, output_path = fs.IMAGES_SORTED_PATH, distance_threshold = d_num, dist_calc = d_calc)


#Create a window with a few buttons 
window = tk.Tk()

#Widgets
descriptive_label = tk.Label(window, text = "GPS COORDINATE-BASED IMAGE SORTING TOOL")
descriptive_label.grid(row = 0, column = 0) 

referencepoints_label = tk.Label(window, text = "LIST OF REFERENCE POINTS:")
referencepoints_label.grid(row = 1, column = 0) 

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
frame.grid(row = 2, column = 0)

#insert contents of REFERENCE_POINTS_PATH into Treeview
with open(fs.REFERENCE_POINTS_PATH) as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        location = row['Location']
        lat = row['Latitude']
        lon = row['Longtitude']
        tree_refs.insert("", 0, values=(location, lat, lon))


#Use a field to change the distance based on which images are sorted
frame2 = tk.Frame(window)
distancefield_label = tk.Label(frame2, text = "Distance Threshold (in km):")
distancefield_label.grid(row = 0, column = 0) 
#field validation 
def callback(P):
    if P == "": return True
    
    try:
        float(P)
    except:
        return False
    
    return True

vcmd = (frame2.register(callback))
distfield = tk.Entry(frame2, validate = 'all', validatecommand = (vcmd, '%P'), width = 12)
distfield.grid(row = 0, column = 1)
frame2.grid(row = 3, column = 0)

#selection between calculation methods?
frame3 = tk.Frame(window)
methodchoice = tk.Label(frame3, text="Calculation Method:")
methodchoice.grid(row = 0, column = 0)
var = tk.IntVar()
R1 = tk.Radiobutton(frame3, text="Haversine", variable= var, value=0)
R1.grid(row = 0, column = 1)
R2 = tk.Radiobutton(frame3, text="Vicenty Inverse", variable= var, value=1)
var.set(0)
R2.grid(row = 0, column = 2)
frame3.grid(row = 4, column = 0)


info_label = tk.Label(window, text = "LEAVE THE FIELD BLANK TO USE DEFAULT THRESHOLD DISTANCE OF 0.03048 km (APPROX 100 ft) ")
info_label.grid(row = 5, column = 0) 



#This button does the important thing
testbutton1 = tk.Button(window, text = "SORT IMAGES NOW", command = lambda: run(distfield.get(), var.get() ) )
testbutton1.grid(row = 6, column = 0)

window.resizable(width=False, height=False)
window.mainloop()

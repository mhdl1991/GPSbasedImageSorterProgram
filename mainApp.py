import fileSorting as fs
import tkinter as tk
import tkinter.ttk as ttk
import csv

def run(d):
    """
    This command does the important thing
    """
    #default value
    d_num = fs.DISTANCE_LIMIT
    #if d (text from the field) is not blank, turn it into a float
    if not d == "": d_num = float(d)
    #run the sorting algorithm
    fs.output_images_to_new_folder(input_path = fs.IMAGES_UNSORTED_PATH, output_path = fs.IMAGES_SORTED_PATH, distance_threshold = d_num)


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

info_label = tk.Label(frame2, text = "LEAVE THIS FIELD BLANK TO USE THE DEFAULT THRESHOLD DISTANCE OF 0.03048 km (APPROX 100 ft) ")
info_label.grid(row = 1, column = 0) 

frame2.grid(row = 4, column = 2)

#This button does the important thing
testbutton1 = tk.Button(window, text = "SORT IMAGES NOW", command = lambda: run(distfield.get()) )
testbutton1.grid(row = 5, column = 2)


window.mainloop()

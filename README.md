GPS-BASED IMAGE SORTING SCRIPT MADE USING PYTHON 3.6

THIS USES:

    * numpy
    * exifread
    * shutil
    * os
    * datetime
    * tkinter
        
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
    * COPIES THE IMAGE FROM input/imagename.jpg TO output/location/location_date_x.jpg 
    
CREDIT GOES TO:

   * https://gist.github.com/snakeye/fdc372dbf11370fe29eb
   * https://gist.github.com/erans/983821
   * https://github.com/nathanrooy/spatial-analysis/blob/master/vincenty-2016-09-22.py

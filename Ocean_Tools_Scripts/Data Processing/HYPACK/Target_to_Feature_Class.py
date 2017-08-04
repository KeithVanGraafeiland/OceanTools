#-------------------------------------------------------------------------------
# Name:         Target File to Feature Class
# Purpose:      Convert HYPACK Target file to a Feature Class
#
# Author:       Keith VanGraafeiland
# Created:      August 4, 2017
# Copyright:    (c) Keith VanGraafeiland 2017
# Licence:      MIT License
# Version:      0.1
# Tested:       ArcGIS Pro 2.0
#
# This file takes an input Target File (TGT) and convertes it to a feature
# class.
#
#-------------------------------------------------------------------------------
import arcpy, os, sys, string, tempfile
from arcpy import env
aprx = arcpy.mp.ArcGISProject('current')
arcpy.OverWriteOutput = 1
arcpy.env.overwriteOutput = True
pytemp = tempfile.mkdtemp()
fileList = str.split(sys.argv[1], ";")
out_gdb = sys.argv[2]
spRef = sys.argv[3]

for files2 in fileList:
  files = files2.strip("'")
  try:
    f = open(files)
    #f = open(sys.argv[1])

    arcpy.AddMessage("Working on file: " + files)

    filename = os.path.basename(files)
    filename2 = filename.strip(".tgt").strip(".TGT").strip(".txt")
    filename3 = filename2.replace("-", "_")
    print (filename3)

    env.workspace = pytemp
    csvfile = pytemp + os.sep + filename3 + ".csv"
    o = open(csvfile,"a")
    while 1:
      line = f.readline()
      if not line: break
      line = line.replace(" ",",")
      #o.write(line + "\n")
      o.write(line)
      #print line
    o.close()

    f = open(csvfile)
    text = f.read()
    f.close()
    # open the file again for writing
    f = open(csvfile, 'w')
    f.write("Type, Name, X, Y, Depth, Latitude, Longitude, Time, Date, Angle, Distance, Bearing, Code, Event, Quality, Notes, Extra\n")
    # write the original contents
    f.write(text)
    f.close()

    print ("Done")

      # Set the local variables
    in_Table = csvfile
    x_coords = "X"
    y_coords = "Y"
    z_coords = ""
    out_Layer = filename3

    saved_Layer = pytemp + os.sep + filename3 + ".lyrx"

    fc = out_gdb + os.sep + "TGT_" + filename3

      # Set the spatial reference

      #spRef = r""
      # Make the XY event layer...
    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

      # Print the total rows
    print (arcpy.GetCount_management(out_Layer))

    ## process the attributes for out_Layer

    # Save to a layer file
    arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)

    #cover layer file to feature class

    arcpy.CopyFeatures_management(saved_Layer, fc)
    arcpy.AddField_management(fc, "DATE_TIME", "DATE")
    arcpy.AddField_management(fc, "FILE_NAME", "TEXT", "", "" , 255)
    cursor = arcpy.da.UpdateCursor(fc, ("FILE_NAME","Time","Date","DATE_TIME"))
    for row in cursor:
      row[0] = filename
      date_time2 = str(str(row[2]).split(" ")[0] + " " + row[1])
      arcpy.AddMessage(str(date_time2))
      date_time = datetime.datetime.strptime(date_time2, "%Y-%m-%d %H:%M:%S")
      arcpy.AddMessage(str(date_time))
      row[3] = date_time
      cursor.updateRow(row)
    del cursor

    currentMapProject = aprx.listMaps()[0]
    currentMapProject.addDataFromPath(fc)

    print ("copy done")

      # If an error occurred print the message to the screen
    print (arcpy.GetMessages())
  except Exception as e:
    print (e.message)
    arcpy.AddWarning(e.message)


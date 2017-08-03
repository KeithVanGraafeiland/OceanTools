#-------------------------------------------------------------------------------
# Name:        Add Filename as Field
# Purpose:     Add the filename and path as a field to the input feature class.
#
# Author:      Keith VanGraafeiland
#
# Created:     August 3, 2017
# Copyright:   (c) Keith VanGraafeiland 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, os, os.path, string, socket, datetime

file_list_str = arcpy.GetParameterAsText(0)
file_list = file_list_str.split(";")

for i2 in File_list:
    i = i2.strip("'")
    filename = os.path.basename(i.strip(".shp"))
    fieldname = arcpy.ValidateFieldName("FILE_NAME", os.path.dirname(i))
    pathname = os.path.dirname(i)
    source_path = arcpy.ValidateFieldName("SOURCE_PATH", os.path.dirname(i))
    arcpy.AddField_management(i, fieldname, "TEXT", "100")
    arcpy.AddField_management(i, source_path, "TEXT", "255")
    #arcpy.CalculateField_management(i, fieldname, '"' + filename + '"', "PYTHON")
    #arcpy.CalculateField_management(i, source_path, '"' + pathname + '"', "PYTHON")
    cursor = arcpy.da.UpdateCursor(i, (fieldname,source_path))

    for row in cursor:
        row[0] = filename
        row[1] = pathname
        cursor.updateRow(row)


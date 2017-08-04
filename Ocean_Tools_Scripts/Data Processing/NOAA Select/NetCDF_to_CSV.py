#-------------------------------------------------------------------------------
# Name:         NOAA Select NetCDF to CSV
# Purpose:      Convert non-standard NetCDF files into CSV files that can then
#               be further processed.
#
# Author:       Keith VanGraafeiland
# Created:      July 7, 2017
# Copyright:    (c) Keith VanGraafeiland 2017
# Licence:      MIT License
# Version:      0.1
# Tested:       ArcGIS Pro 2.0
#
# This file takes an input directory from the TAR NOAA Select Files in NetCDF
# Format and creates CSV delinated text files for the variable, lat, long,
# depth, and date.
#
#-------------------------------------------------------------------------------
import netCDF4
import os
import csv

##variables
directory = arcpy.GetParameterAsText(0)
varName = arcpy.GetParameterAsText(1)

##function
def processItmesInMainDir(dirName):

    lastPartOfFolderName = dirName.split('.')[2]

    out_file = varName + "_" + lastPartOfFolderName + '.txt'

    outputFilePath = os.path.join(directory, out_file)

    arcpy.AddMessage("outputFilePath: " + outputFilePath)

    out = open(outputFilePath, 'w')
    writer = csv.writer(out)
    writer.writerow(('date', 'lat', 'lon','z', varName))

    proceeItemsInSubDir(dirName, writer)

    out.close()

    arcpy.AddMessage("Done Processing " + varName)

def proceeItemsInSubDir(dirName, writer):

    dirName = os.path.join(directory, dirName)

    for filename in os.listdir(dirName):
        if filename.endswith('.nc'):
            filepath = os.path.join(dirName, filename)
            print(filepath)
            f = netCDF4.Dataset(filepath,'r')
            value_array = f.variables[varName][:]
            for i in range(0, len(value_array)):
                if f.variables[varName][i] > 0:
                    writer.writerow((f.variables['date'][0], f.variables['lat'][0], f.variables['lon'][0], f.variables['z'][i], '{:.20f}'.format(f.variables[varName][i])))
            f.close()
        else:
            continue

def executeScript():
    for name in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, name)):
            processItmesInMainDir(name)

## start executing the script
executeScript()
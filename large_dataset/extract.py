import arcpy

# Set the workspace
arcpy.env.workspace = r'C:\Users\tmlewis\Documents\ArcGIS\Projects\Structures\Structures.gdb'
 
test = arcpy.SelectLayerByAttribute_management('https://services2.arcgis.com/FiaPA4ga0iQKduv3/ArcGIS/rest/services/USA_Structures_View/FeatureServer/3', 'NEW_SELECTION', 
                                         "STATE_FIPS = '{}'".format(42))

# Write the selected features to a new feature class
arcpy.CopyFeatures_management(test, 'structures')
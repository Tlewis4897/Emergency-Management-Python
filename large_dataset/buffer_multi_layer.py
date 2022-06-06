from re import X
import arcpy


def buffer_analytics(config, distance):
    arcpy.env.workspace = r"C:\Users\tmlewis\Documents\ArcGIS\Projects\Calculator\Calculator.gdb"
    buffer_list = [r'C:\Users\tmlewis\Documents\ArcGIS\Projects\Calculator\Calculator.gdb\buffer_pt3',
    r'C:\Users\tmlewis\Documents\ArcGIS\Projects\Calculator\Calculator.gdb\buffer_pt4',
    r'C:\Users\tmlewis\Documents\ArcGIS\Projects\Calculator\Calculator.gdb\buffer_pt5',
    r'C:\Users\tmlewis\Documents\ArcGIS\Projects\Calculator\Calculator.gdb\buffer_pt6',
    r'C:\Users\tmlewis\Documents\ArcGIS\Projects\Calculator\Calculator.gdb\buffer_pt7']

    x = 3
    for buffer_layer in buffer_list:
        arcpy.PairwiseBuffer_analysis(buffer_layer, 'half_mile_buffer'+ str(x), '.5 Miles', "", "", "", "")
        arcpy.PairwiseDissolve_analysis('half_mile_buffer'+ str(x), 'half_mile_buffer_dissolve'+ str(x), "", "", "")
        x+=1
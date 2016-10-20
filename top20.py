from qgis.core import *
import qgis.utils
from PyQt4.QtCore import *
import processing
import numpy as np
tLayer = iface.addVectorLayer("C:\Users\yoav\Copy\LLPlanners\Rehovot\GIS\SHP\Rehovot_Axial_010216Top20.shp", "top20layer", "ogr")
if not tLayer: 
    print "Layer failed to load!"

#Need to convert this script to the same way as was done in ssdiff to use editing mode and save time
    
attrName = "Top20"
attrGlobChoice = "CH"
attrLocChoice = "CHr3"
attrAxConn = "CONN"
attrGlobInt = "INT"
attrLocInt = "INTr3"
TopPercent = 90

caps = tLayer.dataProvider().capabilities()
count = tLayer.fieldNameIndex(attrName)
if caps & QgsVectorDataProvider.DeleteAttributes:
    res = tLayer.dataProvider().deleteAttributes([count])
tLayer.updateFields()
if caps & QgsVectorDataProvider.AddAttributes:
    res = tLayer.dataProvider().addAttributes([QgsField(attrName, QVariant.Int)])
tLayer.updateFields()
tLayer.startEditing()
index = tLayer.fieldNameIndex(attrName)
for feature in tLayer.getFeatures():
    tLayer.changeAttributeValue(feature.id(), index, 0)
tLayer.commitChanges()

GlobChList = tLayer.getValues(attrGlobChoice)[0]
GlobChPercentileValue = np.percentile(GlobChList, TopPercent)
LocChList = tLayer.getValues(attrLocChoice)[0]
LocChPercentileValue = np.percentile(LocChList, TopPercent)
ConnList = tLayer.getValues(attrAxConn)[0]
ConnPercentileValue = np.percentile(ConnList, TopPercent)
GlobIntList = tLayer.getValues(attrGlobInt)[0]
GlobIntPercentileValue = np.percentile(GlobIntList, TopPercent)
LocIntList = tLayer.getValues(attrLocInt)[0]
LocIntPercentileValue = np.percentile(LocIntList, TopPercent)

print "Glob CH", GlobChPercentileValue
print "Loc CH", LocChPercentileValue
print "Conn", ConnPercentileValue
print "Glob Int", GlobIntPercentileValue
print "Loc Int", LocIntPercentileValue

tLayer.startEditing()
for feature in tLayer.getFeatures():
    newValue=0
    if feature[attrGlobChoice]>GlobChPercentileValue:
        print "Adding Glob CH", feature.id(), feature[attrName]+1
        newValue=newValue+1
    if feature[attrLocChoice]>LocChPercentileValue:
        print "Adding Loc CH", feature.id(), feature[attrName]+1
        newValue=newValue+1
    if feature[attrAxConn]>ConnPercentileValue:
        print "Adding Conn", feature.id(), feature[attrName]+1
        newValue=newValue+1
    if feature[attrGlobInt]>GlobIntPercentileValue:
        print "Adding Glob Int", feature.id(), feature[attrName]+1
        newValue=newValue+1
    if feature[attrLocInt]>LocIntPercentileValue:
        print "Adding Loc Int", feature.id(), feature[attrName]+1
        newValue=newValue+1
    tLayer.changeAttributeValue(feature.id(), index, newValue)
tLayer.commitChanges()
        
tLayer.loadNamedStyle("C:\Users\yoav\OneDrive\GIS\Qgis\Top20Style.qml")
if hasattr(tLayer, "setCacheImage"):
    tLayer.setCacheImage(None) 
tLayer.triggerRepaint()

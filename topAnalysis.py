from qgis.core import *
import qgis.utils
from PyQt4.QtCore import *
import processing
import numpy as np

def calcTop20Attr(tLayer, fieldHeader, attrName, topPercent):
    globValList = tLayer.getValues(fieldHeader)[0]
    globPercentileValue = np.percentile(globValList, topPercent)
    index = tLayer.fieldNameIndex(attrName)
    for feature in tLayer.getFeatures():
        if feature[fieldHeader]>globPercentileValue:
            tLayer.changeAttributeValue(feature.id(), index, feature[attrName]+1)
    return
    
def normalizeToFive(tLayer, attrName, attrNum):
    index = tLayer.fieldNameIndex(attrName)
    for feature in tLayer.getFeatures():
        tLayer.changeAttributeValue(feature.id(), index, (feature[attrName]/attrNum)*5)
    return
    
def top20(segmentFileName, attrList, topPercent=90):
    QgsMapLayerRegistry.instance().removeAllMapLayers()    
    tLayer = iface.addVectorLayer(segmentFileName, "tLayer", "ogr")
    if not tLayer: 
        print "Layer failed to load!"
    
    attrName = "Top20"
    
    caps = tLayer.dataProvider().capabilities()
    count = tLayer.fieldNameIndex(attrName)
    if caps & QgsVectorDataProvider.DeleteAttributes:
        res = tLayer.dataProvider().deleteAttributes([count])
    tLayer.updateFields()
    if caps & QgsVectorDataProvider.AddAttributes:
        res = tLayer.dataProvider().addAttributes([QgsField(attrName, QVariant.Double)])
    tLayer.updateFields()
    tLayer.startEditing()
    index = tLayer.fieldNameIndex(attrName)
    for feature in tLayer.getFeatures():
        tLayer.changeAttributeValue(feature.id(), index, 0)
    tLayer.commitChanges()
    
    tLayer.startEditing()
    for fieldHeader in attrList:
        calcTop20Attr(tLayer, fieldHeader, attrName, topPercent)
    
    normalizeToFive(tLayer, attrName, len(attrList))
    tLayer.commitChanges()
    
    #tLayer.loadNamedStyle("C:\Users\yoav\OneDrive\GIS\Qgis\Top20Style.qml")
    if hasattr(tLayer, "setCacheImage"):
        tLayer.setCacheImage(None) 
    tLayer.triggerRepaint()
    
    return

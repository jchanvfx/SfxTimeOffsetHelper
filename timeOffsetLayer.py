# Time Offset Helper (Layer) - Johnny Chan
# --------------------------------------------------
import fx
from timeOffsetShape import OffsetShape

class OffsetLayer():
    def __init__(self, offset=0, layer=None):
        self.offsetFrames = offset
        self.layer = layer

    def runOffset(self):
        if self.layer != None and self.layer.type == 'Layer':
            allLayers = self._getSubLayers(self.layer)
            for layer in allLayers:
                self._offsetStereo(layer)
                self._offsetMatrix(layer)

                if layer == self.layer:
                    print '<b>%s</b> time shifted %d frames (Layer)' %(layer.label, self.offsetFrames)
                else:
                    print '<b>%s</b> time shifted %d frames (Sub-Layer)' %(layer.label, self.offsetFrames)

            childShapes = self._getChildShapes(allLayers)
            for shape in childShapes:
                OffsetShape(offset=self.offsetFrames , shape=shape).runOffset()

    def _offsetStereo(self, layer=None):
        '''offset for layer stereo offset'''
        stereoOffset = layer.property('stereoOffset')

        if stereoOffset.keys != []:
            stereoOffsetEditor = fx.PropertyEditor(stereoOffset)
            offsetStereoOffset = {}

            for so in stereoOffset.keys:
                offKey = self.offsetFrames + so
                offsetStereoOffset[offKey] = stereoOffset.getValue(so)
                stereoOffsetEditor.deleteKey(stereoOffset.keys.index(so))

            stereoOffsetEditor.execute()
            stereoOffset.constant = False

            for so in offsetStereoOffset.keys():
                stereoOffset.setValue(offsetStereoOffset[so], so)

            if offsetStereoOffset.keys()[0] != 0.0:
                stereoOffset = layer.property('stereoOffset')
                stereoOffsetEditor = fx.PropertyEditor(stereoOffset)
                stereoOffsetEditor.deleteKey(0)
                stereoOffsetEditor.execute()

    def _offsetMatrix(self, layer=None):
        '''offset for layer transform matrix (tracking data)'''
        transformMatrix = layer.property('transform.matrix')

        if transformMatrix.keys != []:
            transformMatrixEditor = fx.PropertyEditor(transformMatrix)
            offsetTransformMatrix = {}

            for tm in transformMatrix.keys:
                offKey = self.offsetFrames + tm
                offsetTransformMatrix[offKey] = transformMatrix.getValue(tm)
                transformMatrixEditor.deleteKey(transformMatrix.keys.index(tm))

            transformMatrixEditor.execute()
            transformMatrix.constant = False

            for tm in offsetTransformMatrix.keys():
                transformMatrix.setValue(offsetTransformMatrix[tm], tm)

            transformMatrix = layer.property('transform.matrix')
            transformMatrixEditor = fx.PropertyEditor(transformMatrix)

            for tmk in transformMatrix.keys:
                if not tmk in offsetTransformMatrix.keys():
                    transformMatrixEditor.deleteKey(transformMatrix.keys.index(tmk))

            transformMatrixEditor.execute()

    def _querySubLayers(self, layer=None):
        '''query all child layers'''
        returnObjects = []
        objects = [layer]
        while objects != []:
            for object in objects:
                objects.remove(object)

                for child in object.children:
                    if child.type == 'Layer':
                        objects.append(child)
                        returnObjects.append(child)

        return returnObjects

    def _getSubLayers(self, layer=None):
        '''get layer and all sub layers'''
        childObjects = self._querySubLayers(layer)
        allObjects = [layer]
        for l in childObjects:
            allObjects.append(l)

        return allObjects

    def _getChildShapes(self, layers=None):
        '''get child shape objects'''
        shapeObjects = []
        for layer in layers:
            for object in layer.children:
                if object.type == 'Shape':
                    shapeObjects.append(object)

        return shapeObjects

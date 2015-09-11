# Time Offset Helper v2.1
# (c) 2014 Johnny Chan - johnny@picostyle.com
# www.picostyle.com/scripts
# Compatibility: Silhouette v5.2 and up

import fx

class OffsetShape():
    def __init__(self, offset=0, shape=None):
        self.offsetFrames = offset
        self.shape = shape

    def runOffset(self):
        if self.shape != None and self.shape.type == 'Shape':
            self._offsetPath()
            self._offsetBlur()
            self._offsetOpacity()
            self._offsetStrokeWidth()

            print '<b>%s</b> time shifted %d frames (Shape)' %(self.shape.label, self.offsetFrames)

    def _offsetPath(self):
        '''offset for shape path'''
        path = self.shape.property('path')
        pathEditor = fx.PropertyEditor(path)
        offsetPath = {}

        for key in path.keys:
            offKey = self.offsetFrames + key
            offsetPath[offKey] = self.shape.evalPath(key)
            pathEditor.deleteKey(path.keys.index(key))

        pathEditor.execute()

        for key in offsetPath.keys():
            self.shape.setPath(offsetPath[key], key)

        path.constant = False

    def _offsetBlur(self):
        '''offset for shape blur'''
        blur = self.shape.property('blur')

        if blur.keys != []:
            blurEditor = fx.PropertyEditor(blur)
            offsetBlur = {}

            for b in blur.keys:
                offKey = self.offsetFrames + b
                offsetBlur[offKey] = blur.getValue(b)
                blurEditor.deleteKey(blur.keys.index(b))

            blurEditor.execute()
            blur.constant = False

            for b in offsetBlur.keys():
                blur.setValue(offsetBlur[b], b)

            if offsetBlur.keys()[0] != 0.0:
                blur = self.shape.property('blur')
                blurEditor = fx.PropertyEditor(blur)
                blurEditor.deleteKey(0)
                blurEditor.execute()

    def _offsetOpacity(self):
        '''offset for shape opacity'''
        opacity = self.shape.property('opacity')

        if opacity.keys != []:
            opacityEditor = fx.PropertyEditor(opacity)
            offsetOpacity = {}

            for o in opacity.keys:
                offKey = self.offsetFrames + o
                offsetOpacity[offKey] = opacity.getValue(o)
                opacityEditor.deleteKey(opacity.keys.index(o))

            opacityEditor.execute()
            opacity.constant = False

            for o in offsetOpacity.keys():
                opacity.setValue(offsetOpacity[o], o)

            if offsetOpacity.keys()[0] != 0.0:
                opacity = self.shape.property('opacity')
                opacityEditor = fx.PropertyEditor(opacity)
                opacityEditor.deleteKey(0)
                opacityEditor.execute()

    def _offsetStrokeWidth(self):
        '''offset for shape stroke width'''
        strokeWidth = self.shape.property('strokeWidth')

        if strokeWidth.keys != []:
            strokeWidthEditor = fx.PropertyEditor(strokeWidth)
            offsetStrokeWidth = {}

            for sw in strokeWidth.keys:
                offKey = self.offsetFrames + sw
                offsetStrokeWidth[offKey] = strokeWidth.getValue(sw)
                strokeWidthEditor.deleteKey(strokeWidth.keys.index(sw))

            strokeWidthEditor.execute()
            strokeWidth.constant = False

            for sw in offsetStrokeWidth.keys():
                strokeWidth.setValue(offsetStrokeWidth[sw], sw)

            if offsetStrokeWidth.keys()[0] != 0.0:
                strokeWidth = self.shape.property('strokeWidth')
                strokeWidthEditor = fx.PropertyEditor(strokeWidth)
                strokeWidthEditor.deleteKey(0)
                strokeWidthEditor.execute()


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


# ACTIONS
# _____________________________________

# _Layer Offset
class OffsetLayerAction(fx.Action):
    __doc__ = ("Time Offset all keyframes for the selected Layers and it's child objects\n"
                "Note: Once this script is executed you CANNOT Undo this Action")

    def __init__(self):
        fx.Action.__init__(self, 'Time Offset Helper|Offset selected Layers', root='PicoStyle')

    def available(self):
        session = fx.activeSession()
        assert session, "Select a Session"
        node = session.node(type="RotoNode")
        assert node, "The session does not contain a Roto Node"
        selection = fx.selection()
        assert len(selection) > 0, "There must be more than one selection."

    def execute(self):
        fx.beginUndo('Time Offset Selected Layers')

        viewer = fx.viewer
        selection = fx.selection()

        offsetInput = {'id':'frames', 'label':'Frames', 'value':0}
        offsetType = {'id':'type', 'label':'Offset', 'items':['Forward --->', 'Backward <---']}
        offseFields = [offsetInput, offsetType]

        getOffsetInput = fx.getInput(title='Frame Offset (Layer Selection)', okText='Run Offset', fields=offseFields)

        if getOffsetInput:
            frameAmount = getOffsetInput['frames']
            if getOffsetInput['type'] == offsetType['items'][1]:
                frameAmount = frameAmount * -1

            for layer in selection:
                if layer.type == 'Layer':
                    object = OffsetLayer(offset=frameAmount, layer=layer)
                    object.runOffset()
                else:
                    print '%s ignored because it is not a Layer' % layer.label

        fx.select(selection)

        viewer.update()
        fx.endUndo()

fx.addAction(OffsetLayerAction())


# _Shape Offset
class OffsetShapesAction(fx.Action):
    __doc__ = ("Time Offset all keyframes for the selected Shapes\n"
                "Note: Once this script is executed you CANNOT Undo this Action")

    def __init__(self):
        fx.Action.__init__(self, 'Time Offset Helper|Offset selected Shapes', root='PicoStyle')

    def available(self):
        session = fx.activeSession()
        assert session, "Select a Session"
        node = session.node(type="RotoNode")
        assert node, "The session does not contain a Roto Node"
        selection = fx.selection()
        assert len(selection) > 0, "There must be more than one selection."

    def execute(self):
        fx.beginUndo('Time Offset Selected Shapes')

        viewer = fx.viewer
        selection = fx.selection()

        offsetInput = {'id':'frames', 'label':'Frames', 'value':0}
        offsetType = {'id':'type', 'label':'Offset', 'items':['Forward --->', 'Backward <---']}
        offseFields = [offsetInput, offsetType]

        getOffsetInput = fx.getInput(title='Frame Offset (Shape Selection)', okText='Run Offset', fields=offseFields)

        if getOffsetInput:
            frameAmount = getOffsetInput['frames']
            if getOffsetInput['type'] == offsetType['items'][1]:
                frameAmount = frameAmount * -1

            for shape in selection:
                if shape.type == 'Shape':
                    object = OffsetShape(offset=frameAmount, shape=shape)
                    object.runOffset()
                else:
                    print '%s ignored because it is not a Shape' % shape.label

        fx.select(selection)

        viewer.update()
        fx.endUndo()

fx.addAction(OffsetShapesAction())


# _Object Offset
class OffsetObjectsAction(fx.Action):
    __doc__ = ("Time Offset all Shapes and Layers with in the current activeNode\n"
                "Note: Once this script is executed you CANNOT Undo this Action")

    def __init__(self):
        fx.Action.__init__(self, 'Time Offset Helper|Offset all objects (Shapes and Layers)', root='PicoStyle')

    def available(self):
        session = fx.activeSession()
        assert session, "Select a Session"
        node = session.node(type="RotoNode")
        assert node, "The session does not contain a Roto Node"

    def execute(self):
        fx.beginUndo('Time Offset All Shapes and Layers')

        viewer = fx.viewer
        node = fx.activeNode()

        offsetInput = {'id':'frames', 'label':'Frames', 'value':0}
        offsetType = {'id':'type', 'label':'Offset', 'items':['Forward --->', 'Backward <---']}
        offseFields = [offsetInput, offsetType]

        getOffsetInput = fx.getInput(title='Frame Offset (Shape Selection)', okText='Run Offset', fields=offseFields)

        if getOffsetInput:
            frameAmount = getOffsetInput['frames']
            if getOffsetInput['type'] == offsetType['items'][1]:
                frameAmount = frameAmount * -1

            for object in node.children:
                if object.type == 'Shape':
                    obj = OffsetShape(offset=frameAmount, shape=object)
                    obj.runOffset()
                elif object.type == 'Layer':
                    obj = OffsetLayer(offset=frameAmount, layer=object)
                    obj.runOffset()
                else:
                    print '%s ignored because it is not a Shape or Layer' % object.label

        viewer.update()
        fx.endUndo()

fx.addAction(OffsetObjectsAction())
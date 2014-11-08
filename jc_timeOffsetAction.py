# Time Offset Helper v2.0
# (c) 2014 Johnny Chan - johnny@picostyle.com
# www.picostyle.com/scripts
# Compatibility: Silhouette v5.2 and up
# --------------------------------------------------

import fx
import jc_timeLayer
import jc_timeShape

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
                    object = jc_timeLayer.OffsetLayer(offset=frameAmount, layer=layer)
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
                    object = jc_timeShape.OffsetShape(offset=frameAmount, shape=shape)
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
                    obj = jc_timeShape.OffsetShape(offset=frameAmount, shape=object)
                    obj.runOffset()
                elif object.type == 'Layer':
                    obj = jc_timeLayer.OffsetLayer(offset=frameAmount, layer=object)
                    obj.runOffset()
                else:
                    print '%s ignored because it is not a Shape or Layer' % object.label

        viewer.update()
        fx.endUndo()

fx.addAction(OffsetObjectsAction())



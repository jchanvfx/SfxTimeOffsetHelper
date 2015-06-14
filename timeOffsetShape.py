# Time Offset Helper (Shape) - Johnny Chan
# --------------------------------------------------
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
                offKey = self.offsetFrames + o
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
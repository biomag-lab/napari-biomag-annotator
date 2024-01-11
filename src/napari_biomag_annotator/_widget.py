"""
This module contains four napari widgets declared in
different ways:

- a pure Python function flagged with `autogenerate: true`
    in the plugin manifest. Type annotations are used by
    magicgui to generate widgets for each parameter. Best
    suited for simple processing tasks - usually taking
    in and/or returning a layer.
- a `magic_factory` decorated function. The `magic_factory`
    decorator allows us to customize aspects of the resulting
    GUI, including the widgets associated with each parameter.
    Best used when you have a very simple processing task,
    but want some control over the autogenerated widgets. If you
    find yourself needing to define lots of nested functions to achieve
    your functionality, maybe look at the `Container` widget!
- a `magicgui.widgets.Container` subclass. This provides lots
    of flexibility and customization options while still supporting
    `magicgui` widgets and convenience methods for creating widgets
    from type annotations. If you want to customize your widgets and
    connect callbacks, this is the best widget option for you.
- a `QWidget` subclass. This provides maximal flexibility but requires
    full specification of widget layouts, callbacks, events, etc.

References:
- Widget specification: https://napari.org/stable/plugins/guides.html?#widgets
- magicgui docs: https://pyapp-kit.github.io/magicgui/

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLabel, QVBoxLayout
from qtpy.QtCore import Qt,QSize
from qtpy.QtGui import QPixmap
from skimage.util import img_as_float
import warnings
import os
import napari_nd_annotator

if TYPE_CHECKING:
    import napari

warnings.filterwarnings('ignore', category=FutureWarning)

class BIOMAGAnnotator(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self.viewer = viewer

        self.titleLabel=QLabel('Welcome to the BIOMAG Annotator plugin')

        self.logoFile='biomag-logo'#'biomag_logo'

        self.logo=QLabel()
        max_size=QSize(250,250)
        pixmap=QPixmap(os.path.join(os.path.dirname(__file__),'icon',self.logoFile+'.png')) #'.svg'))
        scaled=pixmap.scaled(max_size,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.logo.setPixmap(scaled)

        self.btn1 = QPushButton('AnnotatorJ')
        self.btn1.setToolTip('Open AnnotatorJ')
        self.btn1.clicked.connect(self.openAnnotatorJ)

        self.btn2 = QPushButton('Minimal Contour')
        self.btn2.setToolTip('Open Minimal Contour')
        self.btn2.clicked.connect(self.openMinContour)

        self.btn3 = QPushButton('Interpolation')
        self.btn3.setToolTip('Open Interpolation')
        self.btn3.clicked.connect(self.openInterpol)

        self.btn4 = QPushButton('Minimal Surface')
        if napari_nd_annotator.MinimalSurfaceWidget is None:
            self.btn4.setToolTip("'minimal_surface' Python package is required")
            self.btn4.setEnabled(False)
        else:
            self.btn4.setToolTip('Open Minimal Surface')
        self.btn4.clicked.connect(self.openMinSurface)

        self.mainVBox=QVBoxLayout()
        self.logoHBox=QHBoxLayout()
        self.topRow=QHBoxLayout()
        self.bottomRow=QHBoxLayout()

        self.logoHBox.addWidget(self.logo)
        self.logoHBox.setAlignment(Qt.AlignCenter)
        self.topRow.addWidget(self.btn1)
        self.topRow.addWidget(self.btn2)
        self.bottomRow.addWidget(self.btn3)
        self.bottomRow.addWidget(self.btn4)

        self.mainVBox.addLayout(self.logoHBox)
        self.mainVBox.addLayout(self.topRow)
        self.mainVBox.addLayout(self.bottomRow)

        self.setLayout(self.mainVBox)

    def openAnnotatorJ(self):
        import napari_annotatorj
        pluginInstance=napari_annotatorj.AnnotatorJ(self.viewer)
        self.viewer.window.add_dock_widget(pluginInstance,name='AnnotatorJ')

    def openMinContour(self):
        import napari_nd_annotator
        pluginInstance=napari_nd_annotator._widgets.annotator_module.MinimalContourWidget(self.viewer)
        self.viewer.window.add_dock_widget(pluginInstance,name='Minimal Contour')
        return pluginInstance

    def openInterpol(self):
        import napari_nd_annotator
        pluginInstance=napari_nd_annotator.InterpolationWidget(self.viewer)
        self.viewer.window.add_dock_widget(pluginInstance,name='Slice Interpolation')

    def openMinSurface(self):
        import napari_nd_annotator
        if napari_nd_annotator.MinimalSurfaceWidget is None:
            return
        min_contour = self.openMinContour()
        pluginInstance=napari_nd_annotator.MinimalSurfaceWidget(self.viewer, min_contour)
        self.viewer.window.add_dock_widget(pluginInstance,name='Minimal Surface')

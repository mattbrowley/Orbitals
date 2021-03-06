# -*- coding: utf-8 -*-
# This program is licenced under an MIT license. Full licence is at the end of
# this file.
"""
Orbitals_UI.py
A user interface for generating and interacting with various animations of
hydrogenic wavefunctions.

@author: Matthew B Rowley
"""
from __future__ import division
import os
# This must be called before importing traits and mayavi elements
os.environ['ETS_TOOLKIT'] = 'qt4'
from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
import Hydrogenic as hyd
import numpy as np
import pyqtgraph as pg
import pickle
#os.environ['ETS_TOOLKIT'] = 'qt4'

sqrt2 = np.sqrt(2)

class MainWindow(QtGui.QMainWindow):
    """ Main Window for the UI"""
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle("Orbitals!")
        self.frame = QtGui.QFrame(self)
        self.layout = QtGui.QHBoxLayout(self.frame)
        self.left_layout = QtGui.QVBoxLayout()
        self.tabs = QtGui.QTabWidget(self, )
        self.tabs.addTab(StationaryPanel(self), 'Stationary States')
        self.tabs.addTab(CoherencePanel(self), 'Coherences')
        self.cross_tab = CrossingPanel(self)
        self.tabs.addTab(self.cross_tab, 'Avoided Crossing')
        self.tabs.setMaximumWidth(550)
        self.tabs.currentChanged.connect(self.changeTab)
        self.left_layout.addWidget(self.tabs)
        self.author = AuthorPanel(self)
        self.left_layout.addWidget(self.author)
        self.layout.addLayout(self.left_layout)
        self.mayavi_widget = MayaviQWidget(self.frame)
        self.layout.addWidget(self.mayavi_widget)
        self.setCentralWidget(self.frame)
        self.changeTab()  # Create the visualization after the UI is made

    def closeEvent(self, evt):
        global calculator
        QtGui.QMainWindow.closeEvent(self, evt)
        calculator.animation_timer.stop()

    def changeTab(self):
        """A new tab has been selected. It may be necessary to reinitialize
        the visualization widget"""
        global calculator
        calculator.writeMode(self.tabs.tabText(self.tabs.currentIndex()))
        self.cross_tab.tabChange(self.tabs.tabText(self.tabs.currentIndex()))


class OrbitalsPanel(QtGui.QWidget):
    """A panel for selecting a hydrogenic orbital, either from a selection
    of real orbitals or by selecting the quantum numbers"""
    def __init__(self, my_orbital, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.my_orbital = my_orbital
        self.n = 2
        self.l = 1
        self.m = 0
        self.s = 1
        self.layout = QtGui.QVBoxLayout(self)
        self.real = QtGui.QVBoxLayout()
        self.s1_layout = QtGui.QHBoxLayout()
        self.s1_layout.addItem(HorizontalSpacer())
        self.s1 = OrbitalButton(self.my_orbital, self, text='1s')
        self.s1_layout.addWidget(self.s1)
        self.s1_layout.addItem(HorizontalSpacer())
        self.real.addLayout(self.s1_layout)
        self.real.addWidget(CenteredLine(self))
        self.s2_layout = QtGui.QHBoxLayout()
        self.s2_layout.addItem(HorizontalSpacer())
        self.s2 = OrbitalButton(self.my_orbital, self, text='2s')
        self.s2_layout.addWidget(self.s2)
        self.s2_layout.addItem(HorizontalSpacer())
        self.real.addLayout(self.s2_layout)
        self.p2_layout = QtGui.QHBoxLayout()
        self.p2_layout.addItem(HorizontalSpacer())
        self.p2x = OrbitalButton(self.my_orbital, self, text='2px')
        self.p2_layout.addWidget(self.p2x)
        self.p2y = OrbitalButton(self.my_orbital, self, text='2py')
        self.p2_layout.addWidget(self.p2y)
        self.p2z = OrbitalButton(self.my_orbital, self, text='2pz')
        self.p2_layout.addWidget(self.p2z)
        self.p2_layout.addItem(HorizontalSpacer())
        self.real.addLayout(self.p2_layout)
        self.real.addWidget(CenteredLine(self))
        self.p3_layout = QtGui.QHBoxLayout()
        self.p3_layout.addItem(HorizontalSpacer())
        self.p3x = OrbitalButton(self.my_orbital, self, text='3px')
        self.p3_layout.addWidget(self.p3x)
        self.p3y = OrbitalButton(self.my_orbital, self, text='3py')
        self.p3_layout.addWidget(self.p3y)
        self.p3z = OrbitalButton(self.my_orbital, self, text='3pz')
        self.p3_layout.addWidget(self.p3z)
        self.p3_layout.addItem(HorizontalSpacer())
        self.real.addLayout(self.p3_layout)
        self.d3_layout = QtGui.QHBoxLayout()
        self.d3_layout.addItem(HorizontalSpacer())
        self.d3z2 = OrbitalButton(self.my_orbital, self, text='3dz^2')
        self.d3_layout.addWidget(self.d3z2)
        self.d3xz = OrbitalButton(self.my_orbital, self, text='3dxz')
        self.d3_layout.addWidget(self.d3xz)
        self.d3_layout.addItem(HorizontalSpacer())
        self.real.addLayout(self.d3_layout)
        self.d3_layout2 = QtGui.QHBoxLayout()
        self.d3_layout2.addItem(HorizontalSpacer())
        self.d3yz = OrbitalButton(self.my_orbital, self, text='3dyz')
        self.d3_layout2.addWidget(self.d3yz)
        self.d3x2y2 = OrbitalButton(self.my_orbital, self, text='3dx^2-y^2')
        self.d3_layout2.addWidget(self.d3x2y2)
        self.d3xy = OrbitalButton(self.my_orbital, self, text='3dxy')
        self.d3_layout2.addWidget(self.d3xy)
        self.d3_layout2.addItem(HorizontalSpacer())
        self.real.addLayout(self.d3_layout2)
        self.real.addWidget(CenteredLine(self))
        self.f4_layout = QtGui.QHBoxLayout()
        self.f4_layout.addItem(HorizontalSpacer())
        self.f4z3 = OrbitalButton(self.my_orbital, self, text='4fz^3')
        self.f4_layout.addWidget(self.f4z3)
        self.f4xz2 = OrbitalButton(self.my_orbital, self, text='4fxz^2')
        self.f4_layout.addWidget(self.f4xz2)
        self.f4yz2 = OrbitalButton(self.my_orbital, self, text='4fyz^2')
        self.f4_layout.addWidget(self.f4yz2)
        self.f4_layout.addItem(HorizontalSpacer())
        self.real.addLayout(self.f4_layout)
        self.f4_layout2 = QtGui.QHBoxLayout()
        self.f4_layout2.addItem(HorizontalSpacer())
        self.f4xyz = OrbitalButton(self.my_orbital, self, text='4fxyz')
        self.f4_layout2.addWidget(self.f4xyz)
        self.f4zx2y2 = OrbitalButton(self.my_orbital, self, text='4fz(x^2-y^2)')
        self.f4_layout2.addWidget(self.f4zx2y2)
        self.f4_layout2.addItem(HorizontalSpacer())
        self.real.addLayout(self.f4_layout2)
        self.f4_layout3 = QtGui.QHBoxLayout()
        self.f4_layout3.addItem(HorizontalSpacer())
        self.f4xx23y2 = OrbitalButton(self.my_orbital, self, text='4fx(x^2-3y^2)')
        self.f4_layout3.addWidget(self.f4xx23y2)
        self.f4zy3x2y2 = OrbitalButton(self.my_orbital, self, text='4fy(3x^2-y^2)')
        self.f4_layout3.addWidget(self.f4zy3x2y2)
        self.f4_layout3.addItem(HorizontalSpacer())
        self.real.addLayout(self.f4_layout3)
        self.real.addItem(VerticalSpacer())
        self.layout.addLayout(self.real)
        self.layout.addWidget(HorizontalLine(self))
        self.numbers_layout = QtGui.QHBoxLayout()
        self.num_label = QtGui.QLabel(self,
                                      text='Set Quantum Numbers Manually')
        self.layout.addWidget(self.num_label)
        self.n_label = QtGui.QLabel(self, text='n')
        self.numbers_layout.addWidget(self.n_label)
        self.num_n = QtGui.QSpinBox(self)
        self.num_n.setMinimum(1)
        self.num_n.valueChanged.connect(self.testNumbers)
        self.numbers_layout.addWidget(self.num_n)
        self.numbers_layout.addItem(HorizontalSpacer())
        self.numbers_layout.addWidget(VerticalLine(self))
        self.numbers_layout.addItem(HorizontalSpacer())
        self.l_label = QtGui.QLabel(self, text='l')
        self.numbers_layout.addWidget(self.l_label)
        self.num_l = QtGui.QSpinBox(self)
        self.num_l.valueChanged.connect(self.testNumbers)
        self.numbers_layout.addWidget(self.num_l)
        self.numbers_layout.addItem(HorizontalSpacer())
        self.numbers_layout.addWidget(VerticalLine(self))
        self.numbers_layout.addItem(HorizontalSpacer())
        self.m_label = QtGui.QLabel(self, text='m')
        self.numbers_layout.addWidget(self.m_label)
        self.num_m = QtGui.QSpinBox(self)
        self.num_m.valueChanged.connect(self.testNumbers)
        self.numbers_layout.addWidget(self.num_m)
        self.numbers_layout.addItem(HorizontalSpacer())
        self.numbers_layout.addWidget(VerticalLine(self))
        self.numbers_layout.addItem(HorizontalSpacer())
        self.s_label = QtGui.QLabel(self, text='s')
        self.numbers_layout.addWidget(self.s_label)
        self.num_s = QtGui.QSpinBox(self)
        self.num_s.valueChanged.connect(self.testNumbers)
        self.num_s.setRange(-1, 1)
        self.num_s.setValue(1)
        self.numbers_layout.addWidget(self.num_s)
        self.layout.addLayout(self.numbers_layout)
        self.layout.addItem(VerticalSpacer())

    def chooseNumbers(self):
        self.my_orbital.writeNumbers([self.n, self.l, self.m, self.s])
        signals.orbital_change.emit()

    def testNumbers(self):
        self.valid_numbers = True
        self.n = self.num_n.value()
        self.num_l.setMaximum(self.n - 1)
        self.l = self.num_l.value()
        self.num_m.setRange(-self.l, self.l)
        self.m = self.num_m.value()
        if self.num_s.value() == 0:
            self.s = -self.s
            self.num_s.setValue(self.s)
        self.chooseNumbers()


class StationaryPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        self.stationary_orbital = OrbitalMutex()
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.inst_button = InstructionsButton(self, my_file='Stationary.txt')
        self.layout.addWidget(self.inst_button)
        self.layout.addWidget(HorizontalLine(self))
        self.orbitals = OrbitalsPanel(stationary_orbital, self)
        self.layout.addWidget(self.orbitals)
        self.animate_button = QtGui.QPushButton(self,
                                                text='Start/Stop Animation')
        self.layout.addWidget(self.animate_button)
        self.animate_button.clicked.connect(signals.animate_orbital.emit)


class CoherencePanel(QtGui.QWidget):
    def __init__(self, parent=None, state=None):
        global ket_orbital, bra_orbital, signals, cycle
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.options = QtGui.QHBoxLayout()
        self.coherence = QtGui.QRadioButton(self, text='Show Coherence')
        self.coherence.setChecked(True)
        self.options.addWidget(self.coherence)
        self.rabi = QtGui.QRadioButton(self, text='Show Rabi Cycle')
        self.options.addWidget(self.rabi)
        self.fid = QtGui.QRadioButton(self, text='Show FID')
        self.options.addWidget(self.fid)
        self.i_button = InstructionsButton(self, my_file='Coherences.txt')
        self.options.addWidget(self.i_button)
        self.layout.addLayout(self.options)
        self.functions = QtGui.QHBoxLayout()
        self.ket_layout = QtGui.QVBoxLayout()
        self.ket_label = QtGui.QLabel(self, text='Lower State    |ket>')
        self.ket_label.setAlignment(QtCore.Qt.AlignRight)
        self.ket_layout.addWidget(self.ket_label)
        self.ket_layout.addWidget(HorizontalLine())
        self.ket_orbitals = OrbitalsPanel(ket_orbital, self)
        self.ket_layout.addWidget(self.ket_orbitals)
        self.bra_layout = QtGui.QVBoxLayout()
        self.bra_label = QtGui.QLabel(self, text='<bra|    Upper State')
        self.bra_layout.addWidget(self.bra_label)
        self.bra_layout.addWidget(HorizontalLine())
        self.bra_orbitals = OrbitalsPanel(bra_orbital, self)
        self.bra_layout.addWidget(self.bra_orbitals)
        self.functions.addLayout(self.ket_layout)
        self.functions.addWidget(VerticalLine())
        self.functions.addLayout(self.bra_layout)
        self.layout.addLayout(self.functions)
        self.animate_button = QtGui.QPushButton(self,
                                                text='Start/Stop Animation')
        self.layout.addWidget(self.animate_button)
        self.animate_button.clicked.connect(signals.animate_orbital.emit)
        self.rabi.clicked.connect(self.changeCycle)
        self.fid.clicked.connect(self.changeCycle)
        self.coherence.clicked.connect(self.changeCycle)

    def changeCycle(self):
        cycle_vals = [self.coherence.isChecked(), self.rabi.isChecked(),
                      self.fid.isChecked()]
        cycle.write(cycle_vals)
        signals.cycle_change.emit()


class CrossingPanel(QtGui.QWidget):
    '''
    A panel for displaying the energy curves and wavefunctions involved
    in photodissociation with an avoided crossing.

    Because these animations are much different from the others, everything
    is self-contained in this class rather than trying to unify it with the
    OrbitalCalculator class.
    '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        # Get the data for the avoided crossing
        pickle_foldername = os.path.join(os.getcwd(),'Crossings_Data')
        pickle_filename = os.path.join(pickle_foldername, 'pickled_data.p')
        with open(pickle_filename, 'r') as file:
            pickled_data = pickle.load(file)
        self.bond_lengths = pickled_data['bond_lengths']
        self.Low_A_Curve = pickled_data['Low_A_Curve']
        self.High_A_Curve = pickled_data['High_A_Curve']
        self.Low_D_Curve = pickled_data['Low_D_Curve']
        self.High_D_Curve = pickled_data['High_D_Curve']
        self.Low_A_MO = pickled_data['Low_A_MO']
        self.High_A_MO = pickled_data['High_A_MO']
        self.Low_D_MO = pickled_data['Low_D_MO']
        self.High_D_MO = pickled_data['High_D_MO']
        self.a_curves = True
        # Now set up the GUI
        self.layout = QtGui.QVBoxLayout(self)
        self.options = QtGui.QHBoxLayout()
        self.adiabat = QtGui.QRadioButton(self, text='Adiabatic Curves')
        self.adiabat.setChecked(True)
        self.options.addWidget(self.adiabat)
        self.adiabat.clicked.connect(self.changeCurves)
        self.diabat = QtGui.QRadioButton(self, text='Diabatic Curves')
        self.options.addWidget(self.diabat)
        self.diabat.clicked.connect(self.changeCurves)
        self.i_button = InstructionsButton(self, my_file='Crossing.txt')
        self.options.addWidget(self.i_button)
        self.layout.addLayout(self.options)
        self.plot_object = pg.PlotWidget()
        self.plot_object.getPlotItem().setMouseEnabled(False, False)
        self.plot_object.setLabel('bottom', 'Bond Length', units='α')
        self.plot_object.setLabel('left', 'Energy')
        self.plot_object.hideAxis('left')
        # Create and add things to the plot widget
        self.curve_AH = pg.PlotCurveItem(pen=(30, 100))
        self.curve_AH.setData(self.bond_lengths, self.High_A_Curve)
        self.plot_object.addItem(self.curve_AH)
        self.curve_AL = pg.PlotCurveItem(pen=(20, 100))
        self.curve_AL.setData(self.bond_lengths, self.Low_A_Curve)
        self.plot_object.addItem(self.curve_AL)
        self.curve_DH = pg.PlotCurveItem(pen=(90, 100))
        self.curve_DH.setData(self.bond_lengths, self.High_D_Curve)
        self.plot_object.addItem(self.curve_DH)
        self.curve_DL = pg.PlotCurveItem(pen=(80, 100))
        self.curve_DL.setData(self.bond_lengths, self.Low_D_Curve)
        self.plot_object.addItem(self.curve_DL)
        self.curser = pg.InfiniteLine(pos=0, angle=90, bounds=[1.5,5.0],
                                      pen=pg.mkPen(width=3, color='g'),
                                      movable=True)
        self.curser.sigPositionChanged.connect(self.curserMoved)
        self.plot_object.addItem(self.curser)
        self.layout.addWidget(self.plot_object)
        self.layout.addItem(VerticalSpacer())
        self.animate_button = QtGui.QPushButton(self,
                                                text='Start/Stop Animation')
        self.layout.addWidget(self.animate_button)
        self.animate_button.clicked.connect(self.animationPressed)
        self.animating = False
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.timeout.connect(self.animateFrame)
        self.vid_frame = 0

    def changeCurves(self):
        if self.adiabat.isChecked():
            self.a_curves = True
        else:
            self.a_curves = False
        self.renderFrame()

    def tabChange(self, tab):
        if tab == 'Avoided Crossing':
            self.vid_frame = 0
            zoom.write(True)
            self.preparePoints()
            signals.create_crossing.emit()
        else:
            if self.animating:
                self.animation_timer.stop()
                self.animating = False
                self.curser.sigPositionChanged.connect(self.curserMoved)

    def curserMoved(self):
        if self.animating:
            self.animating = False
            self.animation_timer.stop()
        position = self.curser.getPos()[0]
        for i in range(100):
            if self.bond_lengths[i] >= position:
                self.vid_frame = i
                break
        self.preparePoints()
        self.renderFrame()

    def preparePoints(self):
        i = self.vid_frame
        if self.a_curves:
            data = (self.bond_lengths[i], self.Low_A_MO[i],
                    self.High_A_MO[i])
        else:
            data = (self.bond_lengths[i], self.Low_D_MO[i],
                    self.High_D_MO[i])
        points.writePoints((data))

    def animateFrame(self):
        self.renderFrame()
        self.curser.setValue(self.bond_lengths[self.vid_frame])
        self.vid_frame = self.vid_frame + 1
        if(self.vid_frame >= 100):
            self.animationPressed()

    def renderFrame(self):
        self.preparePoints()
        signals.update_crossing.emit()

    def animationPressed(self):
        if self.animating:
            self.animating = False
            self.animation_timer.stop()
            self.curser.sigPositionChanged.connect(self.curserMoved)
        else:
            if(self.vid_frame >= 100):
                self.vid_frame = 0
            self.curser.sigPositionChanged.disconnect()
            self.animation_timer.start(50)
            self.animating = True


class AuthorPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.author = QtGui.QLabel(self,
                                   text='Written by: Matthew Rowley - 2015')
        self.layout.addWidget(self.author)
        self.email_label = QtGui.QLabel(self,
                                        text='email: Matt.B.Rowley@gmail.com')
        self.layout.addWidget(self.email_label)


class VerticalSpacer(QtGui.QSpacerItem):
    def __init__(self):
        QtGui.QSpacerItem.__init__(self, 20, 20, QtGui.QSizePolicy.Minimum,
                                   QtGui.QSizePolicy.Expanding)


class HorizontalSpacer(QtGui.QSpacerItem):
    def __init__(self, width=20, height=20,
                 Horizontal_Policy=QtGui.QSizePolicy.Expanding):
        QtGui.QSpacerItem.__init__(self, width, height, Horizontal_Policy,
                                   QtGui.QSizePolicy.Minimum)


class VerticalLine(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setFrameShape(QtGui.QFrame.VLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)


class CenteredLine(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.addItem(HorizontalSpacer(30, 1, QtGui.QSizePolicy.Fixed))
        self.layout.addWidget(HorizontalLine())
        self.layout.addItem(HorizontalSpacer(30, 1, QtGui.QSizePolicy.Fixed))


class HorizontalLine(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setFrameShape(QtGui.QFrame.HLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)


class OrbitalButton(QtGui.QPushButton):
    '''
    A button which will pass the appropriate orbital wavefunction.
    '''
    def __init__(self, my_orbital, parent=None, text=''):
        QtGui.QPushButton.__init__(self, parent=None, text=text)
        self.clicked.connect(self.writeOrbital)
        self.target_text = text
        self.my_orbital = my_orbital

    def writeOrbital(self):
        global signals
        self.my_orbital.writeName(self.target_text)
        signals.orbital_change.emit()


class InstructionsButton(QtGui.QPushButton):
    '''
    A button which will call up an appropriate InstructionsDialog dialog
    window. Pass the my_file keyword argument for the appropriate .txt file
    filename.
    '''
    def __init__(self, my_orbital, parent=None, my_file=''):
        QtGui.QPushButton.__init__(self, parent=parent, text='Instructions')
        self.clicked.connect(self.showInstructions)
        self.my_file = my_file

    def showInstructions(self):
        try:
            this_file_path = os.path.abspath(__file__)
            this_folder_path = os.path.dirname(this_file_path)
            folderpath = os.path.join(this_folder_path, 'Tab_Instructions')
            filename = os.path.join(folderpath, self.my_file)
            with open(filename, "r") as instructions_file:
                lines = instructions_file.readlines()
            self.instruction_dialog = InstructionsDialog(lines=lines)
        except Exception as e:
            print(e)


class InstructionsDialog(QtGui.QDialog):
    '''
    A pop-up window to explain each tab with instructions which can be changed
    and customized by editing the appropriate .txt file.
    '''
    def __init__(self, parent=None, lines=[]):
        QtGui.QDialog.__init__(self, parent=parent)
        self.setWindowTitle(lines[0][:-1])
        self.layout = QtGui.QVBoxLayout(self)
        text = ''
        for line in lines[1:]:
            text = text + line
        self.layout.addWidget(QtGui.QLabel(text=text))
        self.close_button = QtGui.QPushButton(text='Close')
        self.layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)
        self.show()

    def closeWindow(self):
        self.close()


class Visualization(HasTraits):
    '''
    Mayavi visualization
    '''
    scene = Instance(MlabSceneModel, ())
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True  # We need this to resize with the parent widget
                )

    def createOrbital(self):
        global points
        self.scene.mlab.clf()
        x, y, z, psi = points.readPoints()
        self.mesh = self.scene.mlab.mesh(x, y, z, scalars=psi, colormap='hsv',
                                         vmax=np.pi, vmin=-np.pi)
        # This low res colormap is simpler and less distracting
        my_map = [[255, 0, 0, 255], [140, 0, 140, 255], [140, 0, 140, 255],
                  [0, 0, 255, 255], [0, 0, 255, 255], [255, 153, 18, 255],
                  [255, 153, 18, 255], [255, 0, 0, 255]]
        # Comment out the next line to use a smoother high res colormap
        self.mesh.module_manager.scalar_lut_manager.lut.table = my_map
        self.axes = self.scene.mlab.axes()
        self.fig = self.scene.mlab.gcf()
        self.source = self.mesh.mlab_source
        if zoom.read():
            self.scene.mlab.view(0, 90, np.max((x, y, z))*5, (0, 0, 0))
            self.scene.reset_zoom()

    def updateOrbital(self):
        global points, zoom
        x, y, z, psi = points.readPoints()
        self.source.set(x=x, y=y, z=z, scalars=psi)
        if zoom.read():
            self.scene.reset_zoom()
        self.axes.remove()
        self.axes = self.scene.mlab.axes()

    def createCrossing(self):
        self.scene.mlab.clf()
        bond_length, Low, High = points.readPoints()
        self.High_mesh = self.scene.mlab.mesh(High[0], High[1], High[2],
                                              color=(.9,.1,.1), opacity=0.95)
        self.Low_mesh = self.scene.mlab.mesh(Low[0], Low[1], Low[2],
                                             color=(.1,.1,.9), opacity=0.95)
        self.Cl_point = self.scene.mlab.points3d(0, 0, 0, resolution = 12,
                                                 color=(0,1,0))
        self.Br_point = self.scene.mlab.points3d(0., 0., 1.5,
                                                 resolution = 12,
                                                 color=(0.6,0.4,0.7))
        self.axes = self.scene.mlab.axes()
        self.fig = self.scene.mlab.gcf()
        self.Br_source = self.Br_point.mlab_source
        self.Low_source = self.Low_mesh.mlab_source
        self.High_source = self.High_mesh.mlab_source
        self.scene.mlab.view(0, 90, roll=0, focalpoint=(0, 0, 0))
        if zoom.read():
            self.scene.reset_zoom()

    def updateCrossing(self):
        bond_length, Low, High = points.readPoints()
        self.Low_source.set(x=Low[0], y=Low[1], z=Low[2])
        self.High_source.set(x=High[0], y=High[1], z=High[2])
        self.Br_source.set(x=0, y=0, z=bond_length)
        if zoom.read():
            self.scene.reset_zoom()
        self.axes.remove()
        self.axes = self.scene.mlab.axes()


class MayaviQWidget(QtGui.QWidget):
    '''
    Widget containing the visualization
    '''
    def __init__(self, parent=None):
        global signals
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.visualization = Visualization()
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)
        signals.update_orbital.connect(self.visualization.updateOrbital)
        signals.create_orbital.connect(self.visualization.createOrbital)
        signals.update_crossing.connect(self.visualization.updateCrossing)
        signals.create_crossing.connect(self.visualization.createCrossing)


class OrbitalCalculator(object):
    '''
    Calculates the appropriate surface to graph for stationary states
    and coherences. Avoided crossings are handled separately.
    '''
    def __init__(self, stationary_orbital, ket_orbital, bra_orbital,
                 signals, zoom, points):
        object.__init__(self)
        self.stationary_orbital = stationary_orbital
        self.ket_orbital = ket_orbital
        self.bra_orbital = bra_orbital
        self.times = np.linspace(0, 2*np.pi, 100)
        self.signals = signals
        self.zoom = zoom
        self.points = points
        self.mode = 'Stationary States'
        self.coherence = True
        self.rabi = False
        self.fid = False
        self.animating = False
        self.i = 0
        self.phi, self.theta = np.mgrid[0:np.pi:50j, 0:2*np.pi:100j]
        self.signals.orbital_change.connect(self.orbitalChange)
        self.signals.animate_orbital.connect(self.animateClicked)
        self.signals.cycle_change.connect(self.cycleChanged)
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.timeout.connect(self.runStationary)

    def writeMode(self, new_mode):
        '''
        Set the variable which keeps track of which tab is currently selected
        '''
        self.animation_timer.stop()
        self.animating = False
        self.mode = new_mode
        self.animation_timer = QtCore.QTimer()
        if self.mode == 'Stationary States':
            self.stationaryMode()
        elif self.mode == 'Coherences':
            self.coherencesMode()
        elif self.mode == 'Avoided Crossing':
            self.crossingsMode()

    def stationaryMode(self):
        '''Prepare the visualization for stationary states mode'''
        self.animation_timer.timeout.connect(self.runStationary)
        self.times = np.linspace(0, 2*np.pi, 100)
        self.changeStationary(first=True)

    def coherencesMode(self):
        '''Prepare the visualization for coherences mode'''
        self.animation_timer.timeout.connect(self.runCoherence)
        self.zoom.write(False)
        self.changeCoherence(first=True)

    def crossingsMode(self):
        '''Prepare the visualization for avoided crossings mode'''
        self.animation_timer.stop()
        self.animating = False

    def changeStationary(self, first=False):
        '''Update the visualization when a new orbital is selected.'''
        self.orbital = self.stationary_orbital.read()
        self.r = self.orbital.r_90p
        self.x = self.r * np.sin(self.phi) * np.cos(self.theta)
        self.y = self.r * np.sin(self.phi) * np.sin(self.theta)
        self.z = self.r * np.cos(self.phi)
        self.rs = (np.conj(self.orbital.angular(self.theta, self.phi)) *
                   self.orbital.angular(self.theta, self.phi)).real
        #self.rs = self.rs / np.max(self.rs) * self.r
        self.calculateStationary()
        self.zoom.write(True)
        if first:
            self.signals.create_orbital.emit()
        else:
            self.signals.update_orbital.emit()

    def changeCoherence(self, first=False):
        '''Update the visualization when a new orbital is selected.'''
        self.ket = self.ket_orbital.read()
        self.bra = self.bra_orbital.read()
        if self.coherence is True:
            self.times = np.linspace(0, 2*np.pi, 1000)
            self.radial = self.radialNoCycle
            self.angular = self.angularNoCycle
        else:
            self.radial = self.radialRabiCycle
            self.angular = self.angularRabiCycle
            if self.rabi is True:
                self.times = np.linspace(0, 2*np.pi, 1000)
            else:
                self.times = np.linspace(np.pi/4, np.pi/2., 125)
        self.calculateCoherence()
        if first:
            self.signals.create_orbital.emit()
        else:
            self.signals.update_orbital.emit()

    def orbitalChange(self):
        '''Update the visualization when a new orbital is selected.'''
        if self.mode == 'Stationary States':
            self.changeStationary()
        elif self.mode == 'Coherences':
            self.changeCoherence()

    def animateClicked(self):
        '''Start or stop the animation'''
        if not self.animating:
            self.zoom.write(False)  # Zooming during animations is disorienting
            self.animation_timer.start(30)
            self.animating = True
        else:
            self.animation_timer.stop()
            self.animating = False

    def cycleChanged(self):
        cycle_vals = cycle.read()
        self.coherence, self.rabi, self.fid = cycle_vals
        self.changeCoherence()

    def runStationary(self):
        self.calculateStationary()
        self.i = self.i + 1
        self.signals.update_orbital.emit()

    def calculateStationary(self):
        time = self.times[self.i % len(self.times)]
        psi = np.angle(self.orbital.angular(self.theta, self.phi) *
                       np.exp(1j * self.orbital.bohr * time))
        data = (self.rs*self.x, self.rs*self.y, self.rs*self.z, psi)
        self.points.writePoints(data)

    def runCoherence(self):
        self.calculateCoherence()
        self.signals.update_orbital.emit()
        self.i = self.i + 1

    def calculateCoherence(self):
        t = self.times[self.i % len(self.times)]
        r = self.radial(t)
        x = r * np.sin(self.phi) * np.cos(self.theta)
        y = r * np.sin(self.phi) * np.sin(self.theta)
        z = r * np.cos(self.phi)
        angular = self.angular(self.theta, self.phi, t)
        rs = (np.conj(angular) * angular).real
        #rs = rs / np.max(rs)
        psi = np.angle(angular)
        data = (rs*x, rs*y, rs*z, psi)
        self.points.writePoints(data)

    def radialNoCycle(self, t):
        radius = 0.5*(self.ket.r_90p + self.bra.r_90p)
        return radius

    def angularNoCycle(self, theta, phi, t):
        return 0.5*sqrt2*(np.exp(1j*self.ket.bohr*t) * self.ket.angular(theta, phi) +
                          np.exp(1j*self.bra.bohr*t) * self.bra.angular(theta, phi))

    def radialRabiCycle(self, t):
        radius = (np.sin(t)*np.sin(t)*self.ket.r_90p +
                  np.cos(t)*np.cos(t)*self.bra.r_90p)
        return radius

    def angularRabiCycle(self, theta, phi, t):
        return (np.sin(t) * np.exp(1j*self.ket.bohr*t) *
                self.ket.angular(theta, phi) +
                np.cos(t) * np.exp(1j*self.bra.bohr*t) *
                self.bra.angular(theta, phi))

class OrbitalMutex(QtCore.QMutex):
    '''
    Stores a Hydrogenic.Orbital object
    '''
    def __init__(self, orbital = hyd.orbitals['2pz'], bohr = 1):
        QtCore.QMutex.__init__(self)
        self.bohr = bohr
        self.orbital = orbital
        self.orbital.setBohr(self.bohr)

    def read(self):
        return self.orbital

    def writeName(self, new_name):
        self.lock()
        self.orbital = hyd.orbitals[new_name]
        self.orbital.setBohr(self.bohr)
        self.unlock()

    def writeNumbers(self, new_numbers):
        self.lock()
        n = new_numbers[0]
        l = new_numbers[1]
        m = new_numbers[2]
        s = new_numbers[3]
        self.orbital = hyd.Orbital(n, l, m, s)
        self.orbital.setBohr(self.bohr)
        self.unlock()


class PointsMutex(QtCore.QMutex):
    '''
    Stores the points for visualization
    '''
    def __init__(self):
        QtCore.QMutex.__init__(self)
        self.points = (0, 0, 0, 0)

    def readPoints(self):
        return self.points

    def writePoints(self, new_points):
        self.lock()
        self.points = new_points
        self.unlock()

class BoolMutex(QtCore.QMutex):
    '''
    Stores a boolean variable
    '''
    def __init__(self, init_value=False):
        QtCore.QMutex.__init__(self)
        self.value = init_value

    def read(self):
        return self.value

    def write(self, new_value):
        self.lock()
        self.value = new_value
        self.unlock()

class SignalBus(QtCore.QObject):
    '''
    A QObject that holds all the pyqtSignals
    '''
    orbital_change = QtCore.pyqtSignal()
    cycle_change = QtCore.pyqtSignal()
    animate_orbital = QtCore.pyqtSignal()
    create_orbital = QtCore.pyqtSignal()
    update_orbital = QtCore.pyqtSignal()
    frame_rendered = QtCore.pyqtSignal()
    create_crossing = QtCore.pyqtSignal()
    update_crossing = QtCore.pyqtSignal()


signals = SignalBus()
stationary_orbital = OrbitalMutex(orbital = hyd.orbitals['1s'], bohr = 1)
bra_orbital = OrbitalMutex(orbital = hyd.orbitals['2pz'], bohr = 50)
ket_orbital = OrbitalMutex(orbital = hyd.orbitals['1s'], bohr = 10)
points = PointsMutex()
zoom = BoolMutex(init_value=True)
cycle = BoolMutex(init_value=[True,False,False])
calculator = OrbitalCalculator(stationary_orbital, ket_orbital, bra_orbital,
                               signals, zoom, points)

# The MIT License (MIT)
#
# Copyright (c) 2015 Matthew B Rowley
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

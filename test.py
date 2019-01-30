import math
import sys
import os
import csv
import heapq
import time
import copy
import functools

from collections import defaultdict, namedtuple


def infer_call(func):
    '''decorator function to call super method
    Tips: call self first, then call super!!!
    '''

    @functools.wraps(func)
    def wrapper(self, *args, **kw):
        func(self, *args, **kw)
        getattr(super(type(self), self), func.__name__)(*args, **kw)

    return wrapper


class A:
    def test(self):
        print('A')


class B(A):
    # @infer_call
    def test(self):
        print('B')
        # return
        # super(B, self).test()
        getattr(super(type(self), self), self.test.__name__)()

def testVTK():
    print(vtk.VTK_VERSION, sys.version)

    line = vtk.vtkLineSource()
    line.SetPoint1(0, 0, 0)
    line.SetPoint2(5, 0, 0)
    # tubeFilter = vtk.vtkTubeFilter()
    # tubeFilter.SetInputConnection(line.GetOutputPort())
    # tubeFilter.SetRadius(0.1)
    # tubeFilter.SetNumberOfSides(8)
    # tubeFilter.CappingOn()

    cone_a = vtk.vtkConeSource()
    cone_a.SetHeight(10)
    cone_a.SetRadius(5)
    cone_a.SetResolution(30)

    coneMapper1 = vtk.vtkPolyDataMapper()
    coneMapper1.SetInputConnection(cone_a.GetOutputPort())
    coneMapper2 = vtk.vtkPolyDataMapper()
    # coneMapper2.SetInputConnection(tubeFilter.GetOutputPort())
    coneMapper2.SetInputConnection(line.GetOutputPort())

    coneActor1 = vtk.vtkActor()
    coneActor2 = vtk.vtkActor()
    coneActor2.SetPosition(0, 0, -2.5)
    # coneActor1.RotateY(90)
    # coneActor2.RotateY(45)
    # coneActor.RotateWXYZ(90, 0, 0, 1)
    # coneActor.SetScale(0.4)
    coneActor1.SetMapper(coneMapper1)
    coneActor2.SetMapper(coneMapper2)
    coneActor1.GetProperty().SetColor(1, 0, 0)
    coneActor1.GetProperty().SetOpacity(0.5)
    # coneActor2.GetProperty().SetOpacity(0.8)

    xc,yc,zc = 3,6,12
    xCoords = vtk.vtkFloatArray()
    yCoords = vtk.vtkFloatArray()
    zCoords = vtk.vtkFloatArray()
    for i in range(xc):
        xCoords.InsertNextValue(i*i)
    for i in range(yc):
        yCoords.InsertNextValue(i*i)
    for i in range(zc):
        zCoords.InsertNextValue(i*i)
    rgrid = vtk.vtkRectilinearGrid()
    rgrid.SetDimensions(xc, yc, zc)
    rgrid.SetXCoordinates(xCoords)
    rgrid.SetYCoordinates(yCoords)
    rgrid.SetZCoordinates(zCoords)
    plane = vtk.vtkRectilinearGridGeometryFilter()
    plane.SetInputData(rgrid)
    plane.SetExtent(0,xc-1,0,yc-1,0,zc-1)
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputConnection(plane.GetOutputPort())
    # mapper.SetInputData(rgrid)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    ren1 = vtk.vtkRenderer()
    ren1.AddActor(coneActor1)
    ren1.AddActor(coneActor2)
    # ren1.AddActor(actor)
    ren1.SetBackground(0, .4, .4)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(400, 400)
    renWin.Render()

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    iren.Initialize()
    iren.Start()




from transitions import Machine
# 定义一个自己的类
class Matter(object):
    pass
model = Matter()


# 状态定义
states=['solid', 'liquid', 'gas', 'plasma']


# 定义状态转移
# The trigger argument defines the name of the new triggering method
transitions = [
    {'trigger': 'melt', 'source': 'solid', 'dest': 'liquid' },
    {'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas'},
    {'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas'},
    {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'}]


# 初始化
machine = Machine(model=model, states=states, transitions=transitions, initial='solid')


def testSM():
    print(model.state)

    model.melt()

    print(model.state)

    model.evaporate()

    print(model.state)

    print(list(range(0,9,2)))

def testPolyData():
    src = vtk.vtkConeSource()
    src.SetHeight(10)
    src.SetRadius(5)
    src.SetResolution(30)
    src.Update()

    polydata = vtk.vtkPolyData()
    pts = vtk.vtkPoints()
    pts.InsertPoint(0, 0, 0, 0)
    pts.InsertPoint(1, 0, 10, 0)
    pts.InsertPoint(2, 10, 0, 0)
    pts.InsertPoint(3, 0, 20, 20)
    cells = vtk.vtkCellArray()
    cells.InsertNextCell(2, (0, 1))
    cells.InsertNextCell(2, (0, 3))
    cells.InsertNextCell(2, (0, 2))
    cells.InsertNextCell(2, (1, 3))
    cells.InsertNextCell(2, (1, 2))
    cells.InsertNextCell(2, (2, 3))
    polydata.SetPoints(pts)
    polydata.SetLines(cells)

    # mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputData(polydata)
    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)
    
    # actor.GetProperty().SetColor(0,1,0)
    # actor.GetProperty().SetLineWidth(10)
    # actor.GetProperty().SetRenderLinesAsTubes(True)
    # actor.GetProperty().SetVertexVisibility(True)
    # actor.GetProperty().SetRenderPointsAsSpheres(True)
    # actor.GetProperty().SetPointSize(10)

    # mapper1 = vtk.vtkPolyDataMapper()
    # mapper1.SetInputConnection(src.GetOutputPort())
    # actor1 = vtk.vtkActor()
    # actor1.SetMapper(mapper1)
    # actor1.GetProperty().SetOpacity(0.4)

    appendFilter = vtk.vtkAppendPolyData()
    appendFilter.AddInputData(src.GetOutput())
    appendFilter.AddInputData(polydata)
    appendFilter.Update()
    cleanFilter = vtk.vtkCleanPolyData()
    cleanFilter.SetInputConnection(appendFilter.GetOutputPort())
    cleanFilter.Update()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cleanFilter.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(0.4)
    actor.GetProperty().SetLineWidth(10)

    ren1 = vtk.vtkRenderer()
    ren1.AddActor(actor)
    # ren1.AddActor(actor1)
    ren1.SetBackground(0, .4, .4)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(400, 400)
    renWin.Render()

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    iren.Initialize()
    iren.Start()

def testGeo():
    p1 = (2,0,0)
    p2 = (0,1,0)
    print(vtk.vtkLine.DistanceToLine((0,0,0),p1,p2))
    print(vtk.vtkMath.Distance2BetweenPoints(p1, p2))


import vtk
if __name__ == '__main__':
    testGeo()
    testPolyData()

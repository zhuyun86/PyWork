import math
import sys
import os
import csv
import heapq
import time
import copy
import functools

from collections import defaultdict, namedtuple

import vtk
import glob

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

    xc, yc, zc = 3, 6, 12
    xCoords = vtk.vtkFloatArray()
    yCoords = vtk.vtkFloatArray()
    zCoords = vtk.vtkFloatArray()
    for i in range(xc):
        xCoords.InsertNextValue(i * i)
    for i in range(yc):
        yCoords.InsertNextValue(i * i)
    for i in range(zc):
        zCoords.InsertNextValue(i * i)
    rgrid = vtk.vtkRectilinearGrid()
    rgrid.SetDimensions(xc, yc, zc)
    rgrid.SetXCoordinates(xCoords)
    rgrid.SetYCoordinates(yCoords)
    rgrid.SetZCoordinates(zCoords)
    plane = vtk.vtkRectilinearGridGeometryFilter()
    plane.SetInputData(rgrid)
    plane.SetExtent(0, xc - 1, 0, yc - 1, 0, zc - 1)
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
states = ['solid', 'liquid', 'gas', 'plasma']

# 定义状态转移
# The trigger argument defines the name of the new triggering method
transitions = [{
    'trigger': 'melt',
    'source': 'solid',
    'dest': 'liquid'
}, {
    'trigger': 'evaporate',
    'source': 'liquid',
    'dest': 'gas'
}, {
    'trigger': 'sublimate',
    'source': 'solid',
    'dest': 'gas'
}, {
    'trigger': 'ionize',
    'source': 'gas',
    'dest': 'plasma'
}]

# 初始化
machine = Machine(
    model=model, states=states, transitions=transitions, initial='solid')


def testSM():
    print(model.state)

    model.melt()

    print(model.state)

    model.evaporate()

    print(model.state)

    print(list(range(0, 9, 2)))


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
    verts = vtk.vtkCellArray()
    verts.InsertNextCell(1, (0, ))
    verts.InsertNextCell(1, (1, ))
    verts.InsertNextCell(1, (2, ))
    verts.InsertNextCell(1, (3, ))
    polys = vtk.vtkCellArray()
    polys.InsertNextCell(3, (0, 1, 2))
    polys.InsertNextCell(3, (0, 1, 3))
    polys.InsertNextCell(3, (0, 2, 3))
    polys.InsertNextCell(3, (1, 2, 3))
    polydata.SetPoints(pts)
    polydata.SetLines(cells)
    polydata.SetVerts(verts)
    polydata.SetPolys(polys)

    scalars = vtk.vtkIntArray()
    conePointDataPointer = polydata.GetPointData()
    conePolyDataPointer = polydata
    scalars.SetNumberOfTuples(conePolyDataPointer.GetNumberOfPoints())
    scalars.SetNumberOfComponents(1)
    for i in range(conePolyDataPointer.GetNumberOfPoints()):
        scalars.SetTuple1(i, i)
    conePointDataPointer.SetScalars(scalars)

    # pColorTable = vtk.vtkLookupTable()
    # pColorTable.SetNumberOfColors(4)
    # pColorTable.SetTableValue(0, 1.0, 0.0, 0.0, 1.0)
    # pColorTable.SetTableValue(1, 0.0, 1.0, 0.0, 1.0)
    # pColorTable.SetTableValue(2, 1.0, 1.0, 0.0, 1.0)
    # pColorTable.SetTableValue(3, 0.0, 0.0, 1.0, 1.0)
    # pColorTable.Build()
    # mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputData(polydata)
    # mapper.SetScalarRange(0, 3)
    # mapper.SetLookupTable(pColorTable)
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
    # actor.GetProperty().SetOpacity(0.4)
    actor.GetProperty().SetLineWidth(5)
    actor.GetProperty().SetPointSize(10)
    actor.GetProperty().SetRenderLinesAsTubes(True)
    actor.GetProperty().SetRenderPointsAsSpheres(True)

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
    p1 = (2, 0, 0)
    p2 = (0, 1, 0)
    t = vtk.reference(1)
    closest = [0, 0, 0]
    dtl = vtk.vtkLine.DistanceToLine((0, 0, 0), p1, p2, t, closest)
    print(dtl, t, closest)
    print(vtk.vtkMath.Distance2BetweenPoints(p1, p2))

    p = [1, 2, 3]
    project = [0, 0, 0]
    plane = vtk.vtkPlane()
    plane.SetOrigin(0, 0, 0)
    plane.SetNormal(0, 0, 1)
    plane.ProjectPoint(p, project)
    print('distance:', p, project)

    m = vtk.vtkMatrix4x4()
    m.SetElement(0, 0, 1)
    m.SetElement(0, 1, 0)
    m.SetElement(0, 2, 0)
    m.SetElement(0, 3, 0)
    m.SetElement(1, 0, 0)
    m.SetElement(1, 1, 2)
    m.SetElement(1, 2, 0)
    m.SetElement(1, 3, 0)
    m.SetElement(2, 0, 0)
    m.SetElement(2, 1, 0)
    m.SetElement(2, 2, 3)
    m.SetElement(2, 3, 0)
    m.SetElement(3, 0, 0)
    m.SetElement(3, 1, 0)
    m.SetElement(3, 2, 0)
    m.SetElement(3, 3, 4)

    transform = vtk.vtkTransform()
    transform.SetMatrix(m)

    normalProjection = [1.0] * 3
    mNorm = transform.TransformFloatPoint(normalProjection)
    perspectiveTrans = vtk.vtkPerspectiveTransform()
    perspectiveTrans.SetMatrix(m)
    perspectiveProjection = [2] * 3
    mPersp = perspectiveTrans.TransformFloatPoint(perspectiveProjection)
    # m.Identity()
    print('transform:', m.Determinant(), mNorm, mPersp,
          m.MultiplyPoint((1, 1, 1, 1)))


def dec1(t1, t2):
    def dec(f):
        def wrap(*args, **kw):
            print(t1)
            print(type(args), type(kw))
            f(*args, **kw)
            print(t2)
        return wrap
    return dec

@dec1('ac', 123)
def test(txt):
    print(txt)

def testMatirx():
    m3 = vtk.vtkMatrix3x3()
    print(type(m3))
    m31 = vtk.vtkMatrix3x3()
    v3 = [1,0,0,0,2,0,0,0,3]
    v31 = [2,2,2]
    v32 = [2,2,2]
    m3.DeepCopy(v3)
    m3.MultiplyPoint(v31, v32)
    vtk.vtkMatrix3x3.Invert(m3,m31)
    m3.Transpose()
    m3.Adjoint(m3,m31)
    print(m3.Determinant())
    print(m3.IsA('vtkMatrix3x3'), type(m3))

    res = m31.GetData()
    print('m31',res, type(res))
    ls = []
    for i in range(3):
        for j in range(3):
            ls.append(m3.GetElement(i,j))
    print(ls)


import itk
def testITK():
    print(dir(itk.Version))
    print(itk.Version.__doc__)
    print(itk.Version.GetITKVersion(), itk.Version.GetITKSourceVersion(), itk.Version.GetGlobalWarningDisplay() , itk.Version.GetITKMinorVersion())

class Test(object):
    def __init__(self):
        self.age = 18
        self.test()

    name = 'App'
    def test(self):
        return 'test123'

xx = {'x': -10, 'z': -100}
def testEval():
    x = 1
    z = 10
    xx = {'x':-1, 'y':-2}
    print(eval('x+y+z', globals(), xx))
    eval('print(math.pi)')

z = 100
y= 2
x= 11
if __name__ == '__main__':
    # testMatirx()
    testEval()



    # print('glob', glob.glob(r'D:\work\Bat\*.py'))
    # for i in glob.iglob(r'D:\work\Bat\*.py'):
    #     print(i)
    # testGeo()
    # testPolyData()

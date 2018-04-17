import bpy
import bmesh
from mathutils import Vector
from os import path, remove
import sys


HELP_MESSAGE = 'Usage: blender -b -P BlenderSup.py -- [OPTION] ...\n\
Mandatory arguments are:\n\
\t-t, --text [VALUE]\t\tText to generate from\n\
Optionary arguments are:\n\
\t-e, --extrusion [VALUE]\t\tHeight of text\n\
\t-b, --base [VALUE]\t\tHeight of base\n\
\t-p, --padding [VALUE]\t\tExtra padding around text\n\
\t-l, --location [VALUE]\t\tPath to save to\n\
BlenderSup allows you to generate a TextObj.obj\
file from the given arguments'


class Blender(object):
    """A blender static class

    Unifies and simplifies common simple tasks required for the script to work

    """

    @staticmethod
    def removeStartingElements():
        """Removes the starting elements in the blender scene"""

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    @staticmethod
    def deselectAll():
        """Deselects all objects"""

        for obj in bpy.data.objects:
            obj.select = False

    @staticmethod
    def join(objectName1, objectName2):
        """Joins 2 objects

        Args:
            [objectName1] (str): Object name to join to
            [objectName2] (str): Object name to join to [objectName1]

        """

        bpy.data.objects[objectName1].select = True
        bpy.data.objects[objectName2].select = True
        bpy.context.scene.objects.active = bpy.data.objects[objectName1]
        bpy.ops.object.join()
        Blender.deselectAll()


class BlenderText(object):
    """A Blender text textcurve/mesh object

    Allows easy creation of blender text objects

    """

    def __init__(self, text=None, typeT='mesh', meshName="WordMesh"):
        """The BlenderText initializer

        Args:
            [text] (str): Text to write
            [typeT] (str): ['mesh'/'curve'/None] What should be created out of
                the text

        """

        self.text = text

        if typeT is 'mesh':
            self.toCurve()
            self.toMesh(meshName)
        elif typeT is 'curve':
            self.toCurve()

    @property
    def text(self):
        """The text to write"""

        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    @property
    def dimensions(self):
        """Dimensions of the mesh"""
        if self.textMesh:
            return self.textMesh.dimensions
        elif self.textCurve:
            return self.textCurve.dimensions
        else:
            raise Exception('Object not yet created')

    @property
    def location(self):
        """Location of the mesh"""

        if self.textMesh:
            return self.textMesh.location
        elif self.textCurve:
            return self.textCurve.location
        else:
            raise Exception('Object not yet created')

    @location.setter
    def location(self, loc):

        self.textMesh.location[0] = loc[0]
        self.textMesh.location[1] = loc[1]
        self.textMesh.location[2] = loc[2]

    def centerOrigin(self):
        """Centers the origin to the geometry"""

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

    def toCurve(self):
        """Creates a textCurve out of self.text"""

        if not self.text:
            raise TypeError('None value given')
        bpy.ops.object.text_add()
        self.textCurve = bpy.context.object
        self.textCurve.data.body = self.text

        self.centerOrigin()

    def toMesh(self, meshName='WordMesh'):
        """Creates a mesh out of self.textCurve and centers the origin to the geometry

        Note:
            Will raise TypeError if self.text is not set

        """

        if not self.text:
            raise TypeError('None value given')
        if not self.textCurve:
            self.toCurve()

        context = bpy.context
        scene = context.scene

        textMesh = self.textCurve.to_mesh(scene, False, 'PREVIEW')
        self.textMesh = bpy.data.objects.new(meshName, textMesh)
        scene.objects.link(self.textMesh)
        self.textMesh.matrix_world = self.textCurve.matrix_world
        scene.objects.unlink(self.textCurve)

    def extrude(self, amount):
        """Extrudes the self.textMesh

        Args:
            amount (num): Amount to extrude
        """

        me = self.textMesh.data
        bm = bmesh.new()
        bm.from_mesh(me)

        faces = bm.faces[:]

        for face in faces:
            r = bmesh.ops.extrude_discrete_faces(bm, faces=[face])
            bmesh.ops.translate(bm, vec=Vector((0, 0, amount)),
                                verts=r['faces'][0].verts)

        bm.to_mesh(me)
        me.update()


class BlenderCube(object):
    """A Blender text textcurve/mesh object

    Allows easy creation of blender cubes

    """

    def __init__(self, name='Cube',
                 x=0, y=0, z=0, width=0, length=0, height=0):
        """The BlenderCube initializer

        Args:
            [name] (str): Name of the object
            [x] (num): Center location on the X axis
            [y] (num): Center location on the Y axis
            [z] (num): Center location on the Z axis
            [width] (num): X axis dimension
            [length] (num): Y axis dimension
            [height] (num): Z axis dimension
        """

        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        bpy.context.object.name = name
        bpy.context.object.dimensions = width, length, height
        Blender.deselectAll()


argv = sys.argv
argv = argv[argv.index('--') + 1:]

R_TEXT_TO_SET = ""
R_EXTRUSION_VALUE = 0
R_BASE_HEIGHT = 0
R_PADDING = 0
R_LOCATION = path.join(path.expanduser('~'), 'Desktop', 'TextObject.obj')


def createMesh():
    Blender.removeStartingElements()

    text = BlenderText(R_TEXT_TO_SET, 'mesh', 'TextMesh')
    text.location = 0, 0, 0
    text.extrude(R_EXTRUSION_VALUE)

    BlenderCube('Base', 0, 0, 0 - R_BASE_HEIGHT / 2,
                text.dimensions[0] + R_PADDING * 2,
                text.dimensions[1] + R_PADDING * 2,
                R_BASE_HEIGHT)

    Blender.join('TextMesh', 'Base')

    bpy.ops.export_scene.obj(filepath=R_LOCATION)
    remove(path.join(path.expanduser('~'), 'Desktop', 'TextObject.mtl'))


if '--help' in argv:
    print(HELP_MESSAGE)
else:
    if '-t' in argv:
        R_TEXT_TO_SET = argv[argv.index('-t') + 1]
    elif '--text' in argv:
        R_TEXT_TO_SET = argv[argv.index('--text') + 1]
    if '-e' in argv:
        R_EXTRUSION_VALUE = float(argv[argv.index('-e') + 1])
    elif '--extrusion' in argv:
        R_EXTRUSION_VALUE = float(argv[argv.index('--extrusion') + 1])
    if '-b' in argv:
        R_BASE_HEIGHT = float(argv[argv.index('-b') + 1])
    elif '--base' in argv:
        R_BASE_HEIGHT = float(argv[argv.index('--base') + 1])
    if '-p' in argv:
        R_PADDING = float(argv[argv.index('-p') + 1])
    elif '--padding' in argv:
        R_PADDING = float(argv[argv.index('--padding') + 1])
    if '-l' in argv:
        R_LOCATION = argv[argv.index('-l') + 1]
    elif '--location' in argv:
        R_LOCATION = argv[argv.index('--location') + 1]

    createMesh()

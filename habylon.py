import json
import os, sys

import collections

class BObject(dict):
    """ Dictionary like stucture, but very peaky about data types and schema.
        You can't add anything not present in schema. This is good, as variations
        are root of all evil in not homogenious software like Python modules which
        are meant to be used in other softwares.
    """
    def __init__(self, schema, obj):
        super(BObject, self).__init__(schema[obj])
        self.type = obj
    def __setitem__(self, key, value):
        """Custom item setter. Main reason fo it is type checking.
        """
        assert key in self, "Key %s not defined in schema" % key
        if isinstance(value, type(self[key])):
            super(BObject, self).__setitem__(key, value)
        else:
            raise TypeError("Wrong type of %s: %s" % (key, value))

    def __repr__(self):
        from json import dumps
        return dumps(self, indent=1)

class Scene(BObject):
    """Ideally this should be the only specialized class derived from BObject. 
       Scene takes care of creation and adding object to the Babylon scene.
    """
    def __init__(self, *args):
        self.schema = self.load_schema("./schema")
        super(Scene, self).__init__(self.schema, "scene")

    def load_schema(self, path, schema={}):
        """Load *.json files defining Babylon objects.
        """
        from glob import glob
        location = os.path.join(path, "*.json")
        files    = glob(location)
 
        for file in files:
            with open(file) as file_object:
                obj  = json.load(file_object)
                name = os.path.split(file)[1]
                name = os.path.splitext(name)[0]
                schema[name] = obj
        return schema

    def add(self, child):
        """Babylon file has pretty much hardcoded structure...
        """
        if self.type == "scene":
            if child.type == 'box':
                self['geometries']['boxes'].append(child)
            elif child.type == 'sphere':
                self['geometries']['spheres'].append(child)
            elif child.type == 'vertexData':
                self['geometries']['vertexData'].append(child)
            elif child.type == "mesh":
                self['meshes'].append(child)
            elif child.type == 'light':
                self['lights'].append(child)
            elif child.type == "material":
                self['materials'].append(child)
            return True
        return

    def new(self, type):
        """Creats a new class of specified type from schema definition.
        """
        if type in self.schema:
            return BObject(self.schema, type)


def main():
    """Basic test of our tiny module."""

    scene  = Scene()
    box    = scene.new('box')
    sphere = scene.new('sphere')

    scene.add(box)
    scene.add(sphere)

    print scene

if __name__ == "__main__": main()

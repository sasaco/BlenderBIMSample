#任意のオブジェクトを「Edit Mode」で1つ以上の面を選択。
#スクリプトを実行したら、毛が生成される。

import bpy
import random


class MakeFur():
  name = "Fur Polygon"

  def __init__(self):
    self.verts = []
    self.faces = []
    self.index = 0
    if self.name in bpy.data.meshes:
      bpy.data.meshes.remove(bpy.data.meshes[self.name])

  def make(self,num,min,max,size):
    o = bpy.context.active_object
    mesh = bpy.data.meshes[o.data.name]
    for f in range(len(mesh.polygons)):
      poly = mesh.polygons[f]
      if poly.select == False:
        continue
      vi = poly.vertices
      if len(vi) == 3:
        v0 = mesh.vertices[vi[0]].co
        v1 = mesh.vertices[vi[1]].co
        v2 = mesh.vertices[vi[2]].co
        for i in range(num):
          n = poly.normal*random.uniform(min,max)
          self.make_polygon(v0,v1,v2,n,size)
      elif len(vi) == 4:
        v0 = mesh.vertices[vi[0]].co
        v1 = mesh.vertices[vi[1]].co
        v2 = mesh.vertices[vi[2]].co
        v3 = mesh.vertices[vi[3]].co
        for i in range(num):
          n = poly.normal*random.uniform(min,max)
          self.make_polygon(v0,v1,v3,n,size)
          self.make_polygon(v2,v3,v1,n,size)
    mesh = bpy.data.meshes.new(self.name)
    object = bpy.data.objects.new(self.name, mesh)
    bpy.context.collection.objects.link(object)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    mesh.from_pydata(self.verts,[],self.faces)
    mesh.update()
  
  def random_vertex(self,v0,v1,v2):
    r0 = random.random()
    r1 = (1-r0)*random.random()
    v = (v1-v0)*r0 + (v2-v0)*r1 + v0
    return v

  def make_polygon(self,p0,p1,p2,normal,size):
    center = self.random_vertex(p0,p1,p2)
    v0 = center + (p0-center)*size
    v1 = center + (p1-center)*size
    v2 = center + (p2-center)*size
    n = center + normal
    self.verts.append(n)
    self.verts.append(v0)
    self.verts.append(v1)
    self.verts.append(v2)
    self.faces.append((self.index,self.index+1,self.index+2))
    self.faces.append((self.index,self.index+2,self.index+3))
    self.faces.append((self.index,self.index+3,self.index+1))
    self.index += 4

if __name__ == "__main__":
  fur = MakeFur()
  fur.make(5,0.5,1.0,0.1)

#スクリプトを実行したら、アニメーションタブをクリック
#「▶」ボタンをクリックしてアニメーションを再生すればランダムに動くギャグ製造機

import bpy
import math
import random

objs = []
rot_range = (10,45,90,90,90,90,90,90,90,90)

def make_cube(parent,loc,scale,pivot):
  bpy.ops.mesh.primitive_cube_add(location=loc,scale=scale)
  obj = bpy.context.active_object
  x = obj.location.x + pivot[0]
  y = obj.location.y + pivot[1]
  z = obj.location.z + pivot[2]
  bpy.context.scene.cursor.location=(x,y,z)
  bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
  if parent is not None:
    obj.parent = parent
  return obj

def set_animation(obj,frame,rotation):
  bpy.context.scene.frame_set(frame)
  obj.rotation_euler = rotation
  obj.keyframe_insert(data_path="rotation_euler")

for m in bpy.data.meshes:
  bpy.data.meshes.remove(m)

loc = (0,0,0),(0,0,5),(2.5,0,3.5),(3,0,0),(-2.5,0,3.5),(-3,0,0),\
      (0.8,0,-1),(0,0,-3),(-0.8,0,-1),(0,0,-3)
scale = (3,1.5,4),(2,2,2),(2,1,1),(2,1,1),(2,1,1),(2,1,1),\
        (1.25,1.25,2),(1.25,1.25,2),(1.25,1.25,2),(1.25,1.25,2)
pivot = (0,0,-2),(0,0,-1),(-1,0,0),(-1,0,0),(1,0,0),(1,0,0),\
        (0,0,1),(0,0,1),(0,0,1),(0,0,1)
parent = None,0,0,2,0,4,0,6,0,8
length = len(loc)
for i in range(length):
  p = objs[parent[i]] if parent[i] is not None else None
  objs.append(make_cube(p,loc[i],scale[i],pivot[i]))

for o in range(len(objs)):
  obj = objs[o]
  obj.animation_data_clear()
  obj.rotation_mode = "XYZ"
  set_animation(obj,0,(0,0,0))
  for frame in range(25,250,25):
    rot = rot_range[o]
    x = math.radians(random.uniform(-rot,rot))
    y = math.radians(random.uniform(-rot,rot))
    z = math.radians(random.uniform(-rot,rot))
    set_animation(obj,frame,(x,y,z))
  set_animation(obj,250,(0,0,0))

bpy.context.scene.frame_set(0)

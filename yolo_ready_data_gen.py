import bpy
import bpy_extras
from bpy_extras.object_utils import world_to_camera_view
import random
import math
import os
import mathutils

OUTPUT_PATH = "E:/synthetic-data-generation/Helmet_Dataset/"
TOTAL_IMAGES = 10

scene = bpy.context.scene

worker_obj = bpy.data.objects["WORKER"]
helmet_obj = bpy.data.objects["HELMET"]
camera_obj = bpy.data.objects["Camera"]
focus_target = bpy.data.objects["Focus_Target"]

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

def get_bounding_box(obj, camera):
    bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
    min_x, max_x = 1.0, 0.0
    min_y, max_y = 1.0, 0.0
    valid_points = False
    for corner in bbox_corners:
        co_2d = world_to_camera_view(scene, camera, corner)
        if co_2d.z > 0:
            min_x = min(min_x, co_2d.x)
            max_x = max(max_x, co_2d.x)
            min_y = min(min_y, co_2d.y)
            max_y = max(max_y, co_2d.y)
            valid_points = True
    if not valid_points:
        return None
    width = max_x - min_x
    height = max_y - min_y
    center_x = min_x + (width / 2)
    center_y = 1.0 - (min_y + (height / 2))
    center_x = max(0.0, min(1.0, center_x))
    center_y = max(0.0, min(1.0, center_y))
    width = max(0.0, min(1.0, width))
    height = max(0.0, min(1.0, height))
    return [0, center_x, center_y, width, height]

def randomize_camera():
    radius = random.uniform(4.0, 7.0)
    angle = random.uniform(0.2 * math.pi)
    height_offset = random.uniform(0.5, 2.5)
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    camera_obj.location.x = focus_target.location.x + x
    camera_obj.location.y = focus_target.location.y + y
    camera_obj.location.z = focus_target.location.z + height_offset

def toggle_helmet():
    is_safe = random.choice([True, False])
    helmet_obj.hide_render = not is_safe
    helmet_obj.hide_viewport = not is_safe
    return is_safe

for i in range(TOTAL_IMAGES):
    randomize_camera()
    has_helmet = toggle_helmet()
    bpy.context.view_layer.update()
    label_line = "" 
    label_suffix = "unsafe"

    if has_helmet:
        label_suffix = "safe"
        yolo_data = get_bounding_box(helmet_obj, camera_obj)
        if yolo_data:
            label_line = f"{yolo_data[0]} {yolo_data[1]:.6f} {yolo_data[2]:.6f} {yolo_data[3]:.6f} {yolo_data[4]:.6f}"
    filename_base = f"train_{i:04d}_{label_suffix}"
    scene.render.filepath = os.path.join(OUTPUT_PATH, filename_base + ".jpg")
    bpy.ops.render.render(write_still = True)
    with open(os.path.join(OUTPUT_PATH, filename_base + ".txt"), "w") as f:
        f.write(label_line)
    print(f"Generated {filename_base}")
print("Batch complete!")
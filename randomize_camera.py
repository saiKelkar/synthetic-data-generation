import bpy
import random
import math
import os

OUTPUT_PATH = "E:/synthetic-data-generation/Helmet_Dataset/"
TOTAL_IMAGES = 10

worker_obj = bpy.data.objects["WORKER"]
helmet_obj = bpy.data.objects["HELMET"]
camera_obj = bpy.data.objects["Camera"]
focus_target = bpy.data.objects["Focus_Target"]

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

def randomize_camera():
    radius = random.uniform(4.0, 7.0)
    angle = random.uniform(0, 2 * math.pi)
    height = random.uniform(0.5, 2.5)
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    camera_obj.location.x = focus_target.location.x + x
    camera_obj.location.y = focus_target.location.y + y
    camera_obj.location.z = focus_target.location.z + height

def toggle_helmet():
    is_safe = random.choice([True, False])
    helmet_obj.hide_render = not is_safe
    helmet_obj.hide_viewport = not is_safe
    return is_safe

for i in range(TOTAL_IMAGES):
    randomize_camera()
    has_helmet = toggle_helmet()
    label = "safe" if has_helmet else "unsafe"
    filename = f"render_{i:04d}_{label}.jpg"
    bpy.context.scene.render.filepath = os.path.join(OUTPUT_PATH, filename)
    bpy.ops.render.render(write_still = True)
    print(f"Generated {filename}")

print("Batch complete!")
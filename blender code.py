import bpy
import math
import os

texture_dir = r"C:\Users\Aqua Minato\Pictures\solar system textures"
space_texture = os.path.join(texture_dir, "SPACE.jpg")

planet_textures = {
    "Sun": os.path.join(texture_dir, "SUN.jpg"),
    "Mercury": os.path.join(texture_dir, "MERCURY.jpg"),
    "Venus": os.path.join(texture_dir, "VENUS.jpg"),
    "Earth": os.path.join(texture_dir, "EARTH.jpg"),
    "Moon": os.path.join(texture_dir, "MOON.jpg"),
    "Mars": os.path.join(texture_dir, "MARS.jpg"),
    "Jupiter": os.path.join(texture_dir, "JUPITER.jpg"),
    "Saturn": os.path.join(texture_dir, "SATURN.jpg"),
    "Uranus": os.path.join(texture_dir, "URANUS.jpg"),
    "Neptune": os.path.join(texture_dir, "NEPTUNE.jpg"),
    "SaturnRings": os.path.join(texture_dir, "SATURN RING.png"),
}

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

world = bpy.context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
env_node = nodes.new(type='ShaderNodeTexEnvironment')
env_node.image = bpy.data.images.load(space_texture)
bg_node = nodes['Background']
world.node_tree.links.new(env_node.outputs['Color'], bg_node.inputs['Color'])

def create_planet(name, radius, location, texture_path):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    planet = bpy.context.object
    planet.name = name

    mat = bpy.data.materials.new(name + "_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(texture_path)
    mat.node_tree.links.new(bsdf.inputs['Base Color'], tex.outputs['Color'])
    planet.data.materials.append(mat)
    return planet

def create_orbit(radius):
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius)
    orbit = bpy.context.object
    orbit.data.resolution_u = 64
    orbit.data.fill_mode = 'HALF'
    orbit.data.bevel_depth = 0.005
    orbit.data.bevel_resolution = 3
    return orbit

create_planet("Sun", 2.0, (0, 0, 0), planet_textures["Sun"])

planet_data = [
    ("Mercury", 0.3, 4),
    ("Venus", 0.5, 6),
    ("Earth", 0.5, 8),
    ("Moon", 0.13, 8.6),
    ("Mars", 0.4, 10),
    ("Jupiter", 1.1, 13),
    ("Saturn", 1.0, 16),
    ("Uranus", 0.7, 19),
    ("Neptune", 0.7, 22),
]

orbital_periods = {
    "Mercury": 2,     
    "Venus": 5,        
    "Earth": 8,        
    "Moon": 0.7,      
    "Mars": 15,       
    "Jupiter": 95,    
    "Saturn": 236,     
    "Uranus": 673,     
    "Neptune": 1320  
}

for name, size, orbit_radius in planet_data:
    loc = (orbit_radius, 0, 0)
    tex = planet_textures[name]
    planet = create_planet(name, size, loc, tex)
    orbit = create_orbit(orbit_radius)
    
    if name == "Moon":
        bpy.ops.object.empty_add(location=(8, 0, 0))
        moon_empty = bpy.context.object
        moon_empty.name = "Moon_Earth_Orbit_Center"
        
        planet.location = (0.6, 0, 0)
        
        moon_orbit = create_orbit(0.6)
        moon_orbit.parent = moon_empty
        
        planet.parent = moon_empty
        
        earth_empty = bpy.data.objects["Earth_Orbit_Center"]
        moon_empty.parent = earth_empty
        
        period = orbital_periods["Moon"]
        moon_empty.rotation_euler = (0, 0, 0)
        moon_empty.keyframe_insert(data_path="rotation_euler", frame=1)
        
        moon_empty.rotation_euler = (0, 0, 2 * math.pi)
        moon_empty.keyframe_insert(data_path="rotation_euler", frame=period * 24)
        
        for fcurve in moon_empty.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'
                
    elif name in orbital_periods:
        bpy.ops.object.empty_add(location=(0, 0, 0))
        empty = bpy.context.object
        empty.name = f"{name}_Orbit_Center"
        
        planet.parent = empty
        
        period = orbital_periods[name]
        empty.rotation_euler = (0, 0, 0)
        empty.keyframe_insert(data_path="rotation_euler", frame=1)
        
        empty.rotation_euler = (0, 0, 2 * math.pi)
        empty.keyframe_insert(data_path="rotation_euler", frame=period * 24)
        
        for fcurve in empty.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

bpy.context.scene.frame_end = 1320 * 24
bpy.context.scene.render.fps = 24

bpy.context.scene.use_preview_range = False
bpy.context.scene.frame_start = 1

for action in bpy.data.actions:
    fc = action.fcurves
    for curve in fc:
        curve.modifiers.new('CYCLES')

bpy.context.scene.render.use_lock_interface = True
bpy.context.scene.sync_mode = 'AUDIO_SYNC'

bpy.ops.mesh.primitive_torus_add(location=(16, 0, 0), major_radius=1.2, minor_radius=0.05)
rings = bpy.context.object
rings.name = "Saturn_Rings"

mat = bpy.data.materials.new("SaturnRing_Mat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
tex.image = bpy.data.images.load(planet_textures["SaturnRings"])
mat.node_tree.links.new(bsdf.inputs['Base Color'], tex.outputs['Color'])
rings.data.materials.append(mat)

saturn_empty = bpy.data.objects["Saturn_Orbit_Center"]
rings.parent = saturn_empty

bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
bpy.ops.object.camera_add(location=(0, -40, 20), rotation=(math.radians(70), 0, 0))
bpy.context.scene.camera = bpy.context.object

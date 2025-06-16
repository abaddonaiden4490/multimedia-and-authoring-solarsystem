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

# Planet information database
planet_info = {
    "Sun": {
        "description": "The Sun is a massive ball of hot plasma that provides light and heat to our solar system.",
        "orbital_period_days": 365.25,  # Earth reference
        "human_age_factor": 1.0
    },
    "Mercury": {
        "description": "Mercury is the smallest planet and closest to the Sun with extreme temperature variations.",
        "orbital_period_days": 88,
        "human_age_factor": 365.25 / 88
    },
    "Venus": {
        "description": "Venus is the hottest planet with a thick, toxic atmosphere and surface temperatures of 900°F.",
        "orbital_period_days": 225,
        "human_age_factor": 365.25 / 225
    },
    "Earth": {
        "description": "Earth is our home planet, the only known world with life and liquid water on its surface.",
        "orbital_period_days": 365.25,
        "human_age_factor": 1.0
    },
    "Moon": {
        "description": "The Moon is Earth's natural satellite, influencing our planet's tides and stabilizing its rotation.",
        "orbital_period_days": 27.3,
        "human_age_factor": 365.25 / 27.3
    },
    "Mars": {
        "description": "Mars is the Red Planet with polar ice caps, ancient riverbeds, and the largest volcano in the solar system.",
        "orbital_period_days": 687,
        "human_age_factor": 365.25 / 687
    },
    "Jupiter": {
        "description": "Jupiter is the largest planet, a gas giant with a Great Red Spot storm and over 80 moons.",
        "orbital_period_days": 4333,
        "human_age_factor": 365.25 / 4333
    },
    "Saturn": {
        "description": "Saturn is famous for its spectacular ring system and is the least dense planet in our solar system.",
        "orbital_period_days": 10759,
        "human_age_factor": 365.25 / 10759
    },
    "Uranus": {
        "description": "Uranus is an ice giant that rotates on its side and has a faint ring system.",
        "orbital_period_days": 30687,
        "human_age_factor": 365.25 / 30687
    },
    "Neptune": {
        "description": "Neptune is the windiest planet with speeds up to 1,200 mph and a deep blue color from methane.",
        "orbital_period_days": 60190,
        "human_age_factor": 365.25 / 60190
    }
}

def calculate_human_age(earth_age, planet_name):
    """Calculate what your age would be on another planet"""
    if planet_name in planet_info:
        factor = planet_info[planet_name]["human_age_factor"]
        return earth_age * factor
    return earth_age

def create_info_text(planet_name, location, earth_age=20):
    """Create empty with custom properties for planet information (SketchUp-style descriptive text)"""
    if planet_name not in planet_info:
        return None
    
    info = planet_info[planet_name]
    planet_age = calculate_human_age(earth_age, planet_name)
    
    # Create empty object to hold the information
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(location[0], location[1], location[2] + 1))
    info_empty = bpy.context.object
    info_empty.name = f"{planet_name}_Info_Marker"
    info_empty.empty_display_size = 0.1
    
    # Add custom properties that will appear in the properties panel
    info_empty["Planet_Name"] = planet_name
    info_empty["Description"] = info['description']
    info_empty["Orbital_Period_Days"] = info['orbital_period_days']
    info_empty["Your_Age_Here"] = f"{planet_age:.1f} years"
    info_empty["Earth_Age_Reference"] = f"{earth_age} years"
    
    # Set custom property UI settings for better display
    info_empty.id_properties_ui("Planet_Name").update(description="Name of this celestial body")
    info_empty.id_properties_ui("Description").update(description="Scientific description and key facts")
    info_empty.id_properties_ui("Orbital_Period_Days").update(description="How many Earth days in one year here")
    info_empty.id_properties_ui("Your_Age_Here").update(description="Your age if you lived on this planet")
    info_empty.id_properties_ui("Earth_Age_Reference").update(description="Reference age on Earth")
    
    return info_empty

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
    
    # Create info text for this planet
    create_info_text(name, location)
    
    return planet

def create_orbit(radius):
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius)
    orbit = bpy.context.object
    orbit.data.resolution_u = 64
    orbit.data.fill_mode = 'HALF'
    orbit.data.bevel_depth = 0.005
    orbit.data.bevel_resolution = 3
    return orbit

# Set up world background with space texture
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world

world.use_nodes = True
world_nodes = world.node_tree.nodes
world_links = world.node_tree.links

# Clear existing nodes
world_nodes.clear()

# Create new nodes
background = world_nodes.new('ShaderNodeBackground')
environment = world_nodes.new('ShaderNodeTexEnvironment')
mapping = world_nodes.new('ShaderNodeMapping')
texcoord = world_nodes.new('ShaderNodeTexCoord')
output = world_nodes.new('ShaderNodeOutputWorld')

# Load space texture
environment.image = bpy.data.images.load(space_texture)

# Connect nodes
world_links.new(texcoord.outputs['Generated'], mapping.inputs['Vector'])
world_links.new(mapping.outputs['Vector'], environment.inputs['Vector'])
world_links.new(environment.outputs['Color'], background.inputs['Color'])
world_links.new(background.outputs['Background'], output.inputs['Surface'])

# Position nodes for better organization
output.location = (300, 300)
background.location = (100, 300)
environment.location = (-200, 300)
mapping.location = (-400, 300)
texcoord.location = (-600, 300)

# Create the Sun
sun = create_planet("Sun", 2.0, (0, 0, 0), planet_textures["Sun"])

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
    "Mercury": 1,     
    "Venus": 2,        
    "Earth": 3,        
    "Moon": 1,      
    "Mars": 4,       
    "Jupiter": 6,    
    "Saturn": 8,     
    "Uranus": 15,     
    "Neptune": 22  
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
        
        # Parent Moon's info marker to follow the moon
        moon_info = bpy.data.objects.get("Moon_Info_Marker")
        if moon_info:
            moon_info.parent = moon_empty
            moon_info.location = (0.6, 0, 1)
        
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
        
        # Parent info marker to follow the planet
        info_marker = bpy.data.objects.get(f"{name}_Info_Marker")
        if info_marker:
            info_marker.parent = empty
        
        period = orbital_periods[name]
        empty.rotation_euler = (0, 0, 0)
        empty.keyframe_insert(data_path="rotation_euler", frame=1)
        
        empty.rotation_euler = (0, 0, 2 * math.pi)
        empty.keyframe_insert(data_path="rotation_euler", frame=period * 24)
        
        for fcurve in empty.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

# Set animation settings
bpy.context.scene.frame_end = 1320 * 24
bpy.context.scene.render.fps = 24
bpy.context.scene.use_preview_range = False
bpy.context.scene.frame_start = 1

# Add cycle modifiers to all actions for infinite rotation
for action in bpy.data.actions:
    fc = action.fcurves
    for curve in fc:
        try:
            modifier = curve.modifiers.new('CYCLES')
            if modifier:
                modifier.mode_after = 'REPEAT'
        except:
            # If CYCLES doesn't work, try REPEAT
            try:
                modifier = curve.modifiers.new('REPEAT')
                if modifier:
                    modifier.mode_after = 'REPEAT'
            except:
                print(f"Could not add cycle modifier to curve: {curve.data_path}")
                continue

bpy.context.scene.render.use_lock_interface = True
bpy.context.scene.sync_mode = 'AUDIO_SYNC'

# Create Saturn's rings
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

# Add lighting and camera - positioned for top-down view
bpy.ops.object.camera_add(location=(0, 0, 120), rotation=(0, 0, 0))
bpy.context.scene.camera = bpy.context.object

print("Solar System created successfully!")
print("Key improvements:")
print("- Information system with planet details")
print("- Smooth orbital animations")
print("- Realistic textures applied")
print("\nAll planet information markers will orbit with their planets.")
print("Age calculations based on 20-year-old Earth human!")
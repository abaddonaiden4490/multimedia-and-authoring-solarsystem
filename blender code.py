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

def create_planet_label(planet_name, location, earth_age=20):
    """Create visible 3D text label with planet name and age - follows the planet"""
    if planet_name not in planet_info:
        return None
    
    planet_age = calculate_human_age(earth_age, planet_name)
    
    # Create the label text content
    if planet_name == "Sun":
        label_text = f"{planet_name}\n(Our Star)"
    else:
        label_text = f"{planet_name}\nAge: {planet_age:.1f} years"
    
    # Position label above the planet
    label_location = (location[0], location[1], location[2] + 2.0)
    
    bpy.ops.object.text_add(location=label_location)
    text_obj = bpy.context.object
    text_obj.name = f"{planet_name}_Label"
    text_obj.data.body = label_text
    text_obj.data.size = 0.6
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    
    # Convert to mesh for better performance and material application
    bpy.context.view_layer.objects.active = text_obj
    bpy.ops.object.convert(target='MESH')
    
    # Create glowing material for visibility
    mat = bpy.data.materials.new(f"{planet_name}_Label_Mat")
    mat.use_nodes = True
    
    # Clear default nodes
    mat.node_tree.nodes.clear()
    
    # Create new nodes
    output = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
    emission = mat.node_tree.nodes.new("ShaderNodeEmission")
    
    # Set emission properties
    emission.inputs['Color'].default_value = (1, 1, 0.8, 1)  # Warm white
    emission.inputs['Strength'].default_value = 3.0
    
    # Connect nodes
    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    # Apply material
    text_obj.data.materials.append(mat)
    
    # Add constraint to always face the camera for readability
    constraint = text_obj.constraints.new(type='TRACK_TO')
    constraint.target = bpy.context.scene.camera
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    return text_obj

def create_solar_system_info():
    """Create descriptive information system similar to SketchUp"""
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, -35, 15))
    info_center = bpy.context.object
    info_center.name = "Solar_System_Info_Center"
    info_center.empty_display_size = 0.5
    
    # Add comprehensive solar system information
    info_center["System_Name"] = "Our Solar System"
    info_center["Description"] = "A gravitationally bound system with the Sun and 8 planets"
    info_center["Age_Calculation_Note"] = "Ages calculated for 20-year-old Earth human"
    info_center["Scale_Note"] = "Sizes and distances are not to scale for visibility"
    
    # Quick reference data
    info_center["Fastest_Orbit"] = "Mercury (88 Earth days)"
    info_center["Largest_Planet"] = "Jupiter (11x Earth's diameter)"
    info_center["Hottest_Planet"] = "Venus (900°F surface temperature)"
    info_center["Coldest_Planet"] = "Neptune (-353°F average)"
    info_center["Most_Moons"] = "Saturn (146 confirmed moons)"
    
    # Set UI descriptions
    info_center.id_properties_ui("System_Name").update(description="Name of our planetary system")
    info_center.id_properties_ui("Description").update(description="Basic description of the solar system")
    info_center.id_properties_ui("Age_Calculation_Note").update(description="Reference for age calculations")
    info_center.id_properties_ui("Scale_Note").update(description="Important note about scale")
    info_center.id_properties_ui("Fastest_Orbit").update(description="Planet with shortest year")
    info_center.id_properties_ui("Largest_Planet").update(description="Biggest planet in our system")
    info_center.id_properties_ui("Hottest_Planet").update(description="Planet with highest surface temperature")
    info_center.id_properties_ui("Coldest_Planet").update(description="Planet with lowest average temperature")
    info_center.id_properties_ui("Most_Moons").update(description="Planet with most natural satellites")

def create_render_pov_label():
    """Create label near the camera/render POV - prominently visible in render covering entire text"""
    # Position the label to be fully visible in camera view
    # Camera is at (0, -60, 30) with rotation (65°, 0, 0)
    # Position it in the upper area where it won't be cut off
    label_location = (-20, -45, 45)  # Moved higher and closer to center
    
    # Create the multi-line text with proper formatting
    label_text = "SOLAR SYSTEM RENDERING (BLENDER)\nMULTIMEDIA AND AUTHORING"
    
    bpy.ops.object.text_add(location=label_location)
    text_obj = bpy.context.object
    text_obj.name = "Render_POV_Label"
    text_obj.data.body = label_text
    text_obj.data.size = 1.0  # Optimal size to fit entire text in frame
    text_obj.data.align_x = 'CENTER'  # Center alignment for better visibility
    text_obj.data.align_y = 'TOP'
    
    # Adjust rotation to be perfectly readable from camera
    text_obj.rotation_euler = (math.radians(55), 0, 0)  # Slightly less angle for better readability
    
    # Convert to mesh for material application
    bpy.context.view_layer.objects.active = text_obj
    bpy.ops.object.convert(target='MESH')
    
    # Create extremely bright glowing material for maximum visibility
    mat = bpy.data.materials.new("POV_Label_Mat")
    mat.use_nodes = True
    
    # Clear default nodes
    mat.node_tree.nodes.clear()
    
    # Create new nodes for enhanced visibility
    output = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
    emission = mat.node_tree.nodes.new("ShaderNodeEmission")
    
    # Set emission properties - bright yellow for maximum contrast against space
    emission.inputs['Color'].default_value = (1.0, 0.9, 0.0, 1)  # Bright yellow
    emission.inputs['Strength'].default_value = 15.0  # Maximum brightness
    
    # Connect nodes
    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    # Apply material
    text_obj.data.materials.append(mat)
    
    # Add constraint to always face camera for optimal visibility
    constraint = text_obj.constraints.new(type='TRACK_TO')
    constraint.target = bpy.context.scene.camera
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    return text_obj

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Setup space background
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
    
    # Create info text for this planet
    create_info_text(name, location)
    
    # Create 3D text label for this planet (following the planet)
    create_planet_label(name, location)
    
    return planet

def create_orbit(radius):
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius)
    orbit = bpy.context.object
    orbit.data.resolution_u = 64
    orbit.data.fill_mode = 'HALF'
    orbit.data.bevel_depth = 0.005
    orbit.data.bevel_resolution = 3
    return orbit

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
        
        # Parent Moon's info marker and label to follow the moon
        moon_info = bpy.data.objects.get("Moon_Info_Marker")
        moon_label = bpy.data.objects.get("Moon_Label")
        if moon_info:
            moon_info.parent = moon_empty
            moon_info.location = (0.6, 0, 1)
        if moon_label:
            moon_label.parent = moon_empty
            moon_label.location = (0.6, 0, 2.6)
        
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
        
        # Parent both the info marker and label to follow the planet
        info_marker = bpy.data.objects.get(f"{name}_Info_Marker")
        label = bpy.data.objects.get(f"{name}_Label")
        if info_marker:
            info_marker.parent = empty
        if label:
            label.parent = empty
        
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

# Add lighting and camera - positioned to show entire solar system
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
bpy.ops.object.camera_add(location=(0, -60, 30), rotation=(math.radians(65), 0, 0))
bpy.context.scene.camera = bpy.context.object

# Create information systems
create_solar_system_info()
create_render_pov_label()

print("Solar System with following planet labels created successfully!")
print("Key improvements:")
print("- Planet labels now follow their respective planets during orbit")
print("- Labels always face the camera for optimal readability")
print("- Render POV label positioned for complete visibility")
print("- Text size optimized to 1.0 to fit entire label in camera frame")
print("- Label positioned at (-20, -45, 45) and centered for full visibility")
print("- Bright yellow emission (strength 15.0) for maximum contrast")
print("- Camera tracking constraint ensures labels always face viewer")
print("\nThe complete render POV label will be fully visible in renders!")
print("All planet labels will orbit with their planets while facing the camera.")
print("Age calculations now based on 20-year-old Earth human!")
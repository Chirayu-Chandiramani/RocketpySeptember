from rocketpy import Environment, SolidMotor, Rocket, Flight
from rocketpy.plots.compare import CompareFlights
import datetime
import os
import pandas as pd
import numpy as np 

# Setting the location of Launch
env = Environment(latitude=19.0729, longitude=72.9006, elevation=9)

# Setting the date & Time of Launch
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, 12)
)  # Hour given in UTC time

# Getting the weather forcast
env.set_atmospheric_model(type="Forecast", file="GFS")

print(env.info())

payload_mass = 1                  
rocket_mass = 14.1 - payload_mass

K1999NP = SolidMotor(     
    thrust_source=r'C:\Users\chand\OneDrive\Documents\SSRP1\RocketPy\AeroTech_K1999N.eng', 
    dry_mass=2.989,
    dry_inertia=(0.02, 0.02, 0.02),
    nozzle_radius=0,
    grain_number=1,
    grain_density=1640,
    grain_outer_radius=0.0428,
    grain_initial_inner_radius=0.02,
    grain_initial_height=0.1524,
    grain_separation=0.0005,
    grains_center_of_mass_position=0.0762,
    center_of_dry_mass_position=0.973, 
    nozzle_position=0,
    burn_time=1.3,
    throat_radius=0,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
) 

# print(Pro75M1670.info())
# With Payload / Before Launch ------------------------------------------------------------------------ 
vajra_with_payload = Rocket(
    radius=0.069,         #ADDED
    mass=rocket_mass+payload_mass,  #Mass without motor
    inertia=(0.28379, 0.28379 , 0.001437), 
    power_off_drag=r'C:\Users\chand\OneDrive\Documents\SSRP1\RocketPy\powerOffDrag.csv',
    power_on_drag=r'C:\Users\chand\OneDrive\Documents\SSRP1\RocketPy\powerOnDrag.csv', 
    center_of_mass_without_motor=1.29,
    coordinate_system_orientation = 'nose_to_tail'
)

vajra_with_payload.add_motor(K1999NP, position=1.6)

rail_buttons = vajra_with_payload.set_rail_buttons(
    upper_button_position=1.04,
    lower_button_position=1.47,
    angular_position=45,
)

nose_cone = vajra_with_payload.add_nose(
    length=0.25,     #ADDED
    kind="lvhaack",  #ADDED
    position=0,      
    base_radius=0.069  #ADDED  
)

fin_set = vajra_with_payload.add_trapezoidal_fins(
    n=3,                #ADDED
    root_chord=0.138,   #ADDED
    tip_chord=0.048,    #ADDED
    span=0.18,  
    position=1.3,  
    cant_angle=0,       #ADDED
    sweep_length=0.092,   
    airfoil= None   
)

tail = vajra_with_payload.add_tail(
    top_radius=0.08000001, bottom_radius=0.08, length=0.3, position=1.3 #our rocket doesnt have a tail as such so this is just a work around.
)

main = vajra_with_payload.add_parachute(   
    name="main",
    cd_s=0.8,
    trigger=800,      # ejection altitude
   
)

drogue = vajra_with_payload.add_parachute(       
    name="drogue",
    cd_s=0.8,
    trigger="apogee",  # ejection at apogee
    
)

flight_with_payload = Flight(      
    rocket=vajra_with_payload,
    environment=env,
    rail_length=5.2,
    inclination=80,
    heading=25,
    terminate_on_apogee=True,
    name="Rocket Flight With Payload",
)

# Without Payload / After Apogee / After Payload deploy-------------------------------------------------

vajra_without_payload = Rocket(
    radius=0.08,
    mass=rocket_mass,
    inertia=(0.28379, 0.28379 , 0.001437), 
    power_off_drag=r'C:\Users\chand\OneDrive\Documents\SSRP1\RocketPy\powerOffDrag.csv',
    power_on_drag=r'C:\Users\chand\OneDrive\Documents\SSRP1\RocketPy\powerOnDrag.csv',  
    center_of_mass_without_motor=1.29,
    coordinate_system_orientation = 'nose_to_tail'
)

main = vajra_without_payload.add_parachute(
    name="main",
    cd_s=0.8,
    trigger=800,      # ejection altitude
)

drogue = vajra_without_payload.add_parachute(
    name="drogue",
    cd_s=0.8,
    trigger="apogee",  # ejection at apogee
)

flight_without_payload = Flight(
    rocket=vajra_without_payload,
    environment=env,
    rail_length=5.2,  # does not matter since the flight is starting at apogee
    inclination=0,
    heading=0,
    initial_solution=flight_with_payload,
    name="Rocket Flight Without Payload",
)

# Simulating the Payload--------------------------------------------------------------------------------

# payload_vajra = Rocket(
#     radius=0.15/2,
#     mass=payload_mass,
#     inertia=(0.1, 0.1, 0.001),
#     power_off_drag=0.5,
#     power_on_drag=0.5,
#     center_of_mass_without_motor=0,
#     coordinate_system_orientation = 'nose_to_tail'

# )

# payload_drogue = payload_vajra.add_parachute(
#     "Drogue",
#     cd_s=0.8,
#     trigger="apogee",
#     sampling_rate=105,
#     lag=1.5,
#     noise=(0, 8.3, 0.5),
# )

# payload_main = payload_vajra.add_parachute(
#     "Main",
#     cd_s=0.8,
#     trigger=800,
#     sampling_rate=105,
#     lag=1.5,
#     noise=(0, 8.3, 0.5),
# )

# payload_flight = Flight(
#     rocket=payload_vajra,
#     environment=env,
#     rail_length=5.2,  # does not matter since the flight is starting at apogee
#     inclination=0,
#     heading=0,
#     initial_solution=flight_with_payload,
#     name="PayloadFlight",
# )

# Plotting the Results--------------------------------------------------------------------------------
comparison = CompareFlights(
    [flight_with_payload, flight_without_payload]
)

# comparison.all(legend=True, ) #All the plots mentioned belowed

comparison.trajectories_3d(legend=True)
comparison.positions(legend=True)
comparison.velocities(legend=True)
comparison.accelerations(legend=True)
comparison.aerodynamic_forces(legend=True)
comparison.aerodynamic_moments(legend=True)
comparison.angles_of_attack(legend=True)

# Visualizing the Trajectory in Google Earth------------------------------------------------------------
flight_with_payload.export_kml(
    file_name="trajectory_with_payload.kml",
    extrude=True,
    altitude_mode="relative_to_ground",
)

flight_without_payload.export_kml(
    file_name="trajectory_without_payload.kml",
    extrude=True,
    altitude_mode="relative_to_ground",
)
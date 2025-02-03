# Define constants outside the functions
# converter kpa to psi and printed it in the main function
# tested kpa to psi function

EARTH_ACCELERATION_OF_GRAVITY = 9.8066500  # m/s^2
WATER_DENSITY = 998.2000000  # kg/m^3
WATER_DYNAMIC_VISCOSITY = 0.0010016  # Pa·s

def water_column_height(tower_height, tank_height):
    """
    Calculates the height of a column of water from a given tower height and tank wall height.

    Parameters:
    tower_height (float): The height of the tower.
    tank_height (float): The height of the tank walls.

    Returns:
    float: The height of the water column.
    """
    h = tower_height + ((3 * tank_height) / 4)
    return h

def pressure_gain_from_water_height(height):
    """
    Calculates the pressure caused by Earth's gravity pulling on the water stored in an elevated tank.

    Parameters:
    height(float): The height of the tank.

    Returns:
    float: The pressure caused by Earth’s gravity
    """
    p = (WATER_DENSITY * EARTH_ACCELERATION_OF_GRAVITY * height)/1000
    return p

def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    """
    Calculates and returns the water pressure lost due to friction in a pipe.

    Parameters:
    pipe_diameter (float): The diameter of the pipe in meters.
    pipe_length (float): The length of the pipe in meters.
    friction_factor (float): The friction factor of the pipe.
    fluid_velocity (float): The velocity of the fluid in meters per second.

    Returns:
    float: The pressure loss in kilopascals.
    """
    # Applying the formula for pressure loss
    pressure_loss = -friction_factor * pipe_length * WATER_DENSITY * fluid_velocity**2 / (2000 * pipe_diameter)

    return pressure_loss

def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """
    Calculates the water pressure lost because of fittings such as 45° and 90° bends that are in a pipeline.
    
    Parameter:
    fluid_velocity (float): the velocity of the water flowing through the pipe in meters / second
    quantity_fittings (float): the quantity of fittings

    Returns:
    float: the lost pressure in kilopascals
    """
    p = -(0.04 * WATER_DENSITY * fluid_velocity**2 * quantity_fittings) / 2000
    return p

def reynolds_number(hydraulic_diameter, fluid_velocity):
    """
    Calculates and returns the Reynolds number for a pipe with water flowing through it.

    Parameter:
    fluid_velocity (float): the velocity of the water flowing through the pipe in meters / second
    hydraulic_diameter (float): the hydraulic diameter of a pipe in meters

    Returns:
    float: the Reynolds number
    """
    r = WATER_DENSITY * hydraulic_diameter * fluid_velocity / WATER_DYNAMIC_VISCOSITY
    return r

def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    """
    Calculates the water pressure lost because of water moving from a pipe with a large diameter into a pipe with a smaller diameter.

    Parameter:
    fluid_velocity (float): the velocity of the water flowing through the pipe in meters / second
    reynolds_number (float): the Reynolds number that corresponds to the pipe with the larger diameter
    larger_diameter (float): the diameter of the larger pipe in meters
    smaller_diameter (float): the diameter of the smaller pipe in meters

    Returns:
    float: the lost pressure kilopascals
    """
    k = (0.1 + (50 / reynolds_number)) * ((larger_diameter/smaller_diameter)**4 -1)
    p = (-k * WATER_DENSITY * fluid_velocity**2) / 2000
    return p

def kpa_to_psi(kpa):
    """
    Converts pressure from kilopascals (kPa) to pounds per square inch (psi).

    Parameter:
    kpa (float): Pressure in kilopascals

    Returns:
    float: Pressure in psi
    """
    return kpa * 0.145038


PVC_SCHED80_INNER_DIAMETER = 0.28687 # (meters)  11.294 inches
PVC_SCHED80_FRICTION_FACTOR = 0.013  # (unitless)
SUPPLY_VELOCITY = 1.65               # (meters / second)
HDPE_SDR11_INNER_DIAMETER = 0.048692 # (meters)  1.917 inches
HDPE_SDR11_FRICTION_FACTOR = 0.018   # (unitless)
HOUSEHOLD_VELOCITY = 1.75            # (meters / second)
def main():
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))
    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)
    diameter = PVC_SCHED80_INNER_DIAMETER
    friction = PVC_SCHED80_FRICTION_FACTOR
    velocity = SUPPLY_VELOCITY
    reynolds = reynolds_number(diameter, velocity)
    loss = pressure_loss_from_pipe(diameter, length1, friction, velocity)
    pressure += loss
    loss = pressure_loss_from_fittings(velocity, quantity_angles)
    pressure += loss
    loss = pressure_loss_from_pipe_reduction(diameter,
            velocity, reynolds, HDPE_SDR11_INNER_DIAMETER)
    pressure += loss
    diameter = HDPE_SDR11_INNER_DIAMETER
    friction = HDPE_SDR11_FRICTION_FACTOR
    velocity = HOUSEHOLD_VELOCITY
    loss = pressure_loss_from_pipe(diameter, length2, friction, velocity)
    pressure += loss
    pressure_psi = kpa_to_psi(pressure)
    print(f"Pressure at house (kpa): {pressure:.1f} kilopascals")
    print(f"Pressure at house (psi): {pressure_psi:.1f} pounds per square inch")


if __name__ == "__main__":
    main()

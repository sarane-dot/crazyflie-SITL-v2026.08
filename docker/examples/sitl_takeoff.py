import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

# We use the custom simlink URI to connect to the SITL firmware executable (which must be running via `./cf2 1`)
URI = 'sim://01'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    # Initialize the low-level drivers (this initializes the simlink driver)
    cflib.crtp.init_drivers()

    print(f"Connecting to {URI}...")

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        print("Connected to Crazyflie SITL!")
        
        # We take off when the commander is created
        print("Taking off!")
        with MotionCommander(scf) as mc:
            print("Hovering for 3 seconds...")
            time.sleep(3)

            print("Moving up 0.2m...")
            mc.up(0.2)
            time.sleep(2)

            print("Moving down 0.2m...")
            mc.down(0.2)
            time.sleep(2)

            print("Landing!")
            # The MotionCommander automatically lands when the context manager exits

    print("Test complete!")

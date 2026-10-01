import logging
import time

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.positioning.motion_commander import MotionCommander

# We define the URIs for our 10 drones
uris = [
    'sim://01', 'sim://02', 'sim://03', 'sim://04', 'sim://05',
    'sim://06', 'sim://07', 'sim://08', 'sim://09', 'sim://10'
]

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def run_shared_sequence(scf):
    """
    This function will be executed in parallel for each drone in the swarm.
    """
    print(f"[{scf.cf.link_uri}] Taking off!")
    
    # MotionCommander takes care of takeoff and landing automatically
    with MotionCommander(scf) as mc:
        print(f"[{scf.cf.link_uri}] Hovering for 3 seconds...")
        time.sleep(3)

        print(f"[{scf.cf.link_uri}] Moving up 0.5m...")
        mc.up(0.5)
        time.sleep(2)
        
        print(f"[{scf.cf.link_uri}] Moving down 0.5m...")
        mc.down(0.5)
        time.sleep(2)

        print(f"[{scf.cf.link_uri}] Landing!")

if __name__ == '__main__':
    print("Initializing drivers...")
    cflib.crtp.init_drivers()

    print(f"Connecting to {len(uris)} drones...")
    factory = CachedCfFactory(rw_cache='./cache')
    
    with Swarm(uris, factory=factory) as swarm:
        print("Connected to all drones!")
        print("Starting synchronized flight sequence...")
        
        # This executes the run_shared_sequence function on all drones in parallel
        swarm.parallel_safe(run_shared_sequence)
        
        print("Swarm sequence completed!")

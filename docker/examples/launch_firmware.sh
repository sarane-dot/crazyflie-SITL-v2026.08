#!/bin/bash
echo "Starting 10 Crazyflie firmware instances..."

# Kill any existing instances first
killall -9 cf2.elf 2>/dev/null || true

# Enter firmware directory
cd /root/crazyflie_sitl_ws/src/crazyflie-firmware || { echo "Firmware directory not found!"; exit 1; }

# Start all 10 drones in the background
for i in {1..10}; do
    # Format the ID as 01, 02, etc.
    id=$(printf "%02d" $i)
    echo "Starting drone $id..."
    nohup ./cf2.elf $id >/dev/null 2>&1 &
done

echo "All 10 instances started in the background!"
echo "To stop them all later, run: killall -9 cf2.elf"

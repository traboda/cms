import asyncio
from bleak import BleakScanner


async def main():
    devices = await BleakScanner.discover(timeout=20.0)
    arr = []
    for d in devices:
        arr.append({
            'address': d.address,
            'name': d.name
        })
    return arr


def get_bluetooth_address():
    return asyncio.run(main())

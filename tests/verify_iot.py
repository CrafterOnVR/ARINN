
import unittest
from arinn_core.iot_bridge import IoTBridge

class TestIoT(unittest.TestCase):
    def test_01_device_control(self):
        print("\n[TEST] Verifying IoT Bridge...")
        iot = IoTBridge()
        
        # 1. Check Initial State
        status = iot.get_status()
        self.assertIn("Study_Lamp", status)
        self.assertEqual(status["Study_Lamp"]["power"], "off")
        print("  > Initial State Verified (Off)")
        
        # 2. Control Device
        success, msg = iot.control_device("Study_Lamp", "power_on")
        print(f"  > Control 'power_on' -> {msg}")
        self.assertTrue(success)
        
        # 3. Verify Change
        status = iot.get_status()
        self.assertEqual(status["Study_Lamp"]["power"], "on")
        print("  > State Change Verified (On)")
        
        # 4. Brightness
        iot.control_device("Study_Lamp", "set_brightness", 80)
        self.assertEqual(iot.get_status()["Study_Lamp"]["brightness"], 80)

if __name__ == '__main__':
    unittest.main()

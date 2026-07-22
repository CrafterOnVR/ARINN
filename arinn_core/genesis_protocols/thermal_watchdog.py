import subprocess
import time
import logging

logger = logging.getLogger(__name__)

class ThermalWatchdog:
    """
    ARINN Blueprint Part VIII.5: The Miniscule Bug Physical Reality.
    A continuous watchdog polling `nvidia-smi` to prevent thermal meltdowns
    during extended 168-hour Genesis Run setups.
    """
    def __init__(self, max_temp_celsius=85, sleep_duration=300):
        self.max_temp = max_temp_celsius
        self.sleep_duration = sleep_duration

    def get_gpu_temperature(self):
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                temp_str = result.stdout.strip()
                return int(temp_str)
        except Exception as e:
            logger.warning(f"Failed to poll nvidia-smi: {e}")
            pass
        return None

    def assert_thermal_limits(self):
        """
        Polls the hardware. If the limit is exceeded, suspends the executing thread.
        To be called continuously inside Omega or Research learning loops.
        """
        temp = self.get_gpu_temperature()
        if temp is None:
            return True # Assumed safe if no GPU detected
            
        if temp >= self.max_temp:
            logger.critical(f"[THERMAL OVERLOAD] GPU Temperature {temp}°C exceeded threshold {self.max_temp}°C. Suspending logic for {self.sleep_duration} seconds.")
            time.sleep(self.sleep_duration)
            return False # Indicated a suspension occurred
        return True

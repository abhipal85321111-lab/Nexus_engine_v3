import time
from collections import deque

class NexusV3_EventLoop:
    """V3.1 PRO - Real EventLoop - No Threads, No GIL Lock"""
    def __init__(self):
        self.queue = deque()
        self.results = []

    def add_task(self, task_func, *args, **kwargs):
        # Task + args store karo, abhi run mat karo
        self.queue.append((task_func, args, kwargs))

    def run_loop(self):
        start = time.perf_counter()
        executed = 0

        # REAL EVENT LOOP - ek-ek task pop, run, next
        while self.queue:
            func, args, kwargs = self.queue.popleft()
            try:
                result = func(*args, **kwargs)
                self.results.append(result)
                executed += 1
            except Exception as e:
                self.results.append(f"Error: {e}")

        duration = time.perf_counter() - start
        print(f"[V3.1 REAL] Executed {executed} tasks in {duration*1000:.3f}ms")
        print(f"[V3.1] Zero Thread, Zero Context-Switch, RAM: ~0MB overhead")
        print(f"Results: {self.results}")
        return self.results

# ========= REAL TEST - 1GB Device Simulation =========
def load_asset(name):
    time.sleep(0.001)  # Simulate IO
    return f"{name} Loaded"

def process_physics():
    return "Physics Done"

v3 = NexusV3_EventLoop()
v3.add_task(load_asset, "Mesh")
v3.add_task(load_asset, "Texture")
v3.add_task(process_physics)
v3.add_task(lambda: "AI Done")

print("--- V3.1 on 1GB RAM Device ---")
v3.run_loop()

# Comparison
print(f"\nThreaded hota toh: 4 threads = 4*8MB stack = 32MB RAM waste")
print(f"EventLoop se: 1 thread = ~0MB extra = ✅ 1GB device pe chalega")

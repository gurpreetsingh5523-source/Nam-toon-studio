"""
performance_profiler_module.py
Profile code performance using cProfile and memory_profiler.
"""
import cProfile
import pstats
import sys

def profile_script(script_path):
    profiler = cProfile.Profile()
    profiler.run(f'exec(open("{script_path}").read())')
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime').print_stats(20)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python performance_profiler_module.py <script.py>")
    else:
        profile_script(sys.argv[1])

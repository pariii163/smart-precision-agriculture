import time

# Simulated sensor readings (CSV format)
simulated_data = [
    "90,42,43,6.5,25,60,30",
    "88,41,42,6.6,26,59,32",
    "85,40,41,6.7,27,58,35"
]

print("Starting simulated sensor stream...\n")

for line in simulated_data:
    print(line)
    time.sleep(1)

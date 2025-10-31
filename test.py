import time

for i in range(255):
    print(f"\x1B[38;5;{i}mComplete : {i}", end="\r")
    time.sleep(0.25)

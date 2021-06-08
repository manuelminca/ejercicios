import asyncio
import random
import time

BOOTS = 0

async def make_boot():

    global BOOTS
    manufacturing_time = random.choice([1,3,5])
    await asyncio.sleep(manufacturing_time)
    BOOTS += 1

async def make_print():
    t0 = time.time()
    offset = 0.0
    while 1:
        global BOOTS
        await asyncio.sleep(1 - offset)
        t1 = time.time()
        current_time = t1 -t0
        offset = float(str(current_time-int(current_time))[1:])
        print(offset)
        print("seconds: {0} boots: {1}".format(current_time - offset, BOOTS))


async def worker():
    while 1:
        await make_boot()

def main():
    workers = 10
    loop = asyncio.get_event_loop()
    loop.create_task(make_print())
    for i in range(workers):
        loop.create_task(worker())
    loop.run_forever()

if __name__ == "__main__":
    # execute only if run as a script

    main()

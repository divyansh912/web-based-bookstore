import os
import sys
import multiprocessing
import time

BUFFER_SIZE = 5
NUM_ITERATIONS = 10

def producer(empty, full, mutex):
    for i in range(NUM_ITERATIONS):
        empty.acquire()
        mutex.acquire()

        print(f"Produced: {i}")
        sys.stdout.flush()  # Ensure immediate printing

        mutex.release()
        full.release()

def consumer(empty, full, mutex):
    for i in range(NUM_ITERATIONS):
        full.acquire()
        mutex.acquire()

        print(f"Consumed: {i}")
        sys.stdout.flush()  # Ensure immediate printing

        mutex.release()
        empty.release()

if __name__ == "__main__":
    empty = multiprocessing.Semaphore(BUFFER_SIZE)
    full = multiprocessing.Semaphore(0)
    mutex = multiprocessing.Semaphore(1)

    producer_process = multiprocessing.Process(target=producer, args=(empty, full, mutex))
    consumer_process = multiprocessing.Process(target=consumer, args=(empty, full, mutex))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()

    # Cleanup
    empty.unlink()
    full.unlink()
    mutex.unlink()

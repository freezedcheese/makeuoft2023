import asyncio
import platform
import sys
import numpy as np
import cv2
import time

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

def most_common(lst):
    return max(set(lst), key=lst.count)

async def person_detection():
    global write_buffer
    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    cv2.startWindowThread()

# open webcam video stream
    cap = cv2.VideoCapture(0)
    last15Positions = []
    currentPosition = 'N'
    mostCommon = 'N'
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        if (boxes.size == 0):
            currentPosition = 'N'
        else:
            for (xA, yA, xB, yB) in boxes:
                averageX = (xA + xB)/2
                Ypercentage = (yB - yA)/480
                if (Ypercentage > 0.85):
                    # print("soon")
                    currentPosition = 'S'
                elif (averageX > 420):
                    # print("right")
                    currentPosition = 'R'
                elif (averageX < 220):
                    # print("left")
                    currentPosition = 'L'
                else:
                    # print("center")
                    currentPosition = 'C'
                # display the detected boxes in the colour picture
                cv2.rectangle(frame, (xA, yA), (xB, yB),
                                (0, 0, 255), 2)
            
        if (len(last15Positions) < 15):
            last15Positions.append(currentPosition)
        else:
            last15Positions.pop(0)
            last15Positions.append(currentPosition)
            mostCommon = most_common(last15Positions)

        if (mostCommon == 'S'):
            write_buffer = b'\x53'
        elif (mostCommon == 'R'):
            write_buffer = b'\x52'
        elif (mostCommon == 'L'):
            write_buffer = b'\x4C'
        elif (mostCommon == 'N'):
            write_buffer = b'\x4E'
        elif (mostCommon == 'C'):
            write_buffer = b'\x43'
        print(write_buffer)
            
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        await asyncio.sleep(0.01)
    # When everything done, release the capture
    cap.release()
    # and release the output
    # finally, close the window
    cv2.destroyAllWindows()
    cv2.waitKey(1)


async def sending():
    global write_buffer
    device = await initialize_device("4E7C561E-E54F-00E3-8572-5784F0B92FDC")
    k = 0
    while True:
            print("sent:", write_buffer, k)
            async with BleakClient(device) as client:
                    for service in client.services:
                        for char in service.characteristics:
                            if 'write' in char.properties:
                                await client.write_gatt_char(char.uuid, write_buffer)  # this send data to device
                                print("sent")
                                await asyncio.sleep(0.01)
            k+=1
            await asyncio.sleep(0.01)

async def initialize_device(ble_address):
    device = await BleakScanner.find_device_by_address(ble_address, timeout=10.0)
    if not device:
        raise BleakError("A device with address {ble_address} could not be found.")
    else:
        print("initialised")
    return device

async def processing():
    global write_buffer
    write_buffer = b'\x49'
    # device = await asyncio.run(initialize_device("4E7C561E-E54F-00E3-8572-5784F0B92FDC"))
    
    for j in range(10):
        for i in range(30):
            print("processing")
            time.sleep(1/30)
            if (write_buffer == b'\x46'):
                write_buffer = b'\x47'
            else:
                write_buffer = b'\x46'
            await asyncio.sleep(0.01)

async def main():
    global write_buffer
    write_buffer = b'\x49'
    
    sender = asyncio.create_task(sending())
    processor = asyncio.create_task(person_detection())

    await sender
    await processor

if __name__ == "__main__":
    write_buffer = b'\x49'
    asyncio.run(main())
    
    # person_detection()





# async def sending():
#     global write_buffer
#     # device = await initialize_device("4E7C561E-E54F-00E3-8572-5784F0B92FDC")
#     k = 0
#     while True:
#             print(write_buffer, k, "- variable")
#             # async with BleakClient(device) as client:
#                     # for service in client.services:
#                         # for char in service.characteristics:
#                             # if 'write' in char.properties:
#                                 # await client.write_gatt_char(char.uuid, write_buffer)  # this send data to device
#             # print(write_buffer, " - variable")
#             k+=1

# async def initialize_device(ble_address):
#     device = await BleakScanner.find_device_by_address(ble_address, timeout=10.0)
#     if not device:
#         raise BleakError("A device with address {ble_address} could not be found.")
#     return device

# async def processing():
#     global write_buffer
#     write_buffer = b'\x00'
#     loop.create_task(sending())
#     # device = await asyncio.run(initialize_device("4E7C561E-E54F-00E3-8572-5784F0B92FDC"))
#     for j in range(10):
#         for i in range(30):
#             print("processed")
#             time.sleep(1/30)
#             if (write_buffer == b'\x00'):
#                 write_buffer = b'\x01'
#             else:
#                 write_buffer = b'\x00'
#             #await asyncio.sleep(1)

# async def main():
#     global write_buffer
#     write_buffer = b'\x00'
#     # sender = asyncio.create_task(sending())
#     # processor = asyncio.create_task(processing())
#     f1 = loop.create_task(processing())
#     f2 = loop.create_task(sending())
#     await asyncio.wait([f1, f2])

#     # await sender
#     # await processor

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     # asyncio.run(main())
    
#     # person_detection()
    
import serial

def nozzle(frame, box):

    tx = (box[0] - box[2]) * 0.5
    y = (box[1] - box[3]) * 0.5
    x = box[0] + tx
    ty = box[1] + y

    # separate line
    h, w, c = frame.shape

    w = w * 0.5
    w1 = w * 0.5 # 0%-25%
    w2 = w1 + w1 # 25%-50%
    w3 = w2 + w1 # 50%-75%
    w4 = w3 + w1 # 75%-100%
    
    if ty <= 300 and ty <= 280:

        if x <= w1:
            i = [1, 0, 0, 0]

        if x >= w1 and x <= w2:
            i = [0, 1, 0, 0]

        if x >= w2 and x <= w3:
            i = [0, 0, 1, 0]

        if x >= w3 and x <= w4:
            i = [0, 0, 0, 1]

        ser = serial.Serial("COM4", 9600, timeout=None)
        ser.write(i)
        ser.close()
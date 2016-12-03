import numpy as np
import cv2

CR = 0
CV = 0
camera = cv2.VideoCapture(0)
lower_red = np.array([134,110,80])
upper_red = np.array([170,245,255])

green_lower = np.array([50, 100, 100], dtype=np.uint8)
green_upper = np.array([70, 255, 255], dtype=np.uint8)

_, frame = camera.read()

while True:

        _, frame = camera.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 50, 150)
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.01 * peri, True)

                if len(approx) >= 4 and len(approx) <= 6:
                       
                        (x, y, w, h) = cv2.boundingRect(approx)
                        aspectRatio = w / float(h)

                        
                        area = cv2.contourArea(c)
                        hullArea = cv2.contourArea(cv2.convexHull(c))
                        solidity = area / float(hullArea)
                        keepDims = w > 25 and h > 25
                        keepSolidity = solidity > 0.9
                        keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2 

                        
                        if keepDims and keepSolidity and keepAspectRatio:
                                
                                cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                                light = frame[y:y+h,x:x+w]
                                cv2.imshow("Resultado", light)                                                
                                
                                hsv = cv2.cvtColor(light, cv2.COLOR_BGR2HSV)
                                mask2 = cv2.inRange(hsv, green_lower, green_upper)
                                frame2 = cv2.bitwise_and(light,light,mask = mask2)
                                frame3 = frame2.astype('bool')
                                mask = cv2.inRange(hsv,lower_red, upper_red)
                                maskOut = cv2.bitwise_and(light,light,mask = mask)
                                mask2 = maskOut.astype('bool')
                                if True in mask2:
                                        CR+=1
                                        print CR,'semaforo vermelho'

                                elif True in frame3:
                                        CV+=1
                                        print CV,'semaforo verde'
                                
                               
       
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        
        if key == ord("q") or key == ord("Q"):
                break


camera.release()
cv2.destroyAllWindows()


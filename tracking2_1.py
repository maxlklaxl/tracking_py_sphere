#comment
#comment2
import cv2
import numpy as np
from datetime import datetime

def nothing(*arg):
    pass


class benchmarke:
    def __init__(self):
        self.prevTime = datetime.now()
        self.framecount = 0
        
    def stoppTime(self):
        self.framecount = self.framecount +1
        if (self.framecount == 60):
            dt = datetime.now()
            diff = dt - self.prevTime
            fps = float(self.framecount)/float(diff.microseconds/1.0E6)
            print "Diff:" , diff, " FPS:", fps
            self.prevTime = dt 
            self.framecount = 0
        
    
class video:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.flag , self.frame = self.cap.read() 

    def getFrame(self):
        self.flag, self.frame = self.cap.read()#
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        return self.flag, self.frame
      
    def newWindow(self, name, frame):
            cv2.imshow(name,frame)

class tracking:
    def __init__(self):
        flag, frame = vid.getFrame()
        self.bg = frame
        self.bgAverage = np.float32(frame)
        self.binsize = 10
        self.xAv, self.yAv = [0]*self.binsize,[0]*self.binsize
        
    def getBackground(self):
        print """Getting Background...
 - "ESC" to continue and save BG
 - "l" for loading prev. saved BG and continue"""
        while True:
            flag, frame = vid.getFrame()
            cv2.accumulateWeighted(frame,self.bgAverage,0.08) # calculates the average, 0.08 is the weight of the image
            self.bg = cv2.convertScaleAbs(self.bgAverage)# build 8-bit grayscale pictue out of average
            vid.newWindow("Background", self.bg)
            vid.newWindow("Original", frame)
            k = cv2.waitKey(33)
            if k == 27:         # wait for ESC key to exit
                cv2.imwrite('bg.png',self.bg)
                cv2.destroyAllWindows()
                break
            elif k == ord('l'): # wait for 's' key to save and exit
                self.bg = cv2.imread('bg.png',0)
                cv2.destroyAllWindows()
                break
    
    def getCnt(self,contours):
        #Get centroide of best Counters
        best_cnt = 1
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_cnt = cnt
        return best_cnt
    
    def drawLine(self,best_cnt, frame):
            pass
            vx,vy,x,y = cv2.fitLine(best_cnt,cv2.cv.CV_DIST_L2, 0, 0.01, 0.01)
            # Averageing
            self.xAv.append(vx)
            self.yAv.append(vy)
            del self.xAv[0]
            del self.yAv[0]
            vx = sum(self.xAv)/self.binsize
            vy = sum(self.yAv)/self.binsize
            x0 = x+vx*20
            y0 = y+vy*20
            x1 = x-vx*20
            y1 = y-vy*20
            cv2.line(frame,(x1,y1),(x0,y0), (255,255,100),2)
    
    def drawMoments(self, best_cnt, frame):
            M = cv2.moments(best_cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(frame,(cx,cy),2,(0,0,255),-1)
            
    def prepare(self):
        # Read settings
        sett.readBars()
        
        #Get Frame
        flag, frame0 = vid.getFrame()
        
        #convert to grayscale
        ##frame = man.convToGray(frame0)
        
        #BackgroundSub
        frame = cv2.absdiff(frame0, self.bg)
       
        #Blur 
        ##frame = cv2.medianBlur(frame, sett.blur)
        #vid.newWindow("Blur", man.resize(frame, 960/3, 720/3))
        
        #Erode
        kernEr = cv2.getStructuringElement(cv2.MORPH_ERODE,(sett.erode,sett.erode))
        frame = cv2.erode(frame, kernEr)
        frame = cv2.erode(frame, kernEr)
        vid.newWindow("Erode",cv2.resize(frame, (960/3, 720/3)))
        
        #Dilate
        kernelDil = cv2.getStructuringElement(cv2.MORPH_DILATE,(sett.dilate,sett.dilate))
        frame = cv2.dilate(frame, kernelDil)
        vid.newWindow("Dilate", cv2.resize(frame, (960/3, 720/3)))
        
        #Erode 
        frame = cv2.erode(frame, kernEr)
        
        #Threshold Frame
        _, frame = cv2.threshold(frame, sett.tr_Low, sett.tr_High, cv2.THRESH_BINARY)
        vid.newWindow("Th", cv2.resize(frame, (960/2, 720/2)))    
        
        #Contuures   
        frame0 = cv2.cvtColor(frame0, cv2.COLOR_GRAY2RGB)
        contours,hierarchy = cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame0, contours, -1, (255,0,255))
        #contours = 0
        return contours, frame0
            
    def track(self, contours, frame0 ):
        best_cnt = self.getCnt(contours)
        if type(best_cnt) != int:   #avoid errors if no cnt
            #compute and draw line
            self.drawLine(best_cnt, frame0)
            # draw circle from line x and y from line! 
            ## cv2.circle(frame0,(x,y),4,(255,255,0),-1)
            #compute and draw movement predictor (centroide)
            self.drawMoments(best_cnt, frame0)
            #Ellipse
            try:
                ellipse = cv2.fitEllipse(best_cnt)
                cv2.ellipse(frame0,ellipse,(200,255,200),1)
            except:
                pass
            #Hull
            hull = cv2.convexHull(best_cnt)
            cv2.drawContours(frame0, [hull],-1, (50,200,255))
            
        vid.newWindow("Main", frame0) 
        

class settings():
    def __init__(self):
        cv2.namedWindow('Settings')
        cv2.createTrackbar('Blur', 'Settings', 3, 20, nothing)
        cv2.createTrackbar('TreshLow', 'Settings', 77, 255, nothing)
        cv2.createTrackbar('TreshHigh', 'Settings', 255, 255, nothing)
        cv2.createTrackbar('Erode', 'Settings', 2, 12, nothing)
        cv2.createTrackbar('Dilate', 'Settings', 1, 12, nothing)
        #cv2.createTrackbar('Stopp=0 Go=1', 'Settings', 0, 1, nothing)
        # cv2.createTrackbar('TreshHigh', 'Settings', 0, 255, nothing)
        self.readBars()
        
    def readBars(self):
        self.blur = cv2.getTrackbarPos('Blur', 'Settings')
        self.blur = self.blur*2+1 # convert to ungerade: cv2.medianBlur nimmt nur ungerade zahlen
        self.tr_Low = cv2.getTrackbarPos('TreshLow', 'Settings')
        self.tr_High = cv2.getTrackbarPos('TreshHigh', 'Settings')
        self.erode = cv2.getTrackbarPos('Erode', 'Settings')
        if self.erode < 1:
            self.erode=1
        self.dilate = cv2.getTrackbarPos('Dilate', 'Settings')
        if self.dilate < 1:
            self.dilate= 1
        #self.state = cv2.getTrackbarPos('Stopp=0 Go=1', 'Settings')
        

if __name__ == '__main__':
    #load Classes
    vid = video()
    trk = tracking()
       
    #get Background
    trk.getBackground()
    
    #Start Settings 
    sett = settings()
    
    #Start Benchmarking
    bench = benchmarke()
    
    print """Tracking started"""
    while True:
        contours, frame0 = trk.prepare()
        trk.track(contours, frame0)
        bench.stoppTime()
        ch = cv2.waitKey(5)
        if ch == 27:
            break
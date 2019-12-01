from ximea import xiapi
import cv2
import time

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

#create instance for first connected camera 
cam = xiapi.Camera()

#start communication
print('Opening first camera...')
cam.open_device()

#settings
cam.set_exposure(9090)

#create instance of Image to store image data and metadata
img = xiapi.Image()

#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()

try:
    print('Starting video. Press CTRL+C to exit.')
    t0 = time.time()
    while True:
        #get data and pass them from camera to img
        cam.get_image(img)

        #create numpy array with data from camera. Dimensions of the array are 
        #determined by imgdataformat
        data = img.get_image_data_numpy()

        #show acquired image with time since the beginning of acquisition
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = '{:5.2f}'.format(time.time()-t0)
        cv2.putText(
            data, text, (900,150), font, 4, (255, 255, 255), 2
            )
        
        resize = ResizeWithAspectRatio(data, width=1000)
        cv2.imshow('XiCAM example', resize)
        cv2.moveWindow("XiCAM example", 1000,0);

        cv2.waitKey(1)
        
except KeyboardInterrupt:
    cv2.destroyAllWindows()

#stop data acquisition
print('Stopping acquisition...')
cam.stop_acquisition()

#stop communication
cam.close_device()

print('Done.')

# coding: UTF-8
import time
import cv2
import numpy as np
import paho.mqtt.client as paho
import threading

IS_CV3 = ( cv2.__version__[0] == '3' )
g_mutex = threading.Lock()
g_frame = None
g_running = False

# Configure here your connection parameters
#
MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "rcr/video"

DEVICE = 0
FPS = 10
#
# End configuration

def _TSendVideoFrame( fps ):
    global MQTT_SERVER, MQTT_PORT, MQTT_TOPIC, g_mutex, g_frame, g_running

    mqtt_client = paho.Client()
    mqtt_client.connect( MQTT_SERVER, MQTT_PORT )
    mqtt_client.loop_start()

    winName = "Debug"
    cv2.namedWindow( winName, cv2.WINDOW_AUTOSIZE )

    tf = 1./fps
    t1 = 0.
    while( g_running ):
        g_mutex.acquire()
        if( g_frame is not None ):
            frame = np.copy( g_frame )
            g_mutex.release()

            data = cv2.imencode( '.jpg', frame )[1].tostring()
            mqtt_client.publish( MQTT_TOPIC, data )

            t2 = time.time()
            dt = 1./( t2 - t1 )
            cv2.putText( frame, "%03.1f FPS" % ( dt ), ( 10, 30 ), cv2.FONT_HERSHEY_SIMPLEX, 1, ( 255, 255, 255 ) )
            cv2.imshow( winName, frame )
            t1 = t2

        else:
            g_mutex.release()
        time.sleep( tf )
    mqtt_client.loop_stop()

def main( device, fps ):
    global IS_CV3, g_mutex, g_frame, g_running

    # abrimos dispositivo de captura
    cap = cv2.VideoCapture( device )

    # establecemos ventana y dimensiones de la captura
    winName = 'Video Out'
    imgH,imgW = 240, 320
    if( IS_CV3 ):
        cv2.namedWindow( winName, cv2.WINDOW_AUTOSIZE )
        cap.set( cv2.CAP_PROP_FRAME_HEIGHT, imgH )
        cap.set( cv2.CAP_PROP_FRAME_WIDTH, imgW )
    else:
        cv2.namedWindow( winName, cv2.CV_WINDOW_AUTOSIZE )
        cap.set( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, imgH )
        cap.set( cv2.cv.CV_CAP_PROP_FRAME_WIDTH, imgW )
    cv2.resizeWindow( winName, imgW, imgH )

    # levantamos tarea que envia el frame
    g_running = True
    tSendVideoFrame = threading.Thread( target=_TSendVideoFrame, args=( fps, ), name="_TSendVideoFrame" )
    tSendVideoFrame.start()

    # procesamos hasta que recibamos ESC
    t1 = 0.
    while True:
        # internamente hay un buffer que puede producir lags a bajos FPS
        # poca luz genera demoras en la decodificación
        ret, frame = cap.read()
        if( ret ):
            # lo dejamos disponible para la tarea
            g_mutex.acquire()
            g_frame = np.copy( frame )
            g_mutex.release()

            # lo mostramos a la maxima velocidad de captura
            t2 = time.time()
            dt = 1./( t2 - t1 )
            cv2.putText( frame, "%03.1f FPS" % ( dt ), ( 10, imgH-10 ), cv2.FONT_HERSHEY_SIMPLEX, 1, ( 255, 255, 255 ) )
            cv2.imshow( winName, frame )
            t1 = t2

        # verificamos si se presiona ESC
        if( cv2.waitKey( 1 ) == 27 ):
            break

    # finalizamos las tareas
    g_running = False
    tSendVideoFrame.join()

    # liberamos cv2
    cap.release()
    cv2.destroyAllWindows()


# Show time
main( DEVICE, FPS )

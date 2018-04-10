# coding: UTF-8
from __future__ import print_function
import time
import cv2
import numpy as np
import paho.mqtt.client as paho
import threading

IS_CV3 = ( cv2.__version__[0] == '3' )
g_mutex = threading.Lock()
g_frame = None
g_running = False

WIN_CAPTURE = "Capture"
WIN_SEND = "Video Out"
CTRL_FPS = "FPS"

# Configure here your connection parameters
#
MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "rcr/video"

DEVICE = 0
#
# End configuration

def _TSendVideoFrame():
    global g_mutex, g_frame, g_running, WIN_CAPTURE, WIN_SEND, MQTT_SERVER, MQTT_PORT, MQTT_TOPIC

    mqtt_client = paho.Client()
    mqtt_client.connect( MQTT_SERVER, MQTT_PORT )
    mqtt_client.loop_start()

    t1 = 0.
    while( g_running ):
        fps = cv2.getTrackbarPos( CTRL_FPS, WIN_SEND )
        if( fps > 0 ):
            g_mutex.acquire()
            if( g_frame is not None ):
                frame = np.copy( g_frame )
            else:
                frame = None
            g_mutex.release()
            if( frame is not None ):
                data = cv2.imencode( '.jpg', frame )[1].tostring()
                mqtt_client.publish( MQTT_TOPIC, data )

                t2 = time.time()
                dt = 1./( t2 - t1 )
                cv2.putText( frame, "%03.1f FPS" % ( dt ), ( 10, 30 ), cv2.FONT_HERSHEY_SIMPLEX, 1, ( 255, 255, 255 ) )
                cv2.imshow( WIN_SEND, frame )
                t1 = t2
            tf = 1./fps
            time.sleep( tf )
        else:
            frame[:] = 0
            cv2.imshow( WIN_SEND, frame )
            time.sleep( 0.001 )
    mqtt_client.loop_stop()

def trackControls( obj ):
    pass

def main( device ):
    global IS_CV3, g_mutex, g_frame, g_running, WIN_CAPTURE, WIN_SEND

    # abrimos dispositivo de captura
    cap = cv2.VideoCapture( device )

    # establecemos ventana y dimensiones de la captura
    imgH,imgW = 240, 320
    if( IS_CV3 ):
        cv2.namedWindow( WIN_CAPTURE, cv2.WINDOW_NORMAL )
        cv2.namedWindow( WIN_SEND, cv2.WINDOW_NORMAL )
        cap.set( cv2.CAP_PROP_FRAME_HEIGHT, imgH )
        cap.set( cv2.CAP_PROP_FRAME_WIDTH, imgW )
    else:
        cv2.namedWindow( WIN_CAPTURE, cv2.CV_WINDOW_NORMAL )
        cv2.namedWindow( WIN_SEND, cv2.CV_WINDOW_NORMAL )
        cap.set( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, imgH )
        cap.set( cv2.cv.CV_CAP_PROP_FRAME_WIDTH, imgW )
    cv2.resizeWindow( WIN_CAPTURE, imgW, imgH )
    cv2.resizeWindow( WIN_SEND, imgW, imgH )

    # creamos un trackbar para definir los FPS
    cv2.createTrackbar( CTRL_FPS, WIN_SEND, 5, 30, trackControls )

    # levantamos tarea que envia el frame
    g_running = True
    tSendVideoFrame = threading.Thread( target=_TSendVideoFrame, args=(), name="_TSendVideoFrame" )
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
            cv2.imshow( WIN_CAPTURE, frame )
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
main( DEVICE )

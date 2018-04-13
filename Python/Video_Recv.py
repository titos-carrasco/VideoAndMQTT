# coding: UTF-8
from __future__ import print_function
import time
import cv2
import numpy as np
import paho.mqtt.client as paho
import threading
import Queue

import wx
import wx.lib.newevent
import Video_Recv_wx as wxMainFrame

C_IS_CV3 = ( cv2.__version__[0] == '3' )

#### Cambiar aqui
G_MQTT_SERVER = "test.mosquitto.org"
G_MQTT_PORT = 1883
G_MQTT_TOPIC = "rcr/video"
####

class MainApp( wx.App ):
    def OnInit( self ):
        # esto deberian poder ser cambiados en la GUI
        self.MQTT_SERVER = G_MQTT_SERVER
        self.MQTT_PORT = G_MQTT_PORT
        self.MQTT_TOPIC = G_MQTT_TOPIC

        # algunas definiciones
        self.messages = Queue.Queue()

        # operaciones GUI en el thread principal
        self.evtShowImage, EVT_SHOW_IMAGE = wx.lib.newevent.NewEvent()
        self.Bind( EVT_SHOW_IMAGE, self._UpdateImage )

        # levantamos la GUI
        self.mainFrame = wxMainFrame.MainFrame( parent=None )
        self.mainFrame.Bind( wx.EVT_CLOSE, self.OnClose )
        self.mainFrame.Bind( wx.EVT_MENU, self.OnSalir, id=wxMainFrame.ID_SALIR )
        self.mainFrame.Show()

        # levantamos las tareas
        self.running = True
        self.tRecvVideo = threading.Thread( target=self._TRecvVideo, args=( ), name="_TRecvVideo" )
        self.tRecvVideo.start()

        return True

    def OnSalir( self, event ):
        self.mainFrame.Close()

    def OnClose( self, event ):
        # terminamos las tareas
        self.running = False
        self.tRecvVideo.join()

        # propagamos la salida
        event.Skip()

    def _mqtt_on_message( self, client, userdata, message ):
        # ponemos el mensaje en la cola para procesamiento posterior
        self.messages.put_nowait( message )

    def _mqtt_on_connect( self, client, arg1, arg2, arg3 ):
        # nos suscribimos al topico que nos interesa
        client.subscribe( self.MQTT_TOPIC )

    def _TRecvVideo( self ):
        mqtt_client = paho.Client()
        mqtt_client.on_connect = self._mqtt_on_connect
        mqtt_client.on_message = self._mqtt_on_message
        mqtt_client.connect( self.MQTT_SERVER, self.MQTT_PORT )
        mqtt_client.loop_start()

        if( C_IS_CV3 ):
            LOAD_IMAGE_COLOR = cv2.IMREAD_COLOR
        else:
            LOAD_IMAGE_COLOR = cv2.CV_LOAD_IMAGE_COLOR

        while( self.running ):
            try:
                # recibimos un frame de video
                message = self.messages.get_nowait()
                data = np.fromstring( message.payload, np.uint8 )
                img = cv2.imdecode( data, LOAD_IMAGE_COLOR )

                # lo mostramos
                evt = self.evtShowImage( panel=self.mainFrame.RecvImage, img=img )
                wx.PostEvent( self, evt )
            except Queue.Empty:
                pass
            except Exception as e:
                print( e )

            time.sleep( 0.001 )

        # cerramos la conexion
        mqtt_client.loop_stop()
        print( 'Cerrando Recv' )

    def _UpdateImage( self, evt ):
        # los parametros
        panel = evt.panel
        img = evt.img

        # el tamano de la imagen
        imgH, imgW = img.shape[:2]

        # la mostramos ajustado a la ventana
        if( C_IS_CV3 ):
            img = cv2.cvtColor( img, cv2.COLOR_BGR2RGB )
        else:
            img = cv2.cvtColor( img, cv2.cv.CV_BGR2RGB )
        w, h = panel.Size
        if( w>0 and h>0 ):
            img = cv2.resize( img, (w, h) )
            bmp = wx.BitmapFromBuffer( w, h, img )
            dc = wx.ClientDC( panel )
            dc.DrawBitmap( bmp, 0, 0 )
            dc = None


# Show time
myApp = MainApp( False )
myApp.MainLoop()




"""

def main():
    global IS_CV3, MQTT_SERVER, MQTT_PORT, messages

    # establecemos ventana y dimensiones
    winName = 'Video In'
    imgH,imgW = 240, 320
    if( IS_CV3 ):
        cv2.namedWindow( winName, cv2.WINDOW_AUTOSIZE )
        LOAD_IMAGE_COLOR = cv2.IMREAD_COLOR
    else:
        cv2.namedWindow( winName, cv2.CV_WINDOW_AUTOSIZE )
        LOAD_IMAGE_COLOR = cv2.CV_LOAD_IMAGE_COLOR
    cv2.resizeWindow( winName, imgW, imgH )

    # nos conectamos al servidor MQTT
    mqtt_client = paho.Client()
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message
    mqtt_client.connect( MQTT_SERVER, MQTT_PORT )
    mqtt_client.loop_start()

    # procesamos hasta que recibamos ESC
    while True:
        try:
            # recibimos un frame
            message = g_messages.get_nowait()
            data = np.fromstring( message.payload, np.uint8 )
            frame = cv2.imdecode( data, LOAD_IMAGE_COLOR )

            # mostramos el frame
            cv2.imshow( winName, frame )
        except Queue.Empty:
            pass
        except Exception as e:
            print e

        # verificamos si se presiona ESC
        if( cv2.waitKey( 1 ) == 27 ):
            break

    # eso es todo
    mqtt_client.loop_stop()
    cv2.destroyAllWindows()


# Show time
main()
"""

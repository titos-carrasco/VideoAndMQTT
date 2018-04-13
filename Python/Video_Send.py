# coding: UTF-8
from __future__ import print_function
import time
import cv2
import numpy as np
import paho.mqtt.client as paho
import threading

import wx
import wx.lib.newevent
import Video_Send_wx as wxMainFrame

C_IS_CV3 = ( cv2.__version__[0] == '3' )

#### Cambiar aqui
G_DEVICE = 0
G_WIDTH = 320
G_HEIGHT = 240
G_MQTT_SERVER = "test.mosquitto.org"
G_MQTT_PORT = 1883
G_MQTT_TOPIC = "rcr/video"
####

class MainApp( wx.App ):
    def OnInit( self ):
        # esto deberian poder ser cambiados en la GUI
        self.DEVICE = G_DEVICE
        self.imgW = G_WIDTH
        self.imgH = G_HEIGHT
        self.MQTT_SERVER = G_MQTT_SERVER
        self.MQTT_PORT = G_MQTT_PORT
        self.MQTT_TOPIC = G_MQTT_TOPIC

        # algunas definiciones
        self.mutex = threading.Lock()
        self.running = False
        self.vframe = None

        # operaciones GUI en el thread principal
        self.evtShowImage, EVT_SHOW_IMAGE = wx.lib.newevent.NewEvent()
        self.Bind( EVT_SHOW_IMAGE, self._UpdateImage )

        # levantamos la GUI
        self.mainFrame = wxMainFrame.MainFrame( parent=None )
        self.mainFrame.SetDoubleBuffered( True )
        self.mainFrame.Bind( wx.EVT_CLOSE, self.OnClose )
        self.mainFrame.Bind( wx.EVT_MENU, self.OnSalir, id=wxMainFrame.ID_SALIR )
        self.mainFrame.Send.Bind( wx.EVT_TOGGLEBUTTON, self.OnSend )
        self.mainFrame.Show()

        # levantamos las tareas
        self.running = True
        self.tCaptureVideo = threading.Thread( target=self._TCaptureVideo, args=(), name="_TCaptureVideo" )
        self.tSendVideo = threading.Thread( target=self._TSendVideo, args=( ), name="_TSendVideo" )
        self.tCaptureVideo.start()
        self.tSendVideo.start()

        return True

    def OnSalir( self, event ):
        self.mainFrame.Close()

    def OnClose( self, event ):
        # terminamos las tareas
        self.running = False
        self.tCaptureVideo.join()
        self.tSendVideo.join()

        # propagamos la salida
        event.Skip()

    def OnSend( self, event ):
        obj = event.GetEventObject()
        if( obj.GetValue() ):
            obj.SetLabel( 'Pausar' )
        else:
            obj.SetLabel( 'Transmitir' )

    def _TCaptureVideo( self ):
        # abrimos dispositivo de captura
        cap = cv2.VideoCapture( self.DEVICE )

        # dimensiones de la captura
        if( C_IS_CV3 ):
            cap.set( cv2.CAP_PROP_FRAME_HEIGHT, self.imgH )
            cap.set( cv2.CAP_PROP_FRAME_WIDTH, self.imgW )
        else:
            cap.set( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.imgH )
            cap.set( cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.imgW )

        # iniciamos la captura
        t1 = 0.
        while( self.running ):
            # 1. internamente hay un buffer que puede producir lags a bajos FPS
            # 2. poca luz genera demoras en la decodificación
            ret, img = cap.read()
            if( ret ):
                # lo dejamos disponible para la tarea que envia
                self.mutex.acquire()
                self.vframe = img.copy()
                self.mutex.release()

                # lo mostramos
                t2 = time.time()
                evt = self.evtShowImage( panel=self.mainFrame.CaptureImage, img=img, fps=1./(t2-t1))
                wx.PostEvent( self, evt )
                t1 = t2
            time.sleep( 0.001 )

        # liberamos el dispositivo de captura
        cap.release()
        print( 'Cerrando Capture' )

    def _TSendVideo( self ):
        mqtt_client = paho.Client()
        mqtt_client.connect( self.MQTT_SERVER, self.MQTT_PORT )
        mqtt_client.loop_start()

        t1 = 0.
        while( self.running ):
            if( self.mainFrame.Send.GetValue() ):
                cuadros = self.mainFrame.Cuadros.GetValue()
                segundos = self.mainFrame.Segundos.GetValue()
                delay = float(segundos)/float(cuadros)
                t2 = time.time()
                if( t2-t1>=delay ):
                    self.mutex.acquire()
                    img = self.vframe
                    self.mutex.release()

                    if( img is not None ):
                        # lo enviamos
                        data = cv2.imencode( '.jpg', img )[1].tostring()
                        mqtt_client.publish( self.MQTT_TOPIC, data )

                        # lo mostramos
                        evt = self.evtShowImage( panel=self.mainFrame.SendImage, img=img.copy(), fps=1./(t2-t1) )
                        wx.PostEvent( self, evt )
                        t1 = t2
            time.sleep( 0.001 )

        # cerramos la conexion
        mqtt_client.loop_stop()
        print( 'Cerrando Send' )

    def _UpdateImage( self, evt ):
        # los parametros
        panel = evt.panel
        img = evt.img
        fps = evt.fps

        # el tamano de la imagen
        imgH, imgW = img.shape[:2]

        # agregamos los FPS
        cv2.putText( img, "%03.1f FPS" % ( fps ), ( 10, imgH-10 ), cv2.FONT_HERSHEY_SIMPLEX, 1, ( 255, 255, 255 ) )

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

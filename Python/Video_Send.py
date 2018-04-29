# coding: UTF-8
from __future__ import print_function
import time
import cv2
import numpy as np
import paho.mqtt.client as paho
import threading
import sys

import wx
import wx.lib.newevent
import Video_Send_wx as wxMainFrame

G_IS_CV3 = ( cv2.__version__[0] == '3' )
if( G_IS_CV3 ):
    G_IMREAD_COLOR = cv2.IMREAD_COLOR
    G_COLOR_BGR2RGB = cv2.COLOR_BGR2RGB
    G_IMWRITE_JPEG_QUALITY = cv2.IMWRITE_JPEG_QUALITY
else:
    G_IMREAD_COLOR = cv2.CV_LOAD_IMAGE_COLOR
    G_COLOR_BGR2RGB = cv2.cv.CV_BGR2RGB
    G_IMWRITE_JPEG_QUALITY = cv2.cv.CV_IMWRITE_JPEG_QUALITY


#### Cambiar aqui
G_CAP_WIDTH = 320
G_CAP_HEIGHT = 240
####

class MainApp( wx.App ):
    def OnInit( self ):
        # esto vienen de la GUI
        self.CAP_DEVICE = 0
        self.CAP_WIDTH = G_CAP_WIDTH
        self.CAP_HEIGHT = G_CAP_HEIGHT
        self.MQTT_SERVER = ''
        self.MQTT_PORT = 0
        self.MQTT_TOPIC = ''

        # algunas definiciones
        self.mqtt_client = paho.Client()
        self.tx = False
        self.mutex = threading.Lock()
        self.image = None

        # la tarea de captura y envio de frames
        self.tSendVideo = None
        self.running = threading.Event()

        # preparamos la GUI
        self.mainFrame = wxMainFrame.MainFrame( parent=None )
        self.mainFrame.Bind( wx.EVT_CLOSE, self.OnClose )
        self.mainFrame.Bind( wx.EVT_MENU, self.OnSalir, id=wxMainFrame.ID_SALIR )
        self.mainFrame.Device.Bind( wx.EVT_CHOICE, self.OnDevice )
        self.mainFrame.Send.Bind( wx.EVT_TOGGLEBUTTON, self.OnSend )

        # eventos para que las operaciones GUI ocurran en el thread principal
        self.timer = wx.Timer( self )
        self.Bind( wx.EVT_TIMER, self._UpdateImage, self.timer )
        self.timer.Start( 33 )

        # levantamos la GUI
        self.mainFrame.Show()
        return True

        return True

    def OnSalir( self, event ):
        self.mainFrame.Close()

        # propagamos la salida
        event.Skip()

    def OnClose( self, event ):
        # terminamos la tarea
        self.running.clear()
        if( self.tSendVideo is not None ):
            self.tSendVideo.join()
            self.tSendVideo = None

        # quizas estabamos transmitiendo
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

        # propagamos la salida
        event.Skip()

    def OnDevice( self, event ):
        # terminamos la tarea
        self.running.clear()
        if( self.tSendVideo is not None ):
            self.tSendVideo.join()
            self.tSendVideo = None
        self.mainFrame.StatusBar.SetStatusText( '', 0 )

        device = self.mainFrame.Device
        choice = device.GetSelection()
        if( choice != 0 ):
            self.CAP_DEVICE = choice - 1
            self._getGuiParams()
            self.running.set()
            self.tSendVideo = threading.Thread( target=self._TSendVideo, args=(), name='_TSendVideo' )
            self.tSendVideo.start()

    def OnSend( self, event ):
        btnSend = self.mainFrame.Send
        transmit = btnSend.GetValue()
        if( transmit ):
            self.mainFrame.StatusBar.SetStatusText( '', 0 )
            self.mainFrame.Device.Disable()
            self.mainFrame.Server.Disable()
            self.mainFrame.Port.Disable()
            self.mainFrame.Topic.Disable()
            self.mainFrame.JpegQuality.Disable()
            self.mainFrame.Cuadros.Disable()
            self.mainFrame.Segundos.Disable()
            btnSend.Disable()

            self.MQTT_SERVER = self.mainFrame.Server.GetValue()
            self.MQTT_PORT = self.mainFrame.Port.GetValue()
            self.MQTT_TOPIC = self.mainFrame.Topic.GetValue()
            try:
                self.mqtt_client.connect( self.MQTT_SERVER, int( self.MQTT_PORT ) )
                btnSend.SetLabel( 'Pausar' )
                btnSend.Enable()
                self.mqtt_client.loop_start()
                self.tx = True
                return
            except Exception as e:
                self.mainFrame.StatusBar.SetStatusText( repr( e ), 0 )
                btnSend.SetValue( False )
                btnSend.Enable()

        self.tx = False
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        self.mainFrame.Device.Enable()
        self.mainFrame.Server.Enable()
        self.mainFrame.Port.Enable()
        self.mainFrame.Topic.Enable()
        self.mainFrame.JpegQuality.Enable()
        self.mainFrame.Cuadros.Enable()
        self.mainFrame.Segundos.Enable()
        btnSend.SetLabel( 'Transmitir' )

    def _getGuiParams( self ):
        cuadros = self.mainFrame.Cuadros.GetValue()
        segundos = self.mainFrame.Segundos.GetValue()
        self.mutex.acquire()
        self._delay = float(segundos)/float(cuadros)
        self._jpeg_quality = self.mainFrame.JpegQuality.GetValue()
        self.mutex.release()

    def _TSendVideo( self ):
        # abrimos dispositivo de captura
        cap = None
        try:
            cap = cv2.VideoCapture( self.CAP_DEVICE )
            ret, img = cap.read()
            if( not ret ):
                raise ValueError( 'Invalid Device Index' )
        except Exception as e:
            wx.CallAfter( self.mainFrame.StatusBar.SetStatusText, repr( e ), 0 )
            return

        # dimensiones de la imagen
        if( G_IS_CV3 ):
            cap.set( cv2.CAP_PROP_FRAME_HEIGHT, self.CAP_HEIGHT )
            cap.set( cv2.CAP_PROP_FRAME_WIDTH, self.CAP_WIDTH )
        else:
            cap.set( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.CAP_HEIGHT )
            cap.set( cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.CAP_WIDTH )

        wx.CallAfter( self.mainFrame.Send.Enable )

        # iniciamos la captura
        t1 = 0.
        while( self.running.isSet() ):
            try:
                # 1. se captura rapido pues internamente hay un buffer que puede producir lags a bajos FPS
                # 2. poca luz genera demoras en la decodificación
                ret, img = cap.read()
                if( ret ):
                    t2 = time.time()
                    self.mutex.acquire()
                    delay = self._delay
                    self.mutex.release()
                    if( ( t2 - t1 ) >= delay ):
                        _, data = cv2.imencode( '.jpg', img, (G_IMWRITE_JPEG_QUALITY, self._jpeg_quality ) )
                        self.mutex.acquire()
                        self.image = data
                        self.mutex.release()
                        if( self.tx ):
                            self.mqtt_client.publish( self.MQTT_TOPIC, data.tostring() )
                        t1 = t2
            except Exception as e:
                print( repr( e ) )
            wx.CallAfter( self._getGuiParams )
            time.sleep( 0.010 )

        # liberamos el dispositivo de captura
        cap.release()

        wx.CallAfter( self.mainFrame.Send.Disable )

        print( 'Capture: Finalizado' )
        sys.stdout.flush()

    def _UpdateImage( self, evt ):
        self.mutex.acquire()
        img = self.image
        self.image = None
        self.mutex.release()
        if( img is None ):
            return

        try:
            # la procesamos
            data = np.fromstring( img, np.uint8 )
            img = cv2.imdecode( data, G_IMREAD_COLOR )

           # donde desplegar
            panel = self.mainFrame.CaptureImage

            # la mostramos ajustado a la ventana
            img = cv2.cvtColor( img, G_COLOR_BGR2RGB )
            w, h = panel.Size
            if( w>0 and h>0 ):
                img = cv2.resize( img, (w, h) )
                bmp = wx.Bitmap.FromBuffer( w, h, img )
                dc = wx.ClientDC( panel )
                dc.DrawBitmap( bmp, 0, 0 )
                del dc
        except Exception as e:
            pass


# Show time
myApp = MainApp( False )
myApp.MainLoop()

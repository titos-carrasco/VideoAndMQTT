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
import Video_Recv_wx as wxMainFrame

G_IS_CV3 = ( cv2.__version__[0] == '3' )
if( G_IS_CV3 ):
    G_IMREAD_COLOR = cv2.IMREAD_COLOR
    G_COLOR_BGR2RGB = cv2.COLOR_BGR2RGB
else:
    G_IMREAD_COLOR = cv2.CV_LOAD_IMAGE_COLOR
    G_COLOR_BGR2RGB = cv2.cv.CV_BGR2RGB

class MainApp( wx.App ):
    def OnInit( self ):
        # esto vienen de la GUI
        self.MQTT_SERVER = ''
        self.MQTT_PORT = 0
        self.MQTT_TOPIC = ''

        # algunas definiciones
        self.mqtt_client = paho.Client()
        self.mqtt_client.on_connect = self._mqtt_on_connect
        self.mqtt_client.on_message = self._mqtt_on_message
        self.mutex = threading.Lock()
        self.image = None

        # preparamos la GUI
        self.mainFrame = wxMainFrame.MainFrame( parent=None )
        self.mainFrame.Bind( wx.EVT_CLOSE, self.OnClose )
        self.mainFrame.Bind( wx.EVT_MENU, self.OnSalir, id=wxMainFrame.ID_SALIR )
        self.mainFrame.Action.Bind( wx.EVT_TOGGLEBUTTON, self.OnAction )

        # eventos para que las operaciones GUI ocurran en el thread principal
        self.timer = wx.Timer( self )
        self.Bind( wx.EVT_TIMER, self._UpdateImage, self.timer )
        self.timer.Start( 33 )

        # levantamos la GUI
        self.mainFrame.Show()
        return True

    def OnSalir( self, event ):
        self.mainFrame.Close()

        # propagamos la salida
        event.Skip()

    def OnClose( self, event ):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

        # propagamos la salida
        event.Skip()

    def OnAction( self, event ):
        btnAction = event.GetEventObject()
        receive = btnAction.GetValue()
        if( receive ):
            self.mainFrame.StatusBar.SetStatusText( '', 0 )
            self.mainFrame.Server.Disable()
            self.mainFrame.Port.Disable()
            self.mainFrame.Topic.Disable()
            btnAction.Disable()

            self.MQTT_SERVER = self.mainFrame.Server.GetValue()
            self.MQTT_PORT = self.mainFrame.Port.GetValue()
            self.MQTT_TOPIC = self.mainFrame.Topic.GetValue()
            try:
                self.mqtt_client.connect( self.MQTT_SERVER, int( self.MQTT_PORT ) )
                btnAction.SetLabel( 'Detener' )
                btnAction.Enable()
                self.mqtt_client.loop_start()
                return
            except Exception as e:
                self.mainFrame.StatusBar.SetStatusText( str( e ), 0 )
                btnAction.SetValue( False )
                btnAction.Enable()

        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

        self.mainFrame.Server.Enable()
        self.mainFrame.Port.Enable()
        self.mainFrame.Topic.Enable()
        btnAction.SetLabel( 'Iniciar' )

    def _mqtt_on_message( self, client, userdata, message ):
        self.mutex.acquire()
        self.image = message.payload
        self.mutex.release()

    def _mqtt_on_connect( self, client, userdata, flags, rc ):
        # nos suscribimos al topico que nos interesa
        try:
            client.subscribe( self.MQTT_TOPIC )
        except Exception as e:
            wx.CallAfter( self.mainFrame.StatusBar.SetStatusText, str( e ), 0 )

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
            panel = self.mainFrame.RecvImage

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

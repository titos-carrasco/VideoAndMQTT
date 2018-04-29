# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Apr 18 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

ID_SALIR = 1000
ID_ACERCA_DE = 1001

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Video Capture&Send", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.Archivo = wx.Menu()
		self.Salir = wx.MenuItem( self.Archivo, ID_SALIR, u"Salir", wx.EmptyString, wx.ITEM_NORMAL )
		self.Archivo.Append( self.Salir )
		
		self.m_menubar1.Append( self.Archivo, u"Archivo" ) 
		
		self.Ayuda = wx.Menu()
		self.AcercaDe = wx.MenuItem( self.Ayuda, ID_ACERCA_DE, u"Acerca de...", wx.EmptyString, wx.ITEM_NORMAL )
		self.Ayuda.Append( self.AcercaDe )
		
		self.m_menubar1.Append( self.Ayuda, u"Ayuda" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		self.StatusBar = self.CreateStatusBar( 1, 0|wx.SUNKEN_BORDER, wx.ID_ANY )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 4, 2, 4 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Dispositivo:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		DeviceChoices = [ u"Seleccione Dispositivo", u"0 (320x240)", u"1 (320x240)", u"2 (320x240)", u"3 (320x240)", u"4 (320x240)", u"5 (320x240)", u"6 (320x240)", u"7 (320x240)", u"8 (320x240)", u"9 (320x240)" ]
		self.Device = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, DeviceChoices, 0 )
		self.Device.SetSelection( 0 )
		fgSizer1.Add( self.Device, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"Servidor:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		fgSizer1.Add( self.m_staticText31, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		self.Server = wx.TextCtrl( self, wx.ID_ANY, u"broker.hivemq.com", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.Server, 0, wx.EXPAND, 5 )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Puerta:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		self.Port = wx.TextCtrl( self, wx.ID_ANY, u"1883", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.Port, 0, 0, 5 )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Tópico:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		self.Topic = wx.TextCtrl( self, wx.ID_ANY, u"demos/rcr/video", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.Topic, 0, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Calidad Imagen:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		fgSizer1.Add( self.m_staticText7, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		self.JpegQuality = wx.Slider( self, wx.ID_ANY, 50, 1, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		fgSizer1.Add( self.JpegQuality, 0, wx.EXPAND, 0 )
		
		
		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( fgSizer1, 0, wx.ALL|wx.EXPAND, 4 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Cuadros = wx.SpinCtrl( self, wx.ID_ANY, u"5", wx.DefaultPosition, wx.Size( -1,-1 ), wx.SP_ARROW_KEYS|wx.SIMPLE_BORDER, 1, 30, 5 )
		bSizer6.Add( self.Cuadros, 0, 0, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Cuadro(s) en", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText3.Wrap( -1 )
		bSizer6.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )
		
		self.Segundos = wx.SpinCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( -1,-1 ), wx.SP_ARROW_KEYS|wx.SIMPLE_BORDER, 1, 10, 1 )
		bSizer6.Add( self.Segundos, 0, 0, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Segundo(s)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer6.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )
		
		self.Send = wx.ToggleButton( self, wx.ID_ANY, u"Transmitir", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.Send.Enable( False )
		
		bSizer6.Add( self.Send, 0, 0, 2 )
		
		
		bSizer1.Add( bSizer6, 0, wx.ALIGN_CENTER|wx.ALL, 4 )
		
		self.CaptureImage = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 320,240 ), wx.TAB_TRAVERSAL )
		self.CaptureImage.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer1.Add( self.CaptureImage, 0, wx.ALIGN_CENTER|wx.ALL, 4 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	


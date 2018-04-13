# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Apr 10 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
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
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.Archivo = wx.Menu()
		self.Salir = wx.MenuItem( self.Archivo, ID_SALIR, u"Salir", wx.EmptyString, wx.ITEM_NORMAL )
		self.Archivo.AppendItem( self.Salir )
		
		self.m_menubar1.Append( self.Archivo, u"Archivo" ) 
		
		self.Ayuda = wx.Menu()
		self.AcercaDe = wx.MenuItem( self.Ayuda, ID_ACERCA_DE, u"Acerca de...", wx.EmptyString, wx.ITEM_NORMAL )
		self.Ayuda.AppendItem( self.AcercaDe )
		
		self.m_menubar1.Append( self.Ayuda, u"Ayuda" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Cuadros = wx.SpinCtrl( self, wx.ID_ANY, u"5", wx.DefaultPosition, wx.Size( -1,-1 ), wx.SP_ARROW_KEYS|wx.SIMPLE_BORDER, 1, 30, 5 )
		bSizer6.Add( self.Cuadros, 0, wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Cuadro(s) en", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText3.Wrap( -1 )
		bSizer6.Add( self.m_staticText3, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.Segundos = wx.SpinCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( -1,-1 ), wx.SP_ARROW_KEYS|wx.SIMPLE_BORDER, 1, 10, 1 )
		bSizer6.Add( self.Segundos, 0, wx.ALL, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Segundo(s)      ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer6.Add( self.m_staticText2, 0, wx.ALIGN_BOTTOM|wx.ALL|wx.EXPAND, 5 )
		
		self.Send = wx.ToggleButton( self, wx.ID_ANY, u"Transmitir", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer6.Add( self.Send, 0, wx.ALL|wx.EXPAND, 2 )
		
		
		bSizer1.Add( bSizer6, 0, wx.ALIGN_RIGHT, 0 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.CaptureImage = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
		self.CaptureImage.SetMinSize( wx.Size( 320,263 ) )
		
		bSizer3.Add( self.CaptureImage, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer3.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 10 )
		
		self.SendImage = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
		self.SendImage.SetMinSize( wx.Size( 320,263 ) )
		
		bSizer3.Add( self.SendImage, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	


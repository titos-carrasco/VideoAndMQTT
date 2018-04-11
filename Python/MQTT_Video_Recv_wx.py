# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Video Receive&View", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )
		
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
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.RecvImage = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
		self.RecvImage.SetMinSize( wx.Size( 320,263 ) )
		
		bSizer1.Add( self.RecvImage, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		self.m_statusBar1 = self.CreateStatusBar( 1, 0, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	


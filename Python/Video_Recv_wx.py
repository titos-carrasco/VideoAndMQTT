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
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Video Receive&View", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )
        
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
        
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        
        fgSizer2 = wx.FlexGridSizer( 0, 2, 2, 2 )
        fgSizer2.AddGrowableCol( 1 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Servidor:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        fgSizer2.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
        
        self.Server = wx.TextCtrl( self, wx.ID_ANY, u"test.mosquitto.org", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        fgSizer2.Add( self.Server, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Puerta:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        fgSizer2.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
        
        self.Port = wx.TextCtrl( self, wx.ID_ANY, u"1883", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.Port, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Tópico:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        fgSizer2.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
        
        self.Topic = wx.TextCtrl( self, wx.ID_ANY, u"rcr/video", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.Topic, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
        
        
        bSizer2.Add( fgSizer2, 1, wx.ALL|wx.EXPAND, 3 )
        
        self.Action = wx.ToggleButton( self, wx.ID_ANY, u"Iniciar", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.Action, 0, wx.ALL|wx.EXPAND, 3 )
        
        
        bSizer1.Add( bSizer2, 0, wx.ALL|wx.EXPAND, 3 )
        
        self.RecvImage = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 320,240 ), wx.TAB_TRAVERSAL )
        self.RecvImage.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
        
        bSizer1.Add( self.RecvImage, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.FIXED_MINSIZE, 2 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        bSizer1.Fit( self )
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:46:51 2017

@author: gbonnet
"""
def GateOnLiveSingletCells(fcsfilename):

    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets  import RectangleSelector
    import fcsparser
    import pandas as pd


    def line_select_callback(eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        print(" The button you used were: %s %s" % (eclick.button, erelease.button))


    def toggle_selector(event):
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and toggle_selector.RS.active:
            print(' RectangleSelector deactivated.')
            toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not toggle_selector.RS.active:
            print(' RectangleSelector activated.')
            toggle_selector.RS.set_active(True)

    meta,df=fcsparser.parse(fcsfilename, reformat_meta=True)

    data=df.iloc[:,2:-4]

    CyTOF_channels=[]

    for met in meta:
        if (met.find('$P')==0) & (met.find('$PAR')==-1):
            if ((meta[met].find('_')>-1)&~(meta[met].find('Env')>-1)&~(meta[met].find('EQ4')>-1)):
                CyTOF_channels.append(meta[met])

    marker=[]
    for cc in CyTOF_channels:
        marker.append(cc[cc.find('_')+1:])

    channels=[]
    for mark in CyTOF_channels:
        if mark.find('89Y')>-1:
            channels.append('Y89Di')
        else:
            if mark.find('127I')>-1:
                channels.append('I127Di')
            else:
                channels.append(mark[mark.find('_')-2:mark.find('_')]+mark[0:mark.find('_')-2]+'Di')  
    
    Bead_channels='Ce140Di'
    DNA1_channels='Ir191Di'
    CD45_channels='Y89Di'           
    Cisplatin_channels='Pt195Di'     

    fig1, ax1 = plt.subplots()
    ax1.plot(np.arcsinh(data[Bead_channels][:1000]),np.arcsinh(data[Cisplatin_channels][:1000]),'.k',markersize=1,label='All events')        
    ax1.set_xlabel('EQ4_beads (Ce140)')
    ax1.set_ylabel('Cisplatin (Pt195)')
    plt.title(fcsfilename[fcsfilename.rfind('/')+1:])

    toggle_selector.RS = RectangleSelector(ax1, line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()
    Bead_gateout=np.max(toggle_selector.RS.corners[0])
    Cisplatin_gateout=np.max(toggle_selector.RS.corners[1])
    plt.close(fig1)
    #%%
    fig2=plt.figure(num=2,figsize=(10,5))
    ax1=fig2.add_subplot(121)
    ax1.plot(np.arcsinh(data[Bead_channels]),np.arcsinh(data[Cisplatin_channels]),'.k',markersize=1,label='All events')        
    ax1.set_xlabel('EQ4_beads (Ce140)')
    ax1.set_ylabel('Cisplatin (Pt195)')
    plt.title(fcsfilename[fcsfilename.rfind('/')+1:])
    Bead_gateout=np.max(toggle_selector.RS.corners[0])
    Cisplatin_gateout=np.max(toggle_selector.RS.corners[1])

    LiveCells=(np.arcsinh(data[Bead_channels])<Bead_gateout) & (np.arcsinh(data[Cisplatin_channels])<Cisplatin_gateout)
    ax1.plot(np.arcsinh(data[Bead_channels])[LiveCells],np.arcsinh(data[Cisplatin_channels])[LiveCells],'.r',markersize=1,label='Live cells')  
    plt.legend(loc=0) 

    print(Bead_gateout)
    print(Cisplatin_gateout)

    ax2=fig2.add_subplot(122)
    ax2.plot(np.arcsinh(data[DNA1_channels])[LiveCells][:50000],np.arcsinh(data[CD45_channels])[LiveCells][:50000],'.r',markersize=1,label='Live cells')  
    ax2.set_xlabel('DNA1 (Ir191)')
    ax2.set_ylabel('CD45 (Y89)')
    toggle_selector.RS = RectangleSelector(ax2, line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()

    #%%

    DNA1_min=np.min(toggle_selector.RS.corners[0])
    DNA1_max=np.max(toggle_selector.RS.corners[0])
    CD45_min=np.min(toggle_selector.RS.corners[1])
    CD45_max=np.max(toggle_selector.RS.corners[1])
    
    
    SingletLive=(np.arcsinh(data[Bead_channels])<Bead_gateout) \
                & (np.arcsinh(data[Cisplatin_channels])<Cisplatin_gateout) \
                & (np.arcsinh(data[DNA1_channels])<DNA1_max)& (np.arcsinh(data[DNA1_channels])>DNA1_min)\
                & (np.arcsinh(data[CD45_channels])<CD45_max)& (np.arcsinh(data[CD45_channels])>CD45_min)
  
    
    fig2=plt.figure(num=2,figsize=(10,5))
    ax1=fig2.add_subplot(121)
    ax1.plot(np.arcsinh(data[Bead_channels]),np.arcsinh(data[Cisplatin_channels]),'.k',markersize=1,label='All events')        
    ax1.set_xlabel('EQ4_beads (Ce140)')
    ax1.set_ylabel('Cisplatin (Pt195)')
    ax2=fig2.add_subplot(122)
    ax2.plot(np.arcsinh(data[DNA1_channels])[LiveCells],np.arcsinh(data[CD45_channels])[LiveCells],'.r',markersize=1,label='Live cells')  
    ax2.set_xlabel('DNA1 (Ir191)')
    ax2.set_ylabel('CD45 (Y89)')

    ax2.plot(np.arcsinh(data[DNA1_channels])[SingletLive],np.arcsinh(data[CD45_channels])[SingletLive],'.b',markersize=1,label='Singlet / Live cells')  
    plt.legend(loc=0) 
    ax1.plot(np.arcsinh(data[Bead_channels])[SingletLive],np.arcsinh(data[Cisplatin_channels])[SingletLive],'.b',markersize=1,label='Singlet / Live cells') 
    plt.legend(loc=0)
    plt.title(fcsfilename[fcsfilename.rfind('/')+1:])
    plt.show()


    df=pd.DataFrame(data[channels][SingletLive])
    df.columns=marker
    return df


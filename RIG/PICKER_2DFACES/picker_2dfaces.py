# -*- coding: utf-8 -*-
# @Date:   2017-10-10T11:13:42-03:00
# @Last modified time: 2017-11-14T18:56:21-03:00
import random
import re
import sys
from operator import itemgetter
from collections import OrderedDict

from functools import partial
import os
import UTILITIES #necesaria para funciones de diccionario y archivos
reload(UTILITIES)
import pickerBotonera#Necesaria para el picker de controles
reload(pickerBotonera)
import maya.cmds as cmds
import pymel.core as pm

#path = r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\UTIL'
#
# if not path in sys.path:
#     sys.path.append(path)
# try:
#     import UTILITIES
#     reload(UTILITIES)
# except (RuntimeError, TypeError, NameError, IOError):
#     print 'NO SE PUDO IMPORTAR EL MODULO'


def setKeyNow(obj='C_head_01_CTRL', attr='r_ojo'):
    currentTimeX = cmds.currentTime(query=True)
    cmds.setKeyframe(obj, attribute=attr, t=[currentTimeX, currentTimeX])
    cmds.keyTangent(obj, at=attr, itt='linear', ott='linear')

def rotLayer(attr='l_ojo', ctr='C_head_01_CTRL',barraUI=None ,*args):
    if barraUI:
        attr = attr + '_ROT'
        if cmds.objExists(ctr + '.' + attr):
            val=cmds.floatSlider(barraUI,q=True,value=True)
            cmds.setAttr(ctr + '.' + attr, val)
            setKeyNow(ctr, attr)
        else:
            cmds.warning('No existe el atributo ',attr)

def resetSlide(attr,controlAttributos,value,slider,*args):
    cmds.floatSlider(slider,e=True,value=value)
    rotLayer(attr,controlAttributos,slider)

# Ocultara el layer en maya.
def displayLayer(attr='l_ojo', ctr='L_EYE_PUPILA_CNT', *args):

    attr = attr + '_VIS'
    if cmds.objExists(ctr + '.' + attr):
        currentVal = cmds.getAttr(ctr + '.' + attr)
        if currentVal:
            cmds.setAttr(ctr + '.' + attr, 0)
            setKeyNow(ctr, attr)

        else:
            cmds.setAttr(ctr + '.' + attr, 1)
            setKeyNow(ctr, attr)


def getFrame(val=0, attr='r_ojo', ctr='L_EYE_PUPILA_CNT', *args):
    # Con esta funcion pregunto si existe el control que le estoy pasando por
    # argumento
    if cmds.objExists(ctr + '.' + attr):
        currentVal = cmds.getAttr(ctr + '.' + attr)
        # Devuelve el evento que preciono
        mods = cmds.getModifiers()
        setKeyNow(ctr, attr)
        # pregunto si se preciono y es shift y agrego a la seleccion
        if (mods & 1) > 0:#Shift
            if 'l_' in attr:
                attr = 'r_' + attr.split('l_')[1]
                cmds.setAttr(ctr + '.' + attr, val)
                setKeyNow(ctr, attr)
            elif 'r_' in attr:
                attr = 'l_' + attr.split('r_')[1]
                cmds.setAttr(ctr + '.' + attr, val)
                setKeyNow(ctr, attr)
            else:
                cmds.warning(
                    'No contiene el otro lado de la misma imagen nombrada L_ o R_')
        # de lo contrario solo selecciono
        else:
            cmds.setAttr(ctr + '.' + attr, val)
            setKeyNow(ctr, attr)
    else:
        cmds.warning('No existe el atributo o variable ' + attr +
                     ', en el control ' + ctr + ' o necesita de un namespace.')

def ordenarLeftRighMidDiccionario(directorios={}):
    newDic=dict()
    for key,value in directorios.items():
        name = key.split('\\')[-1]
        if 'l_' in name: newDic.setdefault(key,[]).append(value)
        elif 'r_' in name:  newDic.setdefault(key,[]).append(value)
        else: newDic.setdefault(key,[]).append(value)
    #sorted(newDic)
    return newDic

def colapsador(*args):
    global uis
    onOff=cmds.frameLayout(uis['scrolles'][0],q=True,collapse=True)
    for v in uis['scrolles']:
        cmds.frameLayout(v,e=True,collapse=not onOff)
# Definimos una interfas grafica para el usuario
def botonesUI(directorios='', nameSpace='', sizeButtons=100, parents='', controlAttributos='L_EYE_PUPILA_CNT',heightW=800):
    global uis
    uis=dict()#contenedor de gui para colapsar


    # Creo una fila con 3 columnos grandes
    cantButColumFila=8
    #Paletas de colores
    color1 = random.uniform(0.0, 1.0), random.uniform(
        0.0, 1.0), random.uniform(0.0, 1.0)
    color2 = [0.3, 0.3, 0.3]
    color3 = [0.29,0.58,0.96]

    columMaster=cmds.columnLayout(adjustableColumn=True,parent=parents)
    # Contengo todo en un solo scroll grande
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if os.path.isfile(dir_path+'\cof_img.xpm'):
        cmds.symbolButton( image=dir_path+'\cof_img.xpm', width=122, height=35, backgroundColor=[0,0,0],
                          annotation=('www.cofcofstudios.com'), command="cmds.launch(web='http://cofcofstudios.com')",parent=columMaster)
    else:
        cmds.image(w = 122, h = 35,backgroundColor=[0,0,0],parent=columMaster)

    rowGeneral2 = cmds.rowLayout(numberOfColumns=2,height=heightW, adjustableColumn=True ,columnWidth2=(sizeButtons * cantButColumFila,470), columnAttach=[(1, 'both', 0),(2, 'both', 0)])
    fm1=cmds.frameLayout(label='CONTROLES', bgc=[0,0,0],parent=rowGeneral2)
    columna1=cmds.columnLayout(adjustableColumn=True,parent=fm1)
    cmds.channelBox(maxHeight=heightW/3,parent=columna1)

    f2=cmds.frameLayout(label='FACIALES',bgc=[0,0,0],parent=rowGeneral2)
    btnc=cmds.button(l='Colapsar Todas',command=colapsador)#colapsador de ui
    scroll = cmds.scrollLayout( height=heightW-50,minChildWidth=500,parent=f2)

    rowGeneral3 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(150,150, 155),
                                adjustableColumn3=1, columnAttach=[(1, 'left', 2),(2, 'both', 2), (3, 'both', 2)])
    colRight = cmds.columnLayout(adjustableColumn=True,parent=rowGeneral3)
    colMid = cmds.columnLayout(adjustableColumn=True,parent=rowGeneral3)
    colLeft = cmds.columnLayout(adjustableColumn=True,columnOffset=['right',5],parent=rowGeneral3)


    directorios = sorted_x = OrderedDict(sorted(directorios.items(), key=itemgetter(1)))#Ordena los value del diccionario para que muestre ordenada la lista
    #directorios = ordenarLeftRighMidDiccionario(directorios)

    # creo los botones recoriendo el diccionario que creamos
    def columnForFolderUI(botonesArray=[],sideFace='l_ojo', controlAttributos='L_EYE_PUPILA_CNT',sideParent=None):
        # Creo una columna para los botones columnAttach=[(1, 'both', 0),(2, 'right', 0)],
        cl1 = cmds.columnLayout(adjustableColumn=True,columnAttach=['left', 0],parent=sideParent)
        frameIn = cmds.frameLayout(label=sideFace.upper(), collapsable=True, bgc=color3, parent=cl1)
        cl2 = cmds.columnLayout(cal='left', cat=['both', 0], columnOffset=[ 'left', 0],  adjustableColumn=True, parent=frameIn)
        cmds.button(label='DisplayLayer', command=partial( displayLayer, sideFace, controlAttributos))
        cmds.rowColumnLayout(numberOfRows=1,adjustableColumn=True)
        barraRotacion=cmds.floatSlider('barra-'+sideFace,min=-180, max=180, value=0, step=1)
        cmds.floatSlider(barraRotacion,edit=True,changeCommand=partial(rotLayer, sideFace, controlAttributos,barraRotacion),dragCommand=partial( rotLayer, sideFace, controlAttributos,barraRotacion))
        cmds.button( label ='R', bgc=[0.5,0.5,0.4],height=30,width=30,command=partial(resetSlide,sideFace,controlAttributos,0,barraRotacion),annotation='Resetea la rotacion de la capa.')
        cmds.setParent( '..' )
        f3=cmds.frameLayout(  label='Expresiones', collapsable=True, collapse=False)
        scroll2 = cmds.scrollLayout( childResizable=True,height=110)
        rcl1=cmds.rowColumnLayout(numberOfRows=3, bgc=color2)
        uis.setdefault('scrolles', []).append(frameIn)
        uis.setdefault('scrolles', []).append(f3)



        # Para diferenciar las carpeas o frames le pongo diferentes colores
        # r,g,b=random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)
        # creo por cada file un boton
        for ctrl in botonesArray:
            # valFrame=[s.zfill(2) for s in re.findall(r'\b\d+\b', img)]
            val = [int(s) for s in re.findall(r'\b\d+\b', ctrl)][0]
            nameImg=ctrl
            # Solo si existe algo escrito en la variable nameSpace y si es asi
            # le agrego el nameSpace al control.
            if nameSpace is not '':
                ctrl = nameSpace + ctrl
            # Agrego el boton y la funcion, con el nombre del value del
            # diccionario
            cmds.symbolButton(ctrl, image=key + '\\' + nameImg, width=sizeButtons, height=sizeButtons, backgroundColor=color2,
                              annotation=('Frame Num: '+str(val)+'\n Shift + Click: Lado Opuesto.'), command=partial(getFrame, val, sideFace, controlAttributos))

    #por cada carpeta se creara un contenedor de botones
    for key in directorios:
        # Ordeno los frames dependiendo de la letra que contengan las carpetas
        sideFace = key.split('\\')[-1]
        if sideFace in ['l_parpado_sup','l_ojo','l_pupila','l_parpado_inf','l_cachete','l_extras']:
            columnForFolderUI(directorios[key], sideFace, controlAttributos, colLeft)
        elif sideFace in ['r_parpado_sup','r_ojo','r_pupila','r_parpado_inf','r_cachete','r_extras']:
            columnForFolderUI(directorios[key], sideFace, controlAttributos, colRight)
        elif sideFace in ['boca','a_diente','b_diente','lengua','extras']:
            columnForFolderUI(directorios[key], sideFace, controlAttributos, colMid)


    #cmds.button(btnc,e=True,command=colapsador(uis))
    return [columna1,uis,heightW,]


def UI(charName='MILO', directorios={}, nameSpace='', sizeButtons=60, controlAttributo='L_EYE_PUPILA_CNT'):
    # variable que contiene el nombre de dockControl
    WorkspaceName = '2DPICKER_UI-> ' + charName
    # Pregunto si existe la ventana workspaceControl y si existe la borro
    # antes de crearla nuevamente.

    if cmds.workspaceControl(WorkspaceName, exists=True): cmds.deleteUI(WorkspaceName)
    heightW=800
    # ejecuto funcion de interfas y la guardo en un dock
    cmds.workspaceControl(WorkspaceName, initialHeight=heightW, initialWidth=515, floating=True,
                          retain=False,  dtm=('right', 1))
    b=botonesUI(directorios, nameSpace, sizeButtons, WorkspaceName, controlAttributo,heightW)
    print 'Se creo la interfaze ', WorkspaceName
    return b




def picker2D(obj, path='c:/coco', rangeV=30, nameUI='MILO', namespace='', sizeButtons=30, ext='png', keyWord='proxy'):
    if namespace:  # si tiene namespace se le agrega al nombre
        obj = namespace + ':' + obj
    if cmds.objExists(obj):
        if os.path.isdir(path):
            # Con esta funcion creo los atributos en el objeto indicado
            UTILITIES.addAttr_FromFolders(obj, path, ext, keyWord, rangeV)

            # Con esta funcion creo la interface dependiendo la cantidad de carpetas y
            # archivos en FACES folder.
            directorios = UTILITIES.dirs_files_dic(path, ext, keyWord)
            # llamo a la funcion la cual ejecuta todo el resto.
            uip=UI(nameUI, directorios, namespace, 30, obj)
            return uip
        else:
            cmds.error('No existe el directorio ', path)
    else:
        cmds.error('No se encontro ', obj)
'''
import maya.cmds as cmds
import pymel.core as pm
import sys
try:
    import picker2dUi.picker_2dfaces as p2dui#Modulo necesario para que funcione todo
    reload(p2dui)
    import picker2dUi.pickerBotonera as btnUi#Necesaria para el picker de controles
    reload(btnUi)
except (RuntimeError, TypeError, NameError, IOError):
    print 'NO SE PUDO IMPORTAR EL MODULO'

#Este es el nombre que le daremos a nuestra interfas el cual tiene que ser diferente por cada personaje
nameUI = 'FANI' #Nombre que utilizara la interface.
nameSpace = '' #NameSpace del personaje.
#lista de controles
controles={'L_EYE':['l_Eye_CNT','l_eyelid_sup_CNT','l_eyelid_inf_CNT','l_extras_CNT','l_pupil_CNT'],
           'R_EYE':['r_Eye_CNT','r_eyelid_sup_CNT','r_eyelid_inf_CNT','r_extras_CNT','r_pupil_CNT'],
           'OTROS':['c_Pupils_CNT','C_Eyes_CNT','extras_CNT','C_hair_02_CTRL','R_hair_02_CTRL'],
           'BOCA':['lengua_CNT','b_diente_CNT','a_diente_CNT','boca_CNT'],
           'CABEZA':['C_head_01_CTRL']}

obj='C_head_01_CTRL' #objeto que contiene los atributos animables.
path = 'O:\EMPRESAS\RIG_FACE2D\PERSONAJES\FANI\FACES' #Carpeta ordenada donde se contiene los arhivos proxys.
rangeVariable=60 #Cantidad maxima de archivos que contiene una carpeta de proxy.
sizeButtons=30 #Tamaño de botonera

pickerUI=p2dui.picker2D(obj,path,rangeVariable,nameUI,nameSpace,sizeButtons)#Funcion que contiene toda la programacion necesaria para la UI
btnUi.botonesUI(controles,nameSpace,[100,20],pickerUI[0])#Picker de controles
'''

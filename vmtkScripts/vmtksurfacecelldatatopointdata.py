#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtksurfacecelldatatopointdata.py,v $
## Language:  Python
## Date:      $Date: 2005/09/14 09:49:59 $
## Version:   $Revision: 1.7 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.


import vtk
import vtkvmtk
import sys

import pypes

vmtksurfacecelldatatopointdata = 'vmtkSurfaceCellDataToPointData'

class vmtkSurfaceCellDataToPointData(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)
        
        self.Surface = None

        self.SetScriptName('vmtksurfacecelldatatopointdata')
        self.SetScriptDoc('convert cell data arrays to point data surface arrays')
        self.SetInputMembers([
            ['Surface','i','vtkPolyData',1,'','the input surface','vmtksurfacereader']
            ])
        self.SetOutputMembers([
            ['Surface','o','vtkPolyData',1,'','the output surface','vmtksurfacewriter']
            ])

    def Execute(self):

        if self.Surface == None:
            self.PrintError('Error: No Surface.')

        cellDataToPointDataFilter = vtk.vtkCellDataToPointData()
        cellDataToPointDataFilter.SetInput(self.Surface)
        cellDataToPointDataFilter.PassCellDataOn()
        cellDataToPointDataFilter.Update()

        self.Surface = cellDataToPointDataFilter.GetPolyDataOutput()

        if self.Surface.GetSource():
            self.Surface.GetSource().UnRegisterAllOutputs()

if __name__=='__main__':
    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()

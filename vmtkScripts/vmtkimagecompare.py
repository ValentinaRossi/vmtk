#!/usr/bin/env python

import sys
import vtk
import vtkvmtk
import pypes

vmtkimagecompare = 'vmtkImageCompare'

class vmtkImageCompare(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)

        self.Image = None
        self.ReferenceImage = None
        self.Method = ''
	self.Tolerance = 1E-8
        self.Result = ''
        self.ResultLog = ''

        self.SetScriptName('vmtkimagecompare')
        self.SetScriptDoc('compares an image against a reference')
        self.SetInputMembers([
            ['Image','i','vtkImageData',1,'','the input image','vmtkimagereader'],
            ['ReferenceImage','r','vtkImageData',1,'','the reference image to compare against','vmtkimagereader'],
            ['Method','method','str',1,'["subtraction","range"]','method of the test'],
            ['Tolerance','tolerance','float',1,'','tolerance for numerical comparisons'],
            ])
        self.SetOutputMembers([
            ['Result','result','bool',1,'','Output boolean stating if images are equal or not'],
            ['ResultLog','log','str',1,'','Result Log']
            ])

    def rangeCompare(self):

        imageRange = self.Image.GetPointData().GetScalars().GetRange()
        referenceRange = self.ReferenceImage.GetPointData().GetScalars().GetRange()
        rangeDiff = (imageRange[0] - referenceRange[0], imageRange[1] - referenceRange[1])

        self.PrintLog('Image Range: '+ str(imageRange))
        self.PrintLog('Reference Image Range: '+ str(referenceRange))
        self.PrintLog('Range Difference: '+ str(rangeDiff))

        if max([abs(d) for d in rangeDiff]) < self.Tolerance:
            return True
 
        return False

    def subtractionCompare(self):

        imagePoints = self.Image.GetNumberOfPoints()
        referencePoints = self.ReferenceImage.GetNumberOfPoints()

        self.PrintLog('Image Points: ' + str(imagePoints))
        self.PrintLog('Reference Image Points: ' + str(referencePoints))

        if abs(imagePoints - referencePoints) > 0 :
            self.ResultLog = 'Uneven NumberOfPoints'
            return False
            
        imageScalarType = self.Image.GetScalarType()
        referenceScalarType = self.ReferenceImage.GetScalarType()
        minScalarType = min(imageScalarType,referenceScalarType)
        self.Image.SetScalarType(minScalarType) 
        self.ReferenceImage.SetScalarType(minScalarType) 

        imageMath = vtk.vtkImageMathematics()
        imageMath.SetInput1(self.Image) 
        imageMath.SetInput2(self.ReferenceImage) 
        imageMath.SetOperationToSubtract()
        imageMath.Update()
        differenceImage = imageMath.GetOutput()
        differenceRange = differenceImage.GetPointData().GetScalars().GetRange()

        self.PrintLog('Difference Range: ' + str(differenceRange))
 
        if max([abs(d) for d in differenceRange]) < self.Tolerance:
            return True
        
        return False

    def Execute(self):

        if not self.Image:
            self.PrintError('Error: No image.')
        if not self.ReferenceImage:
            self.PrintError('Error: No reference image.')
        if not self.Method:
            self.PrintError('Error: No method.')        
        
        if (self.Method == 'subtraction'):
            self.Result = self.subtractionCompare()
        elif (self.Method == 'range'):
            self.Result = self.rangeCompare()
        
if __name__=='__main__':
    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()

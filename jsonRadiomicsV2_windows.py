# -*- coding: utf-8 -*-
"""
    Program: discoveryRadiomics
    file name: jsonradiomics.py
    date of creation: 2017-06-28 by LiuHui
    date of modification: 2018-03-31
    Author: Chunbo Liu (cbliu@12sigma.com)
    change History: 
    1.support the CAD result of  SigmaLU 0.5.6
    2.import latest pyradiomics 1.3.0
    3.can support all of the filters
"""
import os
import sys
import csv
import re
import json
import argparse
from collections import OrderedDict
import numpy, ijson, six
import SimpleITK as sitk

import scipy
from scipy import optimize
import skimage
import trimesh

from radiomics import firstorder, glcm, glrlm, glszm, shape, ngtdm,gldm,imageoperations
# from sigma.base import get_current_config
basic_featuresList=["Firstorder","Shape","Glcm","Glrlm","Glszm","Ngtdm","Gldm"]
filters_List = ["wavelet","Log","Square","SquareRoot","Logarithm","Exponential","Gradient","LocalBinaryPattern2D","LocalBinaryPattern3D"]
# ------------------------------------------------------------------------------
# resampling the sitkImages with origin aligned
def resample_sitkImage(sitkImage, newSpacing):
    """
    :param sitkImage:
    :param newSpacing:
    :return:
    """
    if sitkImage == None: return None
    oldSize = sitkImage.GetSize()
    oldSpacing = sitkImage.GetSpacing()
    newSize = (int(oldSize[0]*oldSpacing[0]/newSpacing[0]), \
               int(oldSize[1]*oldSpacing[1]/newSpacing[1]), \
              int(oldSize[2]*oldSpacing[2]/newSpacing[2]))
    transform = sitk.Transform()
    return sitk.Resample(sitkImage, newSize, transform, sitk.sitkLinear, sitkImage.GetOrigin(), \
                         newSpacing, sitkImage.GetDirection(), 0, sitkImage.GetPixelID())

def calculateRadiomicsFromJson(niiFile, jsonFile,wavelet,LoG,Square,SquareRoot,Logarithm,\
                Exponential,Gradient,LocalBinaryPattern2D,LocalBinaryPattern3D):
    sitkImageParent = sitk.ReadImage(niiFile)
    direction = sitkImageParent.GetDirection()
    origin = sitkImageParent.GetOrigin()
    spacing = sitkImageParent.GetSpacing()
    # processing json
    nodules = {}   
    parameterList = ["xBegin","yBegin","zBegin","DimInPixelX","DimInPixelY","DimInPixelZ",\
                     "sliceMask"]
    with open(jsonFile,mode='r') as f: 
        json_Data = json.load(f)
        nodule_List = json_Data.get("Nodules",None)
        if not nodule_List:
            print("Error!NO DATA IN json")
            return
        for subNodule,subVal in nodule_List.items():
            if str(subNodule) == 'count' or str(subNodule) == 'version' :
                continue
            # print("subNodule=",subNodule)
            # print("subVal=",subVal)
            label = subVal.get("Label",None)
            if not label:
                print("ERROR:Nodule No Label Info")
                return 
            nodules[label]={}
            nodules[label]['label'] = label
            nodules[label]['sliceMask'] = ''
            for arg in parameterList:
                if arg in ["DimInPixelX","DimInPixelY","DimInPixelZ"]:
                    nodules[label][arg] = int(subVal.get(arg,None))
                elif arg in ["xBegin","yBegin","zBegin"]:
                    if subVal.get("VerifiedNodule",None).get("mask",None):
                        nodules[label][arg] = float(subVal.get("VerifiedNodule",None).get("mask",None).get(arg,None))#subVal.get("VerifiedNodule",None).get("mask",None).get(arg,None))
                    else:
                        nodules[label][arg] = float(subVal.get("mask",None).get(arg,None))#subVal.get("VerifiedNodule",None).get("mask",None).get(arg,None))
                else:
                    if subVal.get("VerifiedNodule",None).get("mask",None):
                        subSliceMask = subVal.get("VerifiedNodule",None).get("mask",None).get("sliceMask",None)#.get("VerifiedNodule",None).get("mask",None).get("sliceMask",None)#['item']
                    else:
                        subSliceMask = subVal.get("mask",None).get("sliceMask",None)
                    subSliceMask.pop("count")
                    for key,val in subSliceMask.items():#current 
                        for i in val:
                            nodules[label][arg] += i
                    # nodules[label][arg] =subVal.get("VerifiedNodule",None).get("mask",None).get("sliceMask",None)['item']
    # print("nodules=",nodules)
    features = {}
    kwargs = {'binWidth': 64,
              'interpolator': sitk.sitkBSpline,
              'resampledPixelSpacing': None}
    for noduleLabel in nodules:
        if 'DimInPixelX' not in nodules[noduleLabel]:
            continue
        print("noduleLabel=",noduleLabel)
        bbox_dim = (nodules[noduleLabel]['DimInPixelX'], nodules[noduleLabel]['DimInPixelY'], \
                   nodules[noduleLabel]['DimInPixelZ'])
        bbox_ori = (nodules[noduleLabel]['xBegin'], nodules[noduleLabel]['yBegin'], \
                   nodules[noduleLabel]['zBegin'])

        sitkMask = sitk.Image(bbox_dim[0], bbox_dim[1], bbox_dim[2], sitk.sitkUInt8)
        sitkMask.SetSpacing(spacing)
        sitkMask.SetOrigin(bbox_ori)
        sitkMask.SetDirection(direction)

        for z in range(bbox_dim[2]):
            for y in range(bbox_dim[1]):
                for x in range(bbox_dim[0]):
                    idx = z * bbox_dim[1] * bbox_dim[0]  + y * bbox_dim[0] + x
                    v = int(nodules[noduleLabel]['sliceMask'][idx])
                    sitkMask.SetPixel(x, y, z, v)
        ori_matrix = (int(direction[0] * (bbox_ori[0] - origin[0]) / spacing[0]), \
                      int(direction[4] * (bbox_ori[1] - origin[1]) / spacing[1]), \
                      int(direction[8] * (bbox_ori[2] - origin[2]) / spacing[2]))

        # sitkMask = resample_sitkImage(sitkMask, (spacing[0]/4, spacing[1]/4, spacing[2]/4))
        sitkImage = sitk.RegionOfInterest(sitkImageParent, sitkMask.GetSize(), ori_matrix)
        sitkImage.SetSpacing(spacing)
        sitkImage.SetOrigin(bbox_ori)
        sitkImage.SetDirection(direction)

        features[noduleLabel] = {}
        
        firstOrderFeatures = firstorder.RadiomicsFirstOrder(sitkImage, sitkMask, **kwargs)
        firstOrderFeatures.enableAllFeatures()
        firstOrderFeatures.calculateFeatures()
        firstOrderResult = features[noduleLabel].setdefault('firstorder', {})
        for (key, val) in six.iteritems(firstOrderFeatures.featureValues):
            firstOrderResult[key] = val

        shapeFeatures = shape.RadiomicsShape(sitkImage, sitkMask, **kwargs)
        shapeFeatures.enableAllFeatures()
        shapeFeatures.calculateFeatures()
        shapeResult = features[noduleLabel].setdefault('shape', {})
        for (key, val) in six.iteritems(shapeFeatures.featureValues):
            shapeResult[key] = val

        glcmFeatures = glcm.RadiomicsGLCM(sitkImage, sitkMask, **kwargs)
        glcmFeatures.enableAllFeatures()
        glcmFeatures.calculateFeatures()
        glcmResult = features[noduleLabel].setdefault('glcm', {})
        for (key, val) in six.iteritems(glcmFeatures.featureValues):
            glcmResult[key] = val

        glrlmFeatures = glrlm.RadiomicsGLRLM(sitkImage, sitkMask, **kwargs)
        glrlmFeatures.enableAllFeatures()
        glrlmFeatures.calculateFeatures()
        glrlmResult = features[noduleLabel].setdefault('glrlm', {})
        for (key, val) in six.iteritems(glrlmFeatures.featureValues):
            glrlmResult[key] = val

        glszmFeatures = glszm.RadiomicsGLSZM(sitkImage, sitkMask, **kwargs)
        glszmFeatures.enableAllFeatures()
        glszmFeatures.calculateFeatures()
        glszmResult = features[noduleLabel].setdefault('glszm', {})
        for (key, val) in six.iteritems(glszmFeatures.featureValues):
            glszmResult[key] = val
        #added new feature of gldm
        gldmFeatures = gldm.RadiomicsGLDM(sitkImage, sitkMask, **kwargs)
        gldmFeatures.enableAllFeatures()
        gldmFeatures.calculateFeatures()
        gldmFeatures = features[noduleLabel].setdefault('gldm', {})
        for (key, val) in six.iteritems(glszmFeatures.featureValues):
            gldmFeatures[key] = val
        #added new feature of ngtdm
        ngtdmFeatures = ngtdm.RadiomicsNGTDM(sitkImage, sitkMask, **kwargs)
        ngtdmFeatures.enableAllFeatures()
        ngtdmFeatures.calculateFeatures()
        ngtdmFeatures = features[noduleLabel].setdefault('ngtdm', {})
        for (key, val) in six.iteritems(glszmFeatures.featureValues):
            ngtdmFeatures[key] = val

        print("features=",features)

        featuresList = ["FirstOrder","Shape","GLCM","GLRLM","GLSZM","NGTDM","GLDM"]
        if LoG:
            sigmaValues = numpy.arange(5., 0., -.5)[::1]
            for logImage, imageTypeName, inputKwargs in imageoperations.getLoGImage(sitkImage, sitkMask,sigma=sigmaValues):
                for filterName  in featuresList: 
                    exec("LoG"+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(logImage, sitkMask, **inputKwargs)")
                for feature in featuresList:
                    exec("LoG"+feature+"Features.enableAllFeatures()")
                    exec("LoG"+feature+"Features.calculateFeatures()")
                LoGFirstOrderResult = features[noduleLabel].setdefault('LoGFirstOrder', {})
                LoGShapeResult = features[noduleLabel].setdefault('LoGShape', {})
                LoGGLCMResult = features[noduleLabel].setdefault('LoGGlcm', {})
                LoGGLRLMResult = features[noduleLabel].setdefault('LoGGlrlm', {})
                LoGGLSZMResult = features[noduleLabel].setdefault('LoGGlszm', {})
                LoGGLDMResult = features[noduleLabel].setdefault('LoGGldm', {})
                LoGNGTDMResult = features[noduleLabel].setdefault('LoGNGTDM', {})
                for filterName in featuresList:
                    subFeatureValue =eval("LoG" + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                       exec("LoG"+filterName+"Result[key]=val") 
        
        if wavelet:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getWaveletImage(sitkImage,sitkMask):
                for filterName  in featuresList: 
                    exec("wavelet"+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec("wavelet"+filterName+"Features.enableAllFeatures()")
                    exec("wavelet"+filterName+"Features.calculateFeatures()")
                waveletFirstOrderResult = features[noduleLabel].setdefault('waveletFirstOrder', {})
                waveletShapeResult = features[noduleLabel].setdefault('waveletShape', {})
                waveletGLCMResult = features[noduleLabel].setdefault('waveletGlcm', {})
                waveletGLRLMResult = features[noduleLabel].setdefault('waveletGlrlm', {})
                waveletGLSZMResult = features[noduleLabel].setdefault('waveletGlszm', {})
                waveletGLDMResult = features[noduleLabel].setdefault('waveletGldm', {})
                waveletNGTDMResult = features[noduleLabel].setdefault('waveletNGTDM', {})
                for filterName in featuresList:
                    subFeatureValue =eval("wavelet" + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                       exec("wavelet"+filterName+"Result[key]=val") 
        if Square:
            # calculateSubFilterValues(imageType =="Square",features,noduleLabel,sitkImage,sitkMask)
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getSquareImage(sitkImage,sitkMask):
                for filterName  in featuresList: 
                    exec("square"+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec("square"+filterName+"Features.enableAllFeatures()")
                    exec("square"+filterName+"Features.calculateFeatures()")
                squareFirstOrderResult = features[noduleLabel].setdefault('squareFirstOrder', {})
                squareShapeResult = features[noduleLabel].setdefault('squareShape', {})
                squareGLCMResult = features[noduleLabel].setdefault('squareGlcm', {})
                squareGLRLMResult = features[noduleLabel].setdefault('squareGlrlm', {})
                squareGLSZMResult = features[noduleLabel].setdefault('squareGlszm', {})
                squareGLDMResult = features[noduleLabel].setdefault('squareGldm', {})
                squareNGTDMResult = features[noduleLabel].setdefault('squareNGTDM', {})
                for filterName in featuresList:
                    subFeatureValue =eval("square" + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec("square"+filterName+"Result[key]=val") 
        if SquareRoot:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getSquareRootImage(sitkImage,sitkMask):
                for filterName  in featuresList: 
                    exec("squareRoot"+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec("squareRoot"+filterName+"Features.enableAllFeatures()")
                    exec("squareRoot"+filterName+"Features.calculateFeatures()")
                squareRootFirstOrderResult = features[noduleLabel].setdefault('squareRootFirstOrder', {})
                squareRootShapeResult = features[noduleLabel].setdefault('squareRootShape', {})
                squareRootGLCMResult = features[noduleLabel].setdefault('squareRootGlcm', {})
                squareRootGLRLMResult = features[noduleLabel].setdefault('squareRootGlrlm', {})
                squareRootGLSZMResult = features[noduleLabel].setdefault('squareRootGlszm', {})
                squareRootGLDMResult = features[noduleLabel].setdefault('squareRootGldm', {})
                squareRootNGTDMResult = features[noduleLabel].setdefault('squareRootNGTDM', {})
                for filterName in featuresList:
                    subFeatureValue =eval("squareRoot" + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec("squareRoot"+filterName+"Result[key]=val") 
        if Logarithm:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getLogarithmImage(sitkImage,sitkMask):
                for filterName  in featuresList: 
                    exec("logarithm"+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec("logarithm"+filterName+"Features.enableAllFeatures()")
                    exec("logarithm"+filterName+"Features.calculateFeatures()")
                logarithmFirstOrderResult = features[noduleLabel].setdefault('logarithmFirstOrder', {})
                logarithmShapeResult = features[noduleLabel].setdefault('logarithmShape', {})
                logarithmGLCMResult = features[noduleLabel].setdefault('logarithmGlcm', {})
                logarithmGLRLMResult = features[noduleLabel].setdefault('logarithmGlrlm', {})
                logarithmGLSZMResult = features[noduleLabel].setdefault('logarithmGlszm', {})
                logarithmGLDMResult = features[noduleLabel].setdefault('logarithmGldm', {})
                logarithmNGTDMResult = features[noduleLabel].setdefault('logarithmNGTDM', {})
                for filterName in featuresList:
                    subFeatureValue =eval("logarithm" + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec("logarithm"+filterName+"Result[key]=val")
    
        if Exponential:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getExponentialImage(sitkImage,sitkMask):
                for filterName  in featuresList: 
                    exec("Exponential"+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec("Exponential"+filterName+"Features.enableAllFeatures()")
                    exec("Exponential"+filterName+"Features.calculateFeatures()")
                ExponentialFirstOrderResult = features[noduleLabel].setdefault('ExponentialFirstOrder', {})
                ExponentialShapeResult = features[noduleLabel].setdefault('ExponentialShape', {})
                ExponentialGLCMResult = features[noduleLabel].setdefault('ExponentialGlcm', {})
                ExponentialGLRLMResult = features[noduleLabel].setdefault('ExponentialGlrlm', {})
                ExponentialGLSZMResult = features[noduleLabel].setdefault('ExponentialGlszm', {})
                ExponentialGLDMResult = features[noduleLabel].setdefault('ExponentialGldm', {})
                ExponentialNGTDMResult = features[noduleLabel].setdefault('ExponentialNGTDM', {})
                for filterName in featuresList:
                    subFeatureValue =eval("Exponential" + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec("Exponential"+filterName+"Result[key]=val") 
        if Gradient:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getGradientImage(sitkImage,sitkMask):
                for filterName  in featuresList: 
                    exec("Gradient"+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec("Gradient"+filterName+"Features.enableAllFeatures()")
                    exec("Gradient"+filterName+"Features.calculateFeatures()")
                GradientFirstOrderResult = features[noduleLabel].setdefault('GradientFirstOrder', {})
                GradientShapeResult = features[noduleLabel].setdefault('GradientShape', {})
                GradientGLCMResult = features[noduleLabel].setdefault('GradientGlcm', {})
                GradientGLRLMResult = features[noduleLabel].setdefault('GradientGlrlm', {})
                GradientGLSZMResult = features[noduleLabel].setdefault('GradientGlszm', {})
                GradientGLDMResult = features[noduleLabel].setdefault('GradientGldm', {})
                GradientNGTDMResult = features[noduleLabel].setdefault('GradientNGTDM', {})
                for filterName in featuresList:
                    subFeatureValue =eval("Gradient" + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec("Gradient"+filterName+"Result[key]=val") 
                        
        #LocalBinaryPattern2D,LocalBinaryPattern3D
        if LocalBinaryPattern2D:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getLBP2DImage(sitkImage,sitkMask):
                for filterName  in featuresList: 
                    exec("LBP2D"+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec("LBP2D"+filterName+"Features.enableAllFeatures()")
                    exec("LBP2D"+filterName+"Features.calculateFeatures()")
                LBP2DFirstOrderResult = features[noduleLabel].setdefault('LBP2DFirstOrder', {})
                LBP2DShapeResult = features[noduleLabel].setdefault('LBP2DShape', {})
                LBP2DGLCMResult = features[noduleLabel].setdefault('LBP2DGlcm', {})
                LBP2DGLRLMResult = features[noduleLabel].setdefault('LBP2DGlrlm', {})
                LBP2DGLSZMResult = features[noduleLabel].setdefault('LBP2DGlszm', {})
                LBP2DGLDMResult = features[noduleLabel].setdefault('LBP2DGldm', {})
                LBP2DNGTDMResult = features[noduleLabel].setdefault('LBP2DNGTDM', {})
                for filterName in featuresList:
                    subFeatureValue =eval("LBP2D" + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec("LBP2D"+filterName+"Result[key]=val") 
        
        if LocalBinaryPattern3D:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getLBP3DImage(sitkImage,sitkMask):
                for filterName  in featuresList: 
                    exec("LBP3D"+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec("LBP3D"+filterName+"Features.enableAllFeatures()")
                    exec("LBP3D"+filterName+"Features.calculateFeatures()")
                LBP3DFirstOrderResult = features[noduleLabel].setdefault('LBP3DFirstOrder', {})
                LBP3DShapeResult = features[noduleLabel].setdefault('LBP3DShape', {})
                LBP3DGLCMResult = features[noduleLabel].setdefault('LBP3DGlcm', {})
                LBP3DGLRLMResult = features[noduleLabel].setdefault('LBP3DGlrlm', {})
                LBP3DGLSZMResult = features[noduleLabel].setdefault('LBP3DGlszm', {})
                LBP3DGLDMResult = features[noduleLabel].setdefault('LBP3DGldm', {})
                LBP3DNGTDMResult = features[noduleLabel].setdefault('LBP3DNGTDM', {})
                for filterName in featuresList:
                    subFeatureValue =eval("LBP3D" + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec("LBP3D"+filterName+"Result[key]=val")
    return features

def run(nii, jsf,waveletFilter,LogFilter,Square,SquareRoot,Logarithm,\
                Exponential,Gradient,LocalBinaryPattern2D,LocalBinaryPattern3D,src=None, dst=None):
    # try:
    features = calculateRadiomicsFromJson(nii, jsf,waveletFilter,LogFilter,Square,SquareRoot,Logarithm,\
                Exponential,Gradient,LocalBinaryPattern2D,LocalBinaryPattern3D)
    sortedFeature_Json = OrderedDict()
    for key,val in features.items():
        sortedFeature_Json[key]={}
        for subKey,subVal in val.items():
            for k,v in subVal.items():
                newKey = subKey+"_"+k
                sortedFeature_Json[key][newKey] = v
    saveFeatures2CSVFile(features,jsf)
def saveFeatures2CSVFile(featuresDict,jsf):
    features = featuresDict
    if not features:
        return
    _csv = jsf.replace('.json', '_radiomics.csv')
    sortedLabel = sorted(features.keys())
    sortedFeature = OrderedDict()
    print("features=",features)
    print("sortedLabel={}".format(sortedLabel))
    for i in sorted(features[sortedLabel[0]].keys()):
        sortedFeature[i] = sorted(features[sortedLabel[0]][i])  
    with open(_csv, 'w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['', '']
        for i in sortedLabel:
            header.append('Nodule {}'.format(i))
        print("header=",header)
        writer.writerow(header)
        for title, values in sortedFeature.items():
            for index, feature in enumerate(values):
                row = [features[i][title][feature] for i in sortedLabel]
                if index == 0:
                    row.insert(0, title)
                else:
                    row.insert(0, '')
                row.insert(1, feature)
                writer.writerow(row)

def run_1(nii, jsf,waveletFilter,LogFilter,Square,SquareRoot,Logarithm,\
                Exponential,Gradient,LocalBinaryPattern2D,LocalBinaryPattern3D,src=None, dst=None):
    features = calculateRadiomicsFromJson(nii, jsf,waveletFilter,LogFilter,Square,SquareRoot,Logarithm,\
                Exponential,Gradient,LocalBinaryPattern2D,LocalBinaryPattern3D)
    if not features:
        return
    # sortedFeature_Json = OrderedDict()
    # for key,val in features.items():
    #     sortedFeature_Json[key]={}
    #     for subKey,subVal in val.items():
    #         for k,v in subVal.items():
    #             newKey = subKey+"_"+k
    #             sortedFeature_Json[key][newKey] = v

    # _json = jsf
    # if src and dst:
    #     _json = _json.replace(src.strip('/\\'), dst)
    # _json = _json.replace('.json', '_radiomics.json')
    # with open(_json,"w") as f:
    #     json.dump(sortedFeature_Json,f,indent=4,sort_keys=True)
    saveFeatures2CSVFile(features,jsf)

if __name__ == '__main__':
    filePath = r"E:\Nii_Output"
    niiFileList = [x for x in os.listdir(filePath) if x.endswith(".nii")]
    print("niiFileList=",niiFileList)
    parser = argparse.ArgumentParser(
        description='to calculate the radiomics features from input json and nii files.')
    parser.add_argument('--nii', help='input nii file')
    parser.add_argument('--json', help='input json file')
    parser.add_argument('--wavelet',help="input wavelet filter is enabled or not")
    parser.add_argument('--LoG',help="input Laplacian of Gaussian filter is enabled or not")
    parser.add_argument('--Square',help="input Square filter is enabled or not")
    parser.add_argument('--SquareRoot',help="input SquareRoot filter is enabled or not")
    parser.add_argument('--Logarithm',help="input Logarithm filter is enabled or not")
    parser.add_argument('--Exponential',help="input Exponential filter is enabled or not")
    parser.add_argument('--Gradient',help="input Gradient filter is enabled or not")
    parser.add_argument('--LocalBinaryPattern2D',help="input LocalBinaryPattern2D filter is enabled or not")
    parser.add_argument('--LocalBinaryPattern3D',help="input LocalBinaryPattern3D filter is enabled or not")
    args = parser.parse_args()
    #set all the arguments as True
    argumentList = ["wavelet","LoG","Square","SquareRoot","Logarithm",\
                    "Exponential","Gradient","LocalBinaryPattern2D","LocalBinaryPattern3D"]
    for arg in argumentList:
         exec("args."+arg+"=True")
    for subfile in niiFileList:
        args.nii = os.path.join(filePath,subfile)
        args.json = args.nii.replace(".nii","_CAD_Lung_test.json")
        csvFile = args.nii.replace(".nii",".csv")
        
        if os.path.exists(csvFile):
            print("Juming file=",subfile)
            continue
        if os.path.exists(args.nii) and os.path.exists(args.json):
            import time
            # features = calculateRadiomicsFromJson(args.nii, args.json)
            startTime = time.time()
            print("Computing file=",args.nii)
            print("Computing json=",args.json)
            # try:
            run_1(args.nii,args.json,args.wavelet,args.LoG,args.Square,args.SquareRoot,args.Logarithm,\
                args.Exponential,args.Gradient,args.LocalBinaryPattern2D,args.LocalBinaryPattern3D)
            # except:
            #     print (1111)
            #     import shutil
            #     badNiiFileFolder = filePath+"\issuedNiiFiles"
            #     if os.path.isdir(badNiiFileFolder):
            #         os.mkdir(badNiiFileFolder)
            #     shutil.move(args.nii,badNiiFileFolder)
            #     shutil.move(args.json,badNiiFileFolder)
            # else:
            endTime = time.time()
            print("Running Time:",endTime-startTime)
            # fjson = open(args.json.replace('.json', '_radiomics.json'), 'w')
            # featuresFinal = {k:(features[k]) for k in sorted(features.keys())}
            # json.dump(features, fjson, indent=4, sort_keys=True)
            print('radiomics calculation done!')

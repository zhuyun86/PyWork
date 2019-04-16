# -*- coding: utf-8 -*-
"""
    Program: discoveryRadiomics
    file name: jsonradiomics.py
    date of creation: 2017-06-28 by LiuHui
    date of modification: 2018-03-31
    Author: Chunbo Liu (cbliu@12sigma.com)
    change History: 
    1.support the CAD result of  SigmaLU 0.5.6
    2.import latest pyradiomics 2.0.0
    3.can support all of the filters
    $CHANGDATE:20190221
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
import click
import numpy as np
#import scipy
# from scipy import optimize

# import skimage
# import trimesh


__version__="3.1.0"

__doc__ = """
            20190221--removed the rawInput function which can return to caller without keyboard inputs
          """

from radiomics import firstorder, glcm, glrlm, glszm, shape, ngtdm,gldm,imageoperations
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

def calculateRadiomicsFromJson(niiFile, jsonFile,log,wavelet,square,squareroot,logarithm,exponential,gradient):
    # processing nii
    sitkImageParent = sitk.ReadImage(niiFile)
    direction = sitkImageParent.GetDirection()
    origin = sitkImageParent.GetOrigin()
    spacing = sitkImageParent.GetSpacing()
    # processing json
    f = open(jsonFile)
    p = ijson.parse(f)
    nodules = {}
    label = ''
    for prefix, _, value in p:
        if re.match('Nodules.item\d+.Label', prefix) or prefix == 'Nodules.item.Label':
            label = value
            nodules[label] = {}
            nodules[label]['label'] = value
            nodules[label]['sliceMask'] = ''
        if re.match('Nodules.item\d+.mask.xBegin', prefix) or prefix == 'Nodules.item.mask.xBegin':
            nodules[label]['xBegin'] = float(value)
        if re.match('Nodules.item\d+.mask.yBegin', prefix) or prefix == 'Nodules.item.mask.yBegin':
            nodules[label]['yBegin'] = float(value)
        if re.match('Nodules.item\d+.mask.zBegin', prefix) or prefix == 'Nodules.item.mask.zBegin':
            nodules[label]['zBegin'] = float(value)
        if re.match('Nodules.item\d+.DimInPixelX', prefix) or prefix == 'Nodules.item.DimInPixelX':
            nodules[label]['DimInPixelX'] =int(float(value))
        if re.match('Nodules.item\d+.DimInPixelY', prefix) or prefix == 'Nodules.item.DimInPixelY':
            nodules[label]['DimInPixelY'] = int(float(value))
        if re.match('Nodules.item\d+.DimInPixelZ', prefix) or prefix == 'Nodules.item.DimInPixelZ':
            nodules[label]['DimInPixelZ'] = int(float(value))
        if re.match('Nodules.item\d+.mask.sliceMask.item\d+', prefix) or prefix == 'Nodules.item.mask.sliceMask.item':
            nodules[label]['sliceMask'] += value
    # working on radiomics calculation
    features = {}
    kwargs = {'binWidth': 25,
              'interpolator': sitk.sitkBSpline,
              'resampledPixelSpacing': None}
    
    for noduleLabel in nodules:
        if 'DimInPixelX' not in nodules[noduleLabel]:
            continue
        bbox_dim = (nodules[noduleLabel]['DimInPixelX'], nodules[noduleLabel]['DimInPixelY'], \
                   nodules[noduleLabel]['DimInPixelZ'])
        bbox_ori = (nodules[noduleLabel]['xBegin'], nodules[noduleLabel]['yBegin'], \
                   nodules[noduleLabel]['zBegin'])
        sitkMask = sitk.Image(bbox_dim[0], bbox_dim[1], bbox_dim[2], sitk.sitkUInt8)
        sitkMask.SetSpacing(spacing)
        sitkMask.SetOrigin(bbox_ori)
        sitkMask.SetDirection(direction)

        for z in range(bbox_dim[2]):#9
            for y in range(bbox_dim[1]):  #16
                for x in range(bbox_dim[0]): #17
                    idx = z * bbox_dim[1] * bbox_dim[0]  + y * bbox_dim[0] + x
                    v = int(nodules[noduleLabel]['sliceMask'][idx])
                    sitkMask.SetPixel(x, y, z, v)
        ori_matrix = (int(direction[0] * (bbox_ori[0] - origin[0]) / spacing[0]), \
                      int(direction[4] * (bbox_ori[1] - origin[1]) / spacing[1]), \
                      int(direction[8] * (bbox_ori[2] - origin[2]) / spacing[2]))

        sitkImage = sitk.RegionOfInterest(sitkImageParent, sitkMask.GetSize(), ori_matrix)
        sitkImage.SetSpacing(spacing)
        sitkImage.SetOrigin(bbox_ori)
        sitkImage.SetDirection(direction)

        features[noduleLabel] = OrderedDict()
        featuresList = ["FirstOrder","GLCM","GLRLM","GLSZM","NGTDM","GLDM"]
        
        #compute the original image's features data
        original_features_list = featuresList+["Shape"]
        exponential_features_list =["FirstOrder","GLRLM","GLSZM","GLDM"]
        for originalImage,imageTypeName,inputKwars in imageoperations.getOriginalImage(sitkImage,sitkMask,**kwargs):
            newImageName = imageTypeName+"_"
            for filterName  in original_features_list: 
                exec(newImageName+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(originalImage, sitkMask, **kwargs)")
                exec(newImageName+filterName+"Features.enableAllFeatures()")
                exec(newImageName+filterName+"Features.calculateFeatures()")
                exec(newImageName+filterName+"=features[noduleLabel].setdefault(newImageName+filterName,{})")
                subFeatureValue =eval(newImageName + filterName + "Features.featureValues")
                for (key, val) in six.iteritems(subFeatureValue):
                    exec(newImageName+filterName+"[key]=val") 

        if log:
            sigmaValues = numpy.arange(5., 0., -1)[::1]
            for logImage, imageTypeName, inputKwargs in imageoperations.getLoGImage(sitkImage, sitkMask,sigma=sigmaValues):
                newImageName = imageTypeName.replace("-","_")+"_"
                for filterName  in featuresList: 
                    exec(newImageName+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(logImage, sitkMask, **inputKwargs)")
                    exec(newImageName+filterName+"Features.enableAllFeatures()")
                    exec(newImageName+filterName+"Features.calculateFeatures()")
                    exec(newImageName+filterName+"=features[noduleLabel].setdefault(newImageName+filterName,{})")
                    subFeatureValue =eval(newImageName + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                       exec(newImageName+filterName+"[key]=val") 

        if wavelet:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getWaveletImage(sitkImage,sitkMask,**kwargs):
                newName = "wavelet_"+decompositionName.split("-")[-1]+"_"    #here should be use more elegant method
                for filterName  in featuresList: 
                    exec("wavelet"+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec("wavelet"+filterName+"Features.enableAllFeatures()")
                    exec("wavelet"+filterName+"Features.calculateFeatures()")
                    exec(newName+filterName+"=features[noduleLabel].setdefault(newName+filterName,{})")
                    subFeatureValue =eval("wavelet" + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                       exec(newName+filterName+"[key]=val") 

        if square:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getSquareImage(sitkImage,sitkMask):
                newDecompositionName = decompositionName+"_"
                for filterName  in featuresList: 
                    exec(newDecompositionName+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec(newDecompositionName+filterName+"Features.enableAllFeatures()")
                    exec(newDecompositionName+filterName+"Features.calculateFeatures()")
                    exec(newDecompositionName+filterName+"=features[noduleLabel].setdefault(newDecompositionName+filterName,{})")
                    subFeatureValue =eval(newDecompositionName + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec(newDecompositionName+filterName+"[key]=val") 
        
        if squareroot:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getSquareRootImage(sitkImage,sitkMask):
                newDecompositionName = decompositionName+"_"
                for filterName  in featuresList: 
                    exec(newDecompositionName+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec(newDecompositionName+filterName+"Features.enableAllFeatures()")
                    exec(newDecompositionName+filterName+"Features.calculateFeatures()")
                    exec(newDecompositionName+filterName+"=features[noduleLabel].setdefault(newDecompositionName+filterName,{})")
                    subFeatureValue =eval(newDecompositionName + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec(newDecompositionName+filterName+"[key]=val") 
        
        if logarithm:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getLogarithmImage(sitkImage,sitkMask):
                newDecompositionName = decompositionName+"_"
                for filterName  in featuresList: 
                    exec(newDecompositionName+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec(newDecompositionName+filterName+"Features.enableAllFeatures()")
                    exec(newDecompositionName+filterName+"Features.calculateFeatures()")
                    exec(newDecompositionName+filterName+"=features[noduleLabel].setdefault(newDecompositionName+filterName,{})")
                    subFeatureValue =eval(newDecompositionName + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec(newDecompositionName+filterName+"[key]=val")
    
        if exponential:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getExponentialImage(sitkImage,sitkMask):
                newDecompositionName = decompositionName+"_"
                for filterName  in exponential_features_list: 
                    exec(newDecompositionName+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec(newDecompositionName+filterName+"Features.enableAllFeatures()")
                    exec(newDecompositionName+filterName+"Features.calculateFeatures()")
                    exec(newDecompositionName+filterName+"=features[noduleLabel].setdefault(newDecompositionName+filterName,{})")
                # for filterName in exponential_features_list:
                    subFeatureValue =eval(newDecompositionName + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec(newDecompositionName+filterName+"[key]=val") 
        
        if gradient:
            for decompositionImage, decompositionName, inputKwargs in imageoperations.getGradientImage(sitkImage,sitkMask):
                newDecompositionName = decompositionName+"_"
                for filterName  in featuresList: 
                    exec(newDecompositionName+filterName+"Features = "+filterName.lower()+".Radiomics"+filterName+"(decompositionImage, sitkMask, **inputKwargs)")
                    exec(newDecompositionName+filterName+"Features.enableAllFeatures()")
                    exec(newDecompositionName+filterName+"Features.calculateFeatures()")
                    exec(newDecompositionName+filterName+"=features[noduleLabel].setdefault(newDecompositionName+filterName,{})")
                # for filterName in featuresList:
                    subFeatureValue =eval(newDecompositionName + filterName + "Features.featureValues")
                    for (key, val) in six.iteritems(subFeatureValue):
                        exec(newDecompositionName+filterName+"[key]=val") 
                        
    return features
    
def run(nii, jsf,output,log,wavelet,square,squareroot,logarithm,exponential,gradient,src=None, dst=None):
    features = calculateRadiomicsFromJson(nii, jsf,log,wavelet,square,squareroot,logarithm,exponential,gradient)
    sortedFeature_Json =OrderedDict()
    for key,val in features.items():
        sortedFeature_Json[key]=OrderedDict()
        for subKey,subVal in val.items():
            for k,v in subVal.items():
                newKey = subKey+"_"+k
                if not isinstance(v,np.complex128) :
                    sortedFeature_Json[key][newKey] = v

    _json = jsf
    if src and dst:
        _json = _json.replace(src.strip('/\\'), dst)
    _json = _json.replace('.json', '_radiomics.json')

    if output:
        _json = output
    with open(_json,"w") as f:
        json.dump(sortedFeature_Json,f,indent=4,sort_keys=False)


CONTEXT_SETTINGS = dict(token_normalize_func=lambda x: x.lower())
@click.command(context_settings=CONTEXT_SETTINGS)
# @click.command()
@click.option('--nii',help="nii file path")
@click.option('--json',help='json file path')
@click.option('--output',help="output path of radiomics data file")
@click.option('--log',is_flag=True)
@click.option("--wavelet",is_flag=True)
@click.option("--square",is_flag=True)
@click.option("--squareroot",is_flag=True)
@click.option("--logarithm",is_flag=True)
@click.option("--exponential",is_flag=True)
@click.option("--gradient",is_flag=True)
def main(nii,json,output,log,wavelet,square,squareroot,logarithm,exponential,gradient):
    nii = str(nii)
    json=str(json)
    if os.path.exists(nii) and os.path.exists(json):
        import time
        startTime = time.time()
        run(nii,json,output,log,wavelet,square,squareroot,logarithm,exponential,gradient)
        endTime = time.time()
        print("Running Time:",endTime-startTime)
        print('radiomics calculation done!')
    

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(str(e))
        # raw_input('Please press enter key to exit ...')
    
    

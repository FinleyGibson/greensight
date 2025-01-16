1. Indices are defined in the sentinel2b class
   
   1. see addNDVIimg(self, image) function
   
   2. in test_3, call function to add the selected indices, defined as a list. (see `selectedIndices = ['ndvi']` )
   
   3. add map call to `__init__` of sentinel2b class. 
   
   4. can compare with results of [QGIS](https://www.qgis.org/)

To test:

1. Export image as shown in Seintiel2_test

2. Drag and drop .tif image into QGIS

3. Raster->raster calculator

4. set min and max by right click on layers and render type: singleband gray.



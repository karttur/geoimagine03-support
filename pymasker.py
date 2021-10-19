'''
Copied on 9 july 2019 from
https://github.com/haoliangyu/pymasker/blob/master/pymasker.py

@author: thomasgumbricht
'''

# Standard library imports

import os


class Masker(object):
    '''Provides access to functions that produces masks from remote sensing image, according to its bit structure.'''

    def __init__(self, band, **var):

        if type(band) is str:
            if 'band_num' in var:
                self.load_file(band, var['band_num'])
            else:
                self.load_file(band)
        else:
            self.load_data(band)

    def load_file(self, file_path, band_num = 0):
        '''Load the QA file from a give path
        Parameters
            file_path    -    Path of band file.
            band_num    -    Number of band.
        '''
        import gdal

        self.file_path = file_path
        extension = os.path.splitext(file_path)[1].lower()

        # load file according to the file format.
        if extension == '.hdf':
            dataset = gdal.Open(file_path)
            subdataset = dataset.GetSubDatasets()[band_num][0]
            self.band_data = gdal.Open(subdataset).ReadAsArray()
        else:
            bandfile = gdal.Open(file_path)
            self.band_data = bandfile.GetRasterBand(1).ReadAsArray()

    def load_data(self, array):
        '''Load the BQA ban from a np.array
        Parameters
            array        -    Numpy array that contains the band data.
        '''
        self.file_path = None
        self.band_data = array

    def get_mask(self, bit_pos, bit_len, value):
        '''Generates mask with given bit information.
        Parameters
            bit_pos        -    Position of the specific QA bits in the value string.
            bit_len        -    Length of the specific QA bits.
            value          -    A value indicating the desired condition.
        '''
        bitlen = int('1' * bit_len, 2)

        if type(value) == str:
            value = int(value, 2)

        pos_value = bitlen << bit_pos
        con_value = value << bit_pos
        mask = (self.band_data & pos_value) == con_value

        return mask.astype(int)

    def save_tif(self, mask, file_path):
        '''Save the given mask as a .tif file.
        Parameters
            mask         -    A mask generated with masker.
            file_path    -    Path of .tif file.
        '''
        import gdal

        driver = gdal.GetDriverByName('GTiff')

        x_pixels = mask.shape[1]
        y_pixels = mask.shape[0]

        dataset = driver.Create(file_path, x_pixels, y_pixels, 1, gdal.GDT_Byte)

        if self.file_path is not None:
            extension = os.path.splitext(self.file_path)[1].lower()
            if extension == '.hdf':
                hdfdataset = gdal.Open(self.file_path)
                subdataset = hdfdataset.GetSubDatasets()[0][0]
                bandfile = gdal.Open(subdataset)
            else:
                bandfile = gdal.Open(self.file_path)

            dataset.SetGeoTransform(bandfile.GetGeoTransform())
            dataset.SetProjection(bandfile.GetProjectionRef())
        dataset.GetRasterBand(1).SetNoDataValue(0)
        dataset.GetRasterBand(1).WriteArray(mask)
        dataset.FlushCache()

class LandsatConfidence(object):
    '''Level of confidence that a condition exists
    high         -    Algorithm has high confidence that this condition exists (67-100 percent confidence).
    medium         -    Algorithm has medium confidence that this condition exists (34-66 percent confidence).
    low         -    Algorithm has low to no confidence that this condition exists (0-33 percent confidence)
    undefined    -     Algorithm did not determine the status of this condition.
    none        -    Nothing.
    '''
    high = 3
    medium = 2
    low = 1
    undefined = 0
    none = -1

class LandsatMasker(Masker):
    '''Provides access to functions that produces masks from quality assessment band of Landsat 8.'''

    def __init__(self, file_path, **var):

        if 'collection' not in var:
            raise Exception('Collection number is required for landsast masker.')
        elif var['collection'] != 1 and var['collection'] != 0:
            raise Exception('Collection number must be 0 or 1.')

        self.collection = var['collection']
        super(LandsatMasker, self).__init__(file_path)

    def get_no_cloud_mask(self):
        '''Generate a mask for pixels with no cloud.
        Return
            mask        -   A two-dimensional binary mask
        '''

        if self.collection == 0:
            raise Exception('Non-cloud mask is not available for pre-collection data.')
        elif self.collection == 1:
            return self.__get_mask(4, 1, 0, False).astype(int)

    def get_cloud_mask(self, conf=None, cumulative=False):
        '''Generate a cloud mask.
        Parameters
            conf        -    Level of confidence that cloud exists.
            cumulative    -    A Boolean value indicating whether to get masker with confidence value larger than the given one..
        Return
            mask         -    A two-dimension binary mask.
        '''

        if self.collection == 0:
            if conf is None or conf == -1:
                raise Exception('Confidence value is required for creating cloud mask from pre-collection data.')

            return self.__get_mask(14, 3, conf, cumulative).astype(int)
        elif self.collection == 1 and (conf is None or conf == -1):
            return self.__get_mask(4, 1, 1, False).astype(int)
        elif self.collection == 1:
            return self.__get_mask(5, 3, conf, cumulative).astype(int)

    def get_cloud_shadow_mask(self, conf, cumulative = False):
        '''Generate a cloud shadow mask. Note that the cloud shadow mask is only available for collection 1 data.
        Parameters
            conf        -    Level of confidence that water body exists.
            cumulative    -    A Boolean value indicating whether to get masker with confidence value larger than the given one..
        Return
            mask         -    A two-dimension binary mask.
        '''

        if self.collection == 0:
            raise Exception('Cloud shadow mask is not available for Lansat collection 1 data.')
        elif self.collection == 1:
            return self.__get_mask(7, 3, conf, cumulative).astype(int)

    def get_cirrus_mask(self, conf, cumulative = False):
        '''Generate a cirrus mask. Note that the cirrus mask is only available for Landsat-8 images.
        Parameters
            conf        -    Level of confidence that cloud exists.
            cumulative    -    A Boolean value indicating whether to get masker with confidence value larger than the given one..
        Return
            mask         -    A two-dimension binary mask.
        '''

        if self.collection == 0:
            return self.__get_mask(12, 3, conf, cumulative).astype(int)
        elif self.collection == 1:
            return self.__get_mask(11, 3, conf, cumulative).astype(int)

    def get_water_mask(self, conf, cumulative = False):
        '''Generate a water body mask. Note that the waster mask is only available for pre-collection data.
        Parameters
            conf        -    Level of confidence that water body exists.
            cumulative    -    A Boolean value indicating whether to get masker with confidence value larger than the given one..
        Return
            mask         -    A two-dimension binary mask.
        '''

        if self.collection == 0:
            if conf == 1 or conf == 3:
                raise Exception('Creating water mask for pre-collection data only accepts confidence value 0 and 2.')

            return self.__get_mask(4, 3, conf, cumulative).astype(int)
        elif self.collection == 1:
            raise Exception('Water mask is not available for Lansat pre-collection data.')

    def get_snow_mask(self, conf, cumulative = False):
        '''Generate a water body mask.
        Parameters
            conf        -    Level of confidence that snow/ice exists.
            cumulative    -    A Boolean value indicating whether to get masker with confidence value larger than the given one..
        Return
            mask         -    A two-dimension binary mask.
        '''

        if self.collection == 0:
            if conf == 1 or conf == 2:
                raise Exception('Creating snow mask for pre-collection data only accepts confidence value 0 and 3.')

            return self.__get_mask(10, 3, conf, cumulative).astype(int)
        elif self.collection == 1:
            return self.__get_mask(9, 3, conf, cumulative).astype(int)

    def get_fill_mask(self):
        '''Generate a mask for designated fill pixels.
        Return
            mask        -   A two-dimensional binary mask
        '''
        return self.__get_mask(0, 1, 1, False).astype(int)

    def __get_mask(self, bit_loc, bit_len, value, cumulative):
        '''Get mask with specific parameters.
        Parameters
            bit_loc        -    Location of the specific QA bits in the value string.
            bit_len        -    Length of the specific QA bits.
            value          -    A value indicating the desired condition.
            cumulative    -    A Boolean value indicating whether to get masker with confidence value larger than the given one..
        '''

        pos_value = bit_len << bit_loc
        con_value = value << bit_loc

        if cumulative:
            mask = (self.band_data & pos_value) >= con_value
        else:
            mask = (self.band_data & pos_value) == con_value

        return mask
    
    def __get_maskTest(self, bit_loc, bit_len, value, cumulative):
        '''Get mask with specific parameters.
        Parameters
            bit_loc        -    Location of the specific QA bits in the value string.
            bit_len        -    Length of the specific QA bits.
            value          -    A value indicating the desired condition.
            cumulative    -    A Boolean value indicating whether to get masker with confidence value larger than the given one..
        '''

        pos_value = bit_len << bit_loc
        con_value = value << bit_loc
        '''
        print ('bit_loc',bit_loc)
        print ('bit_len',bit_len)
        print ('pos_value',pos_value)
        print ('con_value',con_value)
        BAND = self.band_data.flatten()
        print (BAND)
        print ('cumulative',cumulative)
        for v in BAND:
            #print ('v',v)
            mask = (np.array([v]) & pos_value) >= con_value
            #print ( 'testvalue',(np.array([928]) & pos_value) )
            #fisk
            if mask[0]:
                print ( (np.array([v]) & pos_value) )
                print ('v',v)
                BALLE

        FISK
        '''

        if cumulative:
            mask = (self.band_data & pos_value) >= con_value
        else:
            mask = (self.band_data & pos_value) == con_value

        return mask

class ModisQuality(object):
    '''Level of data quality of MODIS land products at each pixel.
    high        -    Corrected product produced at ideal quality for all bands.
    medium        -    Corrected product produced at less than ideal quality for some or all bands.
    low         -    Corrected product not produced due to some reasons for some or all bands.
    low_cloud    -    Corrected product not produced due to cloud effects for all bands.
    '''

    high = 0
    medium = 1
    low = 2
    low_cloud = 3

class ModisMasker(Masker):
    '''Provides access to functions that produce QA masks from quality assessment band of MODIS land products.'''

    def __init__(self, file_path):
        super(ModisMasker, self).__init__(file_path, 3)

    def get_qa_mask(self, quality):
        '''Get a quality mask.
        Parameters
            quality        -    Desired level of data quality.
        Returns
            mask         -    A two-dimension binary mask.
        '''

        return self.get_mask(0, 2, quality).astype(int)

if __name__ == "__main__":
    #main()
    srcFPN = '/Volumes/guatemala/landsat/LT05/scenes/dndqa/p019/r049/19941022/bqa_L1TP_p019r049_19941022_0.tif'
    masker = LandsatMasker(srcFPN, collection=1)

    # algorithm has high confidence that this condition exists
    #Set to medium and cumulative, which in effect represents
    
    # (34-100 percent confidence)
    
    conf = LandsatConfidence.medium
    
    # Get mask indicating cloud pixels with high confidence
    cumulative = True

    cloudmask = masker.get_cloud_mask(conf,cumulative)

    
   
    shadowmask = masker.get_cloud_shadow_mask(conf,cumulative)
    

    snowmask = masker.get_snow_mask(conf,cumulative)
    
    fillmask = masker.get_fill_mask()
    
    shadowmask *= 2
    snowmask *= 3
    fillmask *= 4
    
    mask = cloudmask+shadowmask+snowmask+fillmask
    #Reset the cloudmask to let it rule over cloud shadows and snow
    mask[cloudmask == 1] = 1
    
    
    # save the result
    dstFPN = '/Volumes/guatemala/landsat/LT05/scenes/dndqa/p019/r049/19941022/mask_L1TP_p019r049_19941022_0.tif'

    masker.save_tif(mask, dstFPN)
    
    
    '''
    #####
    conf = LandsatConfidence.medium
    
    print ('confmedium')
    
    # Get mask indicating cloud pixels withmedium confidence
    mask = masker.get_cloud_mask(conf,cumulative)
    
    # save the result
    dstFPN = '/Volumes/guatemala/landsat/LT05/scenes/dndqa/p019/r049/19941022/cloudmask-medium_L1TP_p019r049_19941022_0.tif'

    masker.save_tif(mask, dstFPN)
    
    mask = masker.get_cloud_shadow_mask(conf,cumulative)
    
    # save the result
    dstFPN = '/Volumes/guatemala/landsat/LT05/scenes/dndqa/p019/r049/19941022/cloudshadow-medium_L1TP_p019r049_19941022_0.tif'

    masker.save_tif(mask, dstFPN)
    
    
    
    # Get no cloud
    
    mask = masker.get_no_cloud_mask()
    
    # save the result
    dstFPN = '/Volumes/guatemala/landsat/LT05/scenes/dndqa/p019/r049/19941022/clear_L1TP_p019r049_19941022_0.tif'

    masker.save_tif(mask, dstFPN)
    '''
    
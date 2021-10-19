'''
Created on 11 Jul 2019

@author: thomasgumbricht
'''

def illuminationCondition(img):

def TG(DEM,sunelevation,sunazimuth):
    from math import rad
    degree2radian = 0.01745;
    SZ_rad = sunelevation
    SA_rad = sunazimuth
    slope = rad(DEM.GetSlope())
    aspect = rad(DEM.GetAspect())

var scale = 300;
 
#// get terrain layers
#var dem = ee.Image("USGS/SRTMGL1_003");

 
var terrainCorrection = function(collection) {
 
  collection = collection.map(illuminationCondition);
  collection = collection.map(illuminationCorrection);
 
  return(collection);
 
  ////////////////////////////////////////////////////////////////////////////////
  // Function to calculate illumination condition (IC). Function by Patrick Burns and Matt Macander
  function illuminationCondition(img){
 
  // Extract image metadata about solar position
  var SZ_rad = ee.Image.constant(ee.Number(img.get('SOLAR_ZENITH_ANGLE'))).multiply(3.14159265359).divide(180).clip(img.geometry().buffer(10000));
  var SA_rad = ee.Image.constant(ee.Number(img.get('SOLAR_AZIMUTH_ANGLE')).multiply(3.14159265359).divide(180)).clip(img.geometry().buffer(10000));
  // Creat terrain layers
  var slp = ee.Terrain.slope(dem).clip(img.geometry().buffer(10000));
  var slp_rad = ee.Terrain.slope(dem).multiply(3.14159265359).divide(180).clip(img.geometry().buffer(10000));
  var asp_rad = ee.Terrain.aspect(dem).multiply(3.14159265359).divide(180).clip(img.geometry().buffer(10000));
 
  // Calculate the Illumination Condition (IC)
  // slope part of the illumination condition
  var cosZ = SZ_rad.cos();
  var cosS = slp_rad.cos();
  var slope_illumination = cosS.expression("cosZ * cosS",
                                          {'cosZ': cosZ,
                                           'cosS': cosS.select('slope')});
  // aspect part of the illumination condition
  var sinZ = SZ_rad.sin();
  var sinS = slp_rad.sin();
  var cosAziDiff = (SA_rad.subtract(asp_rad)).cos();
  var aspect_illumination = sinZ.expression("sinZ * sinS * cosAziDiff",
                                           {'sinZ': sinZ,
                                            'sinS': sinS,
                                            'cosAziDiff': cosAziDiff});
  // full illumination condition (IC)
  var ic = slope_illumination.add(aspect_illumination);
 
  // Add IC to original image
  var img_plus_ic = ee.Image(img.addBands(ic.rename('IC')).addBands(cosZ.rename('cosZ')).addBands(cosS.rename('cosS')).addBands(slp.rename('slope')));
  return img_plus_ic;
  }
 
// Function to apply the Sun-Canopy-Sensor + C (SCSc) correction method to each
// image. Function by Patrick Burns and Matt Macander
 
function illuminationCorrection(img){
    var props = img.toDictionary();
    var st = img.get('system:time_start');
 
    var img_plus_ic = img;
    var mask1 = img_plus_ic.select('nir').gt(-0.1);
    var mask2 = img_plus_ic.select('slope').gte(5)
                            .and(img_plus_ic.select('IC').gte(0))
                            .and(img_plus_ic.select('nir').gt(-0.1));
    var img_plus_ic_mask2 = ee.Image(img_plus_ic.updateMask(mask2));
 
    // Specify Bands to topographically correct
    var bandList = ['blue','green','red','nir','swir1','swir2'];
    var compositeBands = img.bandNames();
    var nonCorrectBands = img.select(compositeBands.removeAll(bandList));
 
    var geom = ee.Geometry(img.get('system:footprint')).bounds().buffer(10000);
 
    function apply_SCSccorr(band){
      var method = 'SCSc';
      var out = img_plus_ic_mask2.select('IC', band).reduceRegion({
      reducer: ee.Reducer.linearFit(), // Compute coefficients: a(slope), b(offset), c(b/a)
      geometry: ee.Geometry(img.geometry().buffer(-5000)), // trim off the outer edges of the image for linear relationship
      scale: 300,
      maxPixels: 1000000000
      });  
 
   if (out === null || out === undefined ){
       return img_plus_ic_mask2.select(band);
       }
 
  else{
      var out_a = ee.Number(out.get('scale'));
      var out_b = ee.Number(out.get('offset'));
      var out_c = out_b.divide(out_a);
      // Apply the SCSc correction
      var SCSc_output = img_plus_ic_mask2.expression(
        "((image * (cosB * cosZ + cvalue)) / (ic + cvalue))", {
        'image': img_plus_ic_mask2.select(band),
        'ic': img_plus_ic_mask2.select('IC'),
        'cosB': img_plus_ic_mask2.select('cosS'),
        'cosZ': img_plus_ic_mask2.select('cosZ'),
        'cvalue': out_c
      });
 
      return SCSc_output;
    }
 
    }
 
    var img_SCSccorr = ee.Image(bandList.map(apply_SCSccorr)).addBands(img_plus_ic.select('IC'));
    var bandList_IC = ee.List([bandList, 'IC']).flatten();
    img_SCSccorr = img_SCSccorr.unmask(img_plus_ic.select(bandList_IC)).select(bandList);
 
    return img_SCSccorr.addBands(nonCorrectBands)
      .setMulti(props)
      .set('system:time_start',st);
  }
 
}  
 
var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR");
 
var inBands = ee.List(['B2','B3','B4','B5','B6','B7'])
var outBands = ee.List(['blue','green','red','nir','swir1','swir2']);
var collection = l8.filterBounds(geometry)
                   .filterDate("2017-01-01","2017-12-31")
                   .sort("CLOUD_COVER")
                   .select(inBands,outBands);
 
var img = ee.Image(collection.first());
print(img)
var collection = terrainCorrection(collection);
var newimg = ee.Image(collection.first())
 
Map.addLayer(ee.Image(newimg),{ bands: 'red,green,blue',min: 0, max: 3000},'corrected');
Map.addLayer(ee.Image(img),{ bands: 'red,green,blue',min: 0, ma
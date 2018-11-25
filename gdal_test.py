from gzip import GzipFile #pip install gzip-reader
from io import BytesIO
from uuid import uuid4
# from gdalconst import GA_ReadOnly
from osgeo import gdal #pip install pygdal
from timeit import default_timer as timer
from datetime import datetime, timedelta
from urllib.request import urlopen, URLError, Request
import numpy as np
from osgeo.gdalconst import *
import sys
import struct

#link contendo arquivo grib2
link = 'http://ftp.cptec.inpe.br/modelos/tempo/WRF/ams_05km/brutos/2018/11/23/00/WRF_cpt_05KM_2018112300_2018112612.grib2'
#nome do arquivo grib2 local
file = 'WRF_cpt_05KM_2018112100_2018112412.grib2'

#rotina de aquisição do conteúdo do arquivo
def open_gdal(url):
	"""Function for request and treatment of content of a URL.

	Parameters
	----------
	url : str
		URL to be read and whose content will be get.

	Function
	--------
	Request(url : str, headers : dict) > urllib.request.Request
		Request of URL to accept gzip encoding
	urlopen(url : str) > http.client.HTTPResponse
		Read the content of URL
	BytesIO()
	GzipFile(fileobj : )

	Methods
	-------
	read() > 
		Returns a 
	info().get(string : str) > str
		Get the content of string in dictionary of object attached  

	"""
	try:
		request = Request(url, 
			headers={"Accept-Encoding": "gzip"})
		response = urlopen(url)
		#arquivo passado de forma compactada de forma a diminuir o tempo
		if response.info().get('Content-Encoding') == 'gzip': #se encoding do response for gzip
			#abre o conteuo do response como buffer e zipa
			image_data = GzipFile(fileobj=BytesIO(response.read()))
		else:
			image_data = response

		mmap_name = "/vsimem/"+uuid4().hex #lugar na memoria
		
		gdal.FileFromMemBuffer(mmap_name, image_data.read()) #alocado em memoria
		print(type(mmap_name))
		dataset = gdal.Open(mmap_name) #abre o arquivo em memoria 
		#lista = load_geo(dataset) #carrega as coordenadas
		#data = dataset.find_band_number(lista = lista) #carrega os dados do dataset dada as coord
		if dataset is not None:
			return dataset
		else:
			print("Error dataset empty")
			sys.exit(1)

	except URLError:
		return 'None'

	
def find_band_number(dataset):
	'''
	Finds the band number inside the GRIB file, given the variable and the level names
	'''
	array = []
	content = ['84 hr Total precipitation']#'Precipitation', 'precipitation']
	content_element = 'APCP84'

	for i in range(1,dataset.RasterCount + 1):
		band = dataset.GetRasterBand(i)
		metadata = band.GetMetadata()
		band_level = metadata['GRIB_SHORT_NAME']
		band_variable = metadata['GRIB_ELEMENT']
		band_comment = metadata['GRIB_COMMENT']
		#if any(word in band_comment for word in content):
		if band_variable == content_element:
			array.append({
				'indice':i,
				'comment': band_comment,
				#'shortname': band_level,
				'element':band_variable
			})

	return array

def pt2fmt(pt): #retorna letra correspondente ao datatype
	fmttypes = {
		GDT_Byte: 'B',
		GDT_Int16: 'h',
		GDT_UInt16: 'H',
		GDT_Int32: 'i',
		GDT_UInt32: 'I',
		GDT_Float32: 'f',
		GDT_Float64: 'd' #double
		}
	return fmttypes.get(pt, 'x')

def latlon_value(ds,n_band,lat,lon):
	#lat,lon = lista
	transf = ds.GetGeoTransform() #matriz de transformacao
	cols = ds.RasterXSize	#colunas - pixels
	rows = ds.RasterYSize	#linhas - pixels
	bands = ds.RasterCount  #numero de bandas
	band = ds.GetRasterBand(n_band) #conteudo da banda
	bandtype = gdal.GetDataTypeName(band.DataType) #datatype da banda
	driver = ds.GetDriver().LongName #tipo do arquivo

	# Make Inverse Geotransform  (try:except due to gdal version differences)
	try:
		success, transfInv = gdal.InvGeoTransform(transf) #nao sei o que e esse success
	except:
		transfInv = gdal.InvGeoTransform(transf) #obtem inversa da matriz de transf

	px, py = gdal.ApplyGeoTransform(transfInv, lon, lat) #obtem os pixel x,y de lat,lon
	structval = band.ReadRaster(int(px), int(py), 1,1, buf_type = band.DataType ) #valor
	fmt = pt2fmt(band.DataType) #formato
	intval = struct.unpack(fmt , structval) #unpack do valor 

	return intval

def allLatLonValues(ds, description):
	data = []
	for lat in np.arange(-55.0, 12+0.05, 0.05):# -55.0 ~ 12.0
		for lon in np.arange(272.0, 332.0, 0.05):# 272.0 ~ 332.0
			for item in data_description:
				value = latlon_value(dataset, item['indice'], lat,lon)
				data.append({
						#'comment':item['comment'],
						'shortname': item['element'],
						##########comment#############
						'latlon': (round(lat,2),round(lon - 360,2)),
						'value': round(value[0],1)
						})
	return data

def locationValue(ds, lat, lon, description):
	data = []
	for item in description:
		value = latlon_value(dataset, item['indice'], lat, lon)
		data.append({
				#'comment':item['comment'],
				'shortname': item['element'],
				'latlon': (round(lat,2),round(lon - 360,2)),
				'value': round(value[0],6)
				})
	return data

if __name__ == '__main__':
	start = timer()
	print(datetime.now())

###gdal link###
	#dataset = open_gdal(link) #retorna o dataset
###gdal file###
	dataset = gdal.Open(file, GA_ReadOnly) #abre o arquivo em read only

	data_description = find_band_number(dataset) #filtra o dataset
#get all values 
	data = allLatLonValues(ds=dataset, description=data_description)

#get a specific value (lat,lon)
	# lat = float(input("latitude:"))
	# lon = float(input("longitude:")) + 360
	# data = locationValue(ds=dataset, lat=lat, lon=lon, description=data_description)
	
	end = timer()
	sec = end - start
	print(str(timedelta(seconds = sec)))
	print(datetime.now())
	#dataset = open_dataset(GdalStore(mmap_name))

	for i in data:
		print(i)
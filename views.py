from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from forms import MessageForm
import math
from zipfile import *
import shutil
import os
import requests
import json
from os import listdir
from os.path import isfile, join
import qrcode

glob_id = 20

def API(request):
	s = ""
	if request.method == 'GET':
		resp = HttpResponse()
		resp.status_code = 200
		s+="<html>"
		s+="<body>"
		s+="<p style=\"text-align: center\">Gucci Gang</p>"
		s+="</body></html>"
		resp.write(s)
		return resp

	resp = HttpResponse()
	resp.status_code = 204
	resp.write('We need a request')
	return resp

def mydevices(request):
	if request.method == 'GET':
		name = str(request.GET.get('name'))
	onlyfiles = [f for f in listdir('mytestsite/mytestsite/'+name) if isfile(join('mytestsite/mytestsite/'+name, f))]
	resp = HttpResponse()
	resp.status_code = 200
	for fl in onlyfiles:
		f = open('mytestsite/mytestsite/'+name + '/' +fl,'r')
		s = f.read().split('\n')
		resp.write(fl[:-4]+ ' ' + s[0] +' '+ s[2] + ' ')
	return resp

"""def newdevice(request):
	name = str(request.GET.get('name'))
	type1 = str(request.GET.get('type'))
	data = str(request.GET.get('data'))
	id1 = str(request.GET.get('id'))
	newfile
	return request"""
def add_device(request):
	name = str(request.GET.get('name'))
	id1 = str(request.GET.get('id'))
	shutil.move(r'mytestsite/mytestsite/unsorted/'+id1 + '.txt', r'mytestsite/mytestsite/'+name)
	print('mytestsite/mytestsite/unsorted/'+id1 + '.txt')
	resp = HttpResponse()
	resp.status_code = 204
	resp.write('We need a request')
	return resp

def dist(request):
	lon=str(request.GET.get('lon'))
	lat=str(request.GET.get('lat'))
	num = 1000
	v = 1.7
	a = open('list.txt','r')
	q = a.read().split(' ')
	a.close()
	n = []
	for c in q[:-1]:
		j = []
		l = c.split(',')
		j.append(float(l[0]))
		j.append(float(l[1]))
		n.append(j)
	m = []
	for t in n:
		if ((float(lon)-0.05395684)<t[0]) and (t[0]<(float(lon)+0.05395684)):
			m.append(t)
	r = []
	for t in m:
		if ((float(lat)-0.05395684)<t[1]) and (t[1]<(float(lat)+0.05395684)):
			r.append(t)
	min = 10.00000
	for t in r:
		dist  = math.sqrt( (t[0] - float(lon))**2 + (t[1] - float(lat))**2 )
		if dist < min:
			min = dist
	resp = HttpResponse()
	resp.status_code = 200
	if min*111.2 < 6.00:
		resp.write('Источник энергии: ЛЭП\n')
		resp.write('Длина ЛЭП: '+str(round(min*111.2,2)) + ' км\n')
		resp.write('Стоимость ЛЭП: '+str(round((min*111.2)*1.2,2))+' млн.р.\n')
		return resp
	else:
		resp.write(str(round(min*111.2,2))+"   ")
		print('https://maps.googleapis.com/maps/api/place/textsearch/json?query=river&radius=5000&language=ru&opennow&location='+lat+','+lon+'&key=AIzaSyDMkPyS3cWd1qIDDXYQHSLJ4PrV6ILkgVw')
		r = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query=river&radius=5000&language=ru&opennow&location=55.711319,37.595655&key=AIzaSyDMkPyS3cWd1qIDDXYQHSLJ4PrV6ILkgVw')
		print(r.text)
		d = json.loads(r.text)
		lat1 = d['results'][0]['geometry']['location']['lat']
		lon1 = d['results'][0]['geometry']['location']['lng']
		dist  = math.sqrt( (float(lat1) - float(lon))**2 + (float(lon) - float(lat))**2 )
		resp.write(str(round(dist*111.2,2)))
		if round(dist*111.2,2)<3.5:
			resp.write('Источник энергии: ГЭС\n')
			resp.write('Вид ГЭС: Напорная')
			resp.write('Мощность ГЭС: '+str(round((num/(1.5*v*v*v*0.2)+1)*(1.5*v*v*v*0.2),2)) + ' КВт\n')
			resp.write('Стоимость ГЭС: '+str(floor(num/(1.5*v*8)+1,2)*46)+' т.р.\n')
			resp.write('Длина ЛЭП: '+str(floor(dist*111.2,2))+' км\n')
			resp.write('Стоимость ЛЭП: '+str(round((dist*111.2)*1.2,2))+' млн.р.\n')
		return resp

def reg(request):
	if request.method == 'GET':
		name = str(request.GET.get('name'))
		if not os.path.exists('mytestsite/mytestsite/' + name):
			os.makedirs('mytestsite/mytestsite/'+name)
	resp = HttpResponse()
	resp.status_code = 200
	resp.write('We need a request')
	return resp

def form(request):
	return render_to_response('form.html',{})

def qr(request):
	if request.method == 'GET':
		name = str(request.GET.get('name'))
		type1 = str(request.GET.get('type'))
		data = str(request.GET.get('data'))
		ip = str(request.GET.get('ip'))
		num = 0
		num  = int(request.GET.get('number'))
		for i in range(0,num):
			f = open('mytestsite/mytestsite/unsorted/'+name + str(i) + ".txt","w")
			f.write(type1 + '\n' + data + '\n' + ip)
			f.close()
		img = qrcode.make(name+str(i))
		img.save('mytestsite/mytestsite/static/active.png')
		zip = ZipFile('mytestsite/mytestsite/static/zip.zip',"w");
		for i in range(0,num):
			img = qrcode.make(name+str(i))
			img.save('mytestsite/mytestsite/static/'+ name+str(i)+'.png')
			zip.write('mytestsite/mytestsite/static/'+ name+ str(i) +'.png',name+str(i)+'.png')
			os.remove('mytestsite/mytestsite/static/'+ name+str(i)+'.png')
		zip.close()
		return render_to_response('qr.html', {})

	resp = HttpResponse()
	resp.status_code = 204
	resp.write('We need a request')
	return resp
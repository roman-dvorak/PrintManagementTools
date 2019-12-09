from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
from flask import redirect
from flask import url_for
import glob
#from flask_security import Security, SQLAlchemyUserDatastore, \
#    UserMixin, RoleMixin, login_required

import json

import time
import datetime
import os
import sys

import requests



class server():
    def __init__(self):
        print("Start server")

        self.app = Flask('PrintManagementTolls', template_folder='PrintManagementTools/templates')
        self.start()

        self.meta = {
            'current': os.path.realpath(os.path.dirname(__file__)+'/../../../../'),
        }
        print("META", self.meta)

        self.cfg = {
            'src':{
                'stl': 'STL',
                'openscad': 'src',
                'gcode': 'gcode',
                'images': 'images',
            },
            '4printing':{
                'stl': 'STL/4printing',
                'gcode': 'src/4printing',
                'im,ages': 'images/4printing',
            },
            'blades':{
                'stl': 'STL/blades',
                'gcode': 'src/blades',
                'images': 'images/blades',
            }
        }

        self.app.config['TEMPLATES_AUTO_RELOAD'] = True
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = True
        self.app.config['ENV'] = "development"
        self.app.run(host="0.0.0.0", port=9006)



    def start(self):

        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/rep/<path:path>', 'resource', self.get_resource)


    def index(self):
        print(request)
        print(request.json)
        print(request.data)

        data = {}
        path = "../../../"+self.cfg['src']['openscad']+'/*.scad'
        for scad in glob.glob(path):
            print(scad)
            scad = '/'+os.path.abspath(glob.glob(scad)[0])[1:]
            print(scad)
            scad_modif = os.path.getmtime(scad)
            data[os.path.basename(scad)] = {}
            data[os.path.basename(scad)]['scad'] = scad
            data[os.path.basename(scad)]['scad_modif'] = scad_modif
            data[os.path.basename(scad)]['stl_modif'] = 0
            data[os.path.basename(scad)]['image_modif'] = 0
            data[os.path.basename(scad)]['gcode_modif'] = 0

            print(scad)
            image = "../../../"+self.cfg['src']['images'] + '/'+ os.path.splitext(os.path.basename(scad))[0] + '.*'
            try:
                image = os.path.abspath(glob.glob(image)[0])[1:]
                image_modif = os.path.getmtime('/'+image)
                print("TIME", os.path.getmtime('/'+image))
            except Exception as e:
                print('err', e)

            gcode = "../../../"+self.cfg['src']['gcode'] + '/'+ os.path.splitext(os.path.basename(scad))[0] + '.*'
            try:
                gcode = os.path.abspath(glob.glob(gcode)[0])[1:]
                gcode_modif = os.path.getmtime('/'+gcode)
                print("TIME", os.path.getmtime('/'+gcode))
            except Exception as e:
                print('err', e)


            stl = "../../../"+self.cfg['src']['stl'] + '/'+ os.path.splitext(os.path.basename(scad))[0] + '.*'
            try:
                stl = os.path.abspath(glob.glob(stl)[0])[1:]
                stl_modif = os.path.getmtime('/'+stl)
            except Exception as e:
                print('err', e)



            data[os.path.basename(scad)]['stl'] = stl
            data[os.path.basename(scad)]['image'] = image
            data[os.path.basename(scad)]['gcode'] = gcode
            data[os.path.basename(scad)]['stl_modif'] = stl_modif
            data[os.path.basename(scad)]['image_modif'] = image_modif
            data[os.path.basename(scad)]['gcode_modif'] = gcode_modif
            data[os.path.basename(scad)]['scad_ready'] = True
            data[os.path.basename(scad)]['stl_ready'] = stl_modif > scad_modif
            data[os.path.basename(scad)]['image_ready'] = (stl_modif > scad_modif) and (image_modif > stl_modif)
            data[os.path.basename(scad)]['gcode_ready'] = (stl_modif > scad_modif) and (gcode_modif > stl_modif)



        return render_template('dataset.html', title='Home', data = data, meta = self.meta)

    def get_resource(self, path):  # pragma: no cover
        mimetypes = {
            ".css": "text/css",
            ".html": "text/html",
            ".js": "application/javascript",
        }
        complete_path = os.path.join('/',path)
        # ext = os.path.splitext(path)[1]
        print(complete_path)
        # mimetype = mimetypes.get(ext, "text/html")
        # content = get_file(complete_path)
        # return Response(content, mimetype=mimetype)

        return send_file(complete_path)

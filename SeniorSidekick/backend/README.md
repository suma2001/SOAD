# Setting Up

You need to have GDAL and postgis libraries inorder to run this...
I assume you already have postgresql installed and running as backend.
### Installing Postgis

You should have postgis and psycopg2 installed in your laptop.

```
$ pip install psycopg2
$ pip install postgis
```

In **settings.py** the database has been changed to 
```
DATABASES = {
'ENGINE': 'django.contrib.gis.db.backends.postgis',
'NAME': 'postgres',
...
}
```
### Installing  GDAL

GDAL is a must for Spatial domain applications.
The spatial indexing is done with the help of GDAL and postgis.

You can download GDAL here:
https://www.gisinternals.com/release.php

You need to add some changes on your PC inorder to run it you can go through the tutorial here:
https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows

After installing GDAL:
    - Go to your GDAL folder usually located at "C:\OSGeo4W64"
    - Now go to "C:\OSGeo4W64\bin" and search for **gdal300.dll** or **gdal204.dll**
    - Now you have the path go to settings.py and go for **GDAL path** area. 
     It looks like this:
     
    
       if os.name == 'nt':
            import platform
            OSGEO4W = r"C:\OSGeo4W"
            if '64' in platform.architecture()[0]:
                OSGEO4W += "64"
   
Now search modify the GDAL_LIBRARY_PATH to your **gdal300.dll** or **gdal204.dll** path.

#### Getting Nearest Volunteers
Nearest volunteers for a given Elder can be achieved with the URL 'api/volunteers/<Elder.id>'.
This will get all the available nearest volunteers under 1 degrees radius i.e 111 KM.
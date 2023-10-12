import math
import skyfield
from skyfield.api import load, wgs84, EarthSatellite
from datetime import datetime, date, time, timezone,timedelta
import time
from sgp4.api import Satrec, WGS72
import numpy as np
import pandas as pd

t0 = time.time()
ts = load.timescale()
#eph = load('de440s.bsp')
'''
line1 = '1 47665U 21012AX  21272.30279966 -.00000621  00000-0 -22708-4 0  9994'
line2 = '2 47665  53.0498 129.8040 0004522 230.8365 129.2222 15.06392491 35809'
satellite = EarthSatellite(line1, line2, 'STARLINK-2056')
print(satellite.epoch.utc_jpl())

line1 = '1 48772U 21045F   21272.91668981  .00000013  00000-0  00000+0 0  9995'
line2 = '2 48772  87.9070 241.4122 0000768 106.2897 125.2909 13.16057538 19233'
satellite2 = EarthSatellite(line1, line2, 'ONEWEB-0242')
print(satellite2.epoch.utc_jpl())
'''
since = datetime(1949, 12, 31, 0, 0, 0)
start = datetime(2020, 12, 21, 0, 0, 0)
epoch = (start-since).days
inclination = 53*2*np.pi/360
GM = 3.9860044e14
R = 6371393
altitude = 550000
mean_motion = np.sqrt(GM/(R+altitude)**3)*60
#print(mean_motion)
#step = timedelta(minutes=10)
#step_num = 144*365
num_of_orbit = 72
sat_per_orbit = 22
num_of_sat = num_of_orbit*sat_per_orbit
F = 1
for i in range(num_of_orbit):
    raan = i * 2 * np.pi / num_of_orbit
    for j in range(sat_per_orbit):
        mean_anomaly = (j * 360 / sat_per_orbit + i * 360 * F / num_of_sat ) % 360 * 2 * np.pi / 360
        satrec = Satrec()
        satrec.sgp4init(
            WGS72,              # gravity model
            'i',                # 'a' = old AFSPC mode, 'i' = improved mode
            i*sat_per_orbit+j,  # satnum: Satellite number
            epoch,              # epoch: days since 1949 December 31 00:00 UT
            2.8098e-05,         # bstar: drag coefficient (/earth radii)
            6.969196665e-13,    # ndot: ballistic coefficient (revs/day)
            0.0,                # nddot: second derivative of mean motion (revs/day^3)
            0.0,          # ecco: eccentricity
            0.0,    # argpo: argument of perigee (radians)
            inclination,    # inclo: inclination (radians)
            mean_anomaly,    # mo: mean anomaly (radians)
            mean_motion,    # no_kozai: mean motion (radians/minute)
            raan,    # nodeo: right ascension of ascending node (radians)
        )
        sat = EarthSatellite.from_satrec(satrec, ts)
        # timeslot 1min, last for 1 day
        t_ts = ts.utc(2021, 6, 21, 0, range(60*24))
        geocentric = sat.at(t_ts)
        result = pd.DataFrame()
        subpoint = wgs84.subpoint(geocentric)
        result['lat'] = subpoint.latitude.degrees
        result['lon'] = subpoint.longitude.degrees
        result['alt'] = subpoint.elevation.km

        #sunlight = geocentric.is_sunlit(eph)
        #result['sunlight'] = sunlight
        #result = result.astype('int')
        result.to_csv('starlink_72_22_summer/%d.csv'%(sat.model.satnum),index=False)
        #subpoint = wgs84.subpoint(geocentric)
        print(sat.model.satnum)
        #print(geocentric.position.km)
        #print(subpoint.latitude.degrees)
        #print(subpoint.longitude.degrees)
        #print(subpoint.elevation.km)
        #print('{} \tLatitude:{} \tLongitude:{} \t Height: {:.5f} km'.format(t_ts.utc_iso(),subpoint.latitude.degrees, subpoint.longitude.degrees,subpoint.elevation.km ))
    
t1 = time.time()
print('time:',t1-t0)



# lines = [
# 'STARLINK-2056           ',
# '1 47665U 21012AX  21272.30279966 -.00000621  00000-0 -22708-4 0  9994',
# '2 47665  53.0498 129.8040 0004522 230.8365 129.2222 15.06392491 35809',
# 'ONEWEB-0242             ',
# '1 48772U 21045F   21272.91668981  .00000013  00000-0  00000+0 0  9995',
# '2 48772  87.9070 241.4122 0000768 106.2897 125.2909 13.16057538 19233',
# ]

# sat = ephem.readtle(lines[0],lines[1],lines[2])
# sat2 = ephem.readtle(lines[3],lines[4],lines[5])
# #cur_time = (now + datetime.timedelta(minutes=cur_min)).strftime("%Y-%m-%d %H:%M:%S")
# now = datetime.datetime.now()
# print(now)
# cur_time = (now).strftime("%Y-%m-%d %H:%M:%S")
# print(cur_time)
# for i in range(4,24):
#     aim_time = "2021-09-30 "+str(i)+":00:00"
#     sat.compute(aim_time)
#     print(str("%.4f"%(sat.elevation / 1000)))

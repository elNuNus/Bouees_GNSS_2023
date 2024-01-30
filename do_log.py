#!/usr/bin/env python3
"""
[description]
author : Pierre BOSSER
"""


import sys
import os

import numpy as np
import threading as th

sys.path.append(os.environ['LIB_PYTH'])
import gnsstime as gti

# Dev : Pierre B - version 2024-01-23

class logCfg():
  def __init__(self,fcfg=''):
    self.conf = {}
    if os.path.isfile(fcfg):
      self.read(fcfg)
    pass
  
  def read(self,fcfg):
    """
    name / dt / cmd / praw / nraw
    ubx , 3600, gpspipe -R, ./ubx/ , raw_%s.ubx
    nmea,   60, gpspipe -r, ./nmea/, raw_%s.nmea
    met ,   60, echo "met", ./met/ , raw_%s.met

    name : name of the data type to be recorded
    dt : duration of data per file
    cmd : shell command used to retrieve data
    praw : root directory in which the data will be stored (then yyyy/day-of-year)
    nraw : name of the recorded file; the character %s will allow to put a date in suffix
    """
    try:
      cfg = np.genfromtxt(fcfg,delimiter=',',dtype=str)
      for k in range(len(cfg)):
        name = cfg[k][0].strip()
        self.conf[name] = {}
        self.conf[name]['dt'] = int(cfg[k][1])
        self.conf[name]['cmd'] = cfg[k][2].strip()
        self.conf[name]['pout'] = cfg[k][3].strip()
        self.conf[name]['nout'] = cfg[k][4].strip()
        print('Load config '+cfg[k][0].strip()+': ok')
    except:
        print('Load config '+cfg[k][0].strip()+': error')

def log_raw_data(name, dt,cmd,praw,nraw):
  """
  Raw data recording, on files of duration dt, starting at a round date.
  Files are dated in GPS time (UTC+n s). If the file already exists, it is overwritten.

  dt : recording duration
  cmd : command whose standard output will be written to the output file
  praw : directory in which the data will be stored in yyyy/day
  nraw : name of the recording file in the form *%s.* where %s is a pattern for entering the recording date
  """
  tnow_utc = np.ceil(gti.now())
  tnow_gpst = gti.utc2gps(tnow_utc)
  print("GPST %s: log_raw_data %s"%(gti.sec2cal_str(tnow_gpst),name))
  while True:
    tnow_utc = np.ceil(gti.now())
    tnow_gpst = gti.utc2gps(tnow_utc)
    yyyy,mm,dd,h,m,s = gti.sec2cal(tnow_gpst)
    _, doy, _ = gti.sec2doy(tnow_gpst)
    # on recherche la durée d'acqusition nécessaire pour compléter jusqu'au dt "rond" suivant
    dtf = np.round(dt-(h*3600+m*60+s)%dt)
    # le nom du fichier log commence à dt rond
    nraw_date = nraw%(gti.sec2cal_str(tnow_gpst+dtf-dt))
    # on créé le répertoire de sortie
    praw_date = "%s/%04d/%03d/"%(praw,yyyy,doy)
    if not os.path.isdir(praw_date): os.makedirs(praw_date) 
    print("GPST %s: log_raw_data %s > %s/%s (dt=%d s)"%(gti.sec2cal_str(tnow_gpst),name,praw_date,nraw_date,dtf))
    # on lance la commande, elle s'arretera automatiquement à la fin du dt rond
    os.system('timeout %d %s > %s/%s'%(dtf,cmd,praw_date,nraw_date))

def zip_raw_data(name,dt,cmd,praw,nraw):
  """
  dt : recording duration
  cmd : command whose standard output will be written to the output file
  praw : directory in which the data will be stored in yyyy/day
  nraw : name of the recording file in the form *%s.* where %s is a pattern for entering the recording date
  """
  tnow_utc = np.ceil(gti.now())
  tnow_gpst = gti.utc2gps(tnow_utc)
  print("GPST %s: zip_raw_data %s"%(gti.sec2cal_str(tnow_gpst),name))
  while True:
    tnow_utc = np.ceil(gti.now())
    tnow_gpst = gti.utc2gps(tnow_utc)
    yyyy,mm,dd,h,m,s = gti.sec2cal(tnow_gpst)
    # si la date courante correspond à une date de début de log, on archive le dernier fichier créé (à -dt)
    # on recherche la durée d'acqusition nécessaire pour compléter jusqu'au dt "rond" suivant
    test = (h*3600+m*60+s)%dt
    if test != 0 : continue
    tzip = tnow_gpst-dt
    # On attend 10s que le fichier soit bien fermé
    os.system("sleep 10")
    # On récupère la date du fichier qui vient d'etre écrit
    nraw_date = nraw%(gti.sec2cal_str(tzip))
    yyyy,mm,dd,_,_,_ = gti.sec2cal(tzip)
    _, doy, _ = gti.sec2doy(tzip)
    praw_date = "%s/%04d/%03d/"%(praw,yyyy,doy)
    if os.path.isfile(praw_date+"/"+nraw_date):
      print("GPST %s: zip_raw_data %s > %s/%s"%(gti.sec2cal_str(tnow_gpst),name,praw_date,nraw_date))
      os.system('gzip %s/%s'%(praw_date,nraw_date))
  pass

def main():
  # Enregistrement des trames NMEA
  LOG_NMEA = False
  # Enregistrement des fichiers UBX
  LOG_UBX = True
  # Enregistrement des données météo
  LOG_MET = False
  
  log_cnf = logCfg()
  log_cnf.read("log.conf")
  print()
  # LOG NMEA #######################################################################################
  if LOG_NMEA:
    try:
      nmea = log_cnf.conf['nmea']
      thrd = th.Thread(target=log_raw_data,args=('nmea',nmea['dt'],nmea['cmd'],nmea['pout'],nmea['nout']))
      thrd.start()
      thrd = th.Thread(target=zip_raw_data,args=('nmea',nmea['dt'],nmea['cmd'],nmea['pout'],nmea['nout']))
      thrd.start()
    except:
      pass
  # LOG UBX ########################################################################################
  if LOG_UBX:
    try:
      ubx = log_cnf.conf['ubx']
      thrd = th.Thread(target=log_raw_data,args=('ubx',ubx['dt'],ubx['cmd'],ubx['pout'],ubx['nout']))
      thrd.start()
      thrd = th.Thread(target=zip_raw_data,args=('ubx',ubx['dt'],ubx['cmd'],ubx['pout'],ubx['nout']))
      thrd.start()
    except:
      pass
  # LOG MET ########################################################################################
  if LOG_MET:
    try:
      met = log_cnf.conf['met']
      thrd = th.Thread(target=log_raw_data,args=('met',met['dt'],met['cmd'],met['pout'],met['nout']))
      thrd.start()
      thrd = th.Thread(target=zip_raw_data,args=('met',met['dt'],met['cmd'],met['pout'],met['nout']))
      thrd.start()
    except:
      pass
if __name__ == "__main__":
  main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import datetime as dt


sec0 = dt.datetime(2000,1,1,12)
week0 = dt.datetime(1980,1,6,0)
secsInDay = 86400
secsInWeek = secsInDay*7
#leapseconds from https://www.ietf.org/timezones/data/leap-seconds.list
# mjd ls
ls = np.array([[2272060800.0/86400.0+15020,10],
               [2287785600.0/86400.0+15020,11],
               [2303683200.0/86400.0+15020,12],
               [2335219200.0/86400.0+15020,13],
               [2366755200.0/86400.0+15020,14],
               [2398291200.0/86400.0+15020,15],
               [2429913600.0/86400.0+15020,16],
               [2461449600.0/86400.0+15020,17],
               [2492985600.0/86400.0+15020,18],
               [2524521600.0/86400.0+15020,19],
               [2571782400.0/86400.0+15020,20],
               [2603318400.0/86400.0+15020,21],
               [2634854400.0/86400.0+15020,22],
               [2698012800.0/86400.0+15020,23],
               [2776982400.0/86400.0+15020,24],
               [2840140800.0/86400.0+15020,25],
               [2871676800.0/86400.0+15020,26],
               [2918937600.0/86400.0+15020,27],
               [2950473600.0/86400.0+15020,28],
               [2982009600.0/86400.0+15020,29],
               [3029443200.0/86400.0+15020,30],
               [3076704000.0/86400.0+15020,31],
               [3124137600.0/86400.0+15020,32],
               [3345062400.0/86400.0+15020,33],
               [3439756800.0/86400.0+15020,34],
               [3550089600.0/86400.0+15020,35],
               [3644697600.0/86400.0+15020,36],
               [3692217600.0/86400.0+15020,37]])
lsGPS = 19

class clock():
  def __init__(self):
    self.start = now()
    print(self)
    
  def __str__(self):
    return '%.3f'%(now() - self.start)

class GnssTime:
  def __init__(self,yyyy_in=1,mm_in=1,dd_in=1,h_in=0,m_in=0,s_in=0):
    self._t = np.nan

  def sec(self):
    dt_sec0=self._t-sec0
    sec=dt_sec0.days*secsInDay+dt_sec0.seconds+dt_sec0.microseconds*1e-6
    return sec
  
  def mth(self):
    year=self._t.year
    month = self._t.month
    day = self._t.day
    
    dt_day=self._t-dt.datetime(self._t.year,self._t.month,self._t.day)
    secd=dt_day.seconds+dt_day.microseconds*1e-6
    
    next_month = self._t.replace(day=28) + dt.timedelta(days=4)  # this will never fail
    day_in_month = (next_month - dt.timedelta(days=next_month.day)).day
    mth = month + (day + secd/86400)/(day_in_month +1)-1
    return year, mth
  
  def doy(self):
    dt_doy0=self._t-dt.datetime(self._t.year,1,1)+dt.timedelta(days=1)
    year=self._t.year
    doy=dt_doy0.days
    secd=dt_doy0.seconds+dt_doy0.microseconds*1e-6
    return year,doy,secd

  def week(self):
    dt_week0=self._t-week0
    week=np.floor(dt_week0.days*secsInDay/secsInWeek)
    secw=dt_week0.seconds+dt_week0.days*secsInDay-week*secsInWeek+dt_week0.microseconds*1e-6
    return week,secw

  def cal(self):
    return self._t.year,self._t.month,self._t.day,self._t.hour,self._t.minute,self._t.second+self._t.microsecond*1e-6

  def jd(self):
    yyyy = self._t.year
    mm = self._t.month
    dd = self._t.day
    h = self._t.hour
    m = self._t.minute
    s = self._t.second+self._t.microsecond*1e-6

    if mm<=2:
      mm = mm+12
      yyyy = yyyy-1

    C = np.floor(yyyy / 100)
    B = 2 - C + np.floor(C / 4)
    T = h / 24 + m / 1440 + s / 86400
    return np.floor(365.25 * ( yyyy + 4716 ) ) + np.floor( 30.6001 * ( mm + 1  ) ) + dd + T + B - 1524.5

  def mjd(self):
    return self.jd()-2400000.5

  def gst(self):
    # source : http://aa.usno.navy.mil/faq/docs/GAST.php
    jd = self.jd()
    jd0 = np.floor(jd)+0.5
    d = jd - 2451545.0
    d0 = jd0 - 2451545.0
    h = 24 * (jd-jd0)
    
    t = d/36525.0
    gmst = np.mod(6.697374558 + 0.06570982441908 * d0  + 1.00273790935 * h + 0.000026 * t * t, 24.0)
    # The following alternative formula can be used with a loss of precision of 0.1 second per century
    #~ gmst = np.mod(18.697374558 + 24.06570982441908*d, 24.0)
    
    # Computing Equation of Equinoxes
    deg2rad = np.pi / 180
    Omega = 125.04 - 0.052954 * d # Longitude of the ascending node of the Moon
    L = 280.47 + 0.98565 * d # Mean Longitude of the Sun
    epsilon = 23.4393 - 0.0000004 * d # obliquity
    Delta_psi = -0.000319 * np.sin (Omega*deg2rad) - 0.000024 * np.sin (2*L*deg2rad) # nutation in longitude
    eqeq = Delta_psi * np.cos(epsilon * deg2rad)
    # Computing gast
    gast=np.mod(gmst + eqeq,24.0);
    return gmst,gast

  def __str__(self):
    return str(self._t)

  def from_date(self,yyyy_in,mm_in,dd_in,h_in=0,m_in=0,s_in=0,mus_in=0):
    mus_in = (s_in - int(s_in))*1e6
    self._t=dt.datetime(int(yyyy_in),int(mm_in),int(dd_in),int(h_in),int(m_in),int(s_in), int(mus_in))

  def from_doy(self,yyyy_in,doy_in,secd_in):
    mus = (secd_in-np.floor(secd_in))*1e6
    self._t=dt.datetime(int(yyyy_in),1,1)+dt.timedelta(seconds=(int(doy_in)-1)*secsInDay+int(secd_in+0.5), microseconds = mus)

  def from_sec(self,sec_in):
    self._t=sec0+dt.timedelta(seconds=float(sec_in))

  def from_week(self,week_in,secw_in):
    mus = (secw_in-np.floor(secw_in))*1e6
    self._t=week0+dt.timedelta(seconds=secsInWeek*week_in+np.floor(secw_in), microseconds = mus)

  def from_datetime(self,t):
    self._t = t;

  def from_datetime64(self,t_64):
    t_64_array = np.array(t_64,dtype = 'datetime64[s],i4')
    self._t = t_64_array.astype(object)    

  def from_mjd(self, mjd):
    self._t=dt.datetime(1858,11,17)+dt.timedelta(days=mjd)
    
  def get_t(self):
    return self._t

  def set_t(self,t_in):
    self._t=t_in

def gps2utc(secgps):
  idx = np.where(sec2mjd(secgps)-ls[:,0]>=0)[0]
  if len(idx)==0:return secgps
  secutc = secgps - ls[idx[-1],1] + lsGPS
  return secutc

def utc2gps(secutc):
  idx = np.where(sec2mjd(secutc)-ls[:,0]>=0)[0]
  if len(idx)==0:return secutc
  secgps = secutc + ls[idx[-1],1] - lsGPS
  return secgps

def now():
  t=GnssTime()
  t.from_datetime(dt.datetime.now())
  return t.sec()
  
def utcnow():
  t=GnssTime()
  t.from_datetime(dt.datetime.utcnow())
  return t.sec()

def sec2jd(sec):
  t=GnssTime()
  t.from_sec(sec)
  return t.jd();

def sec2mjd(sec):
  t=GnssTime()
  t.from_sec(sec)
  return t.mjd();

def sec2gmst(sec):
  t=GnssTime()
  t.from_sec(sec)
  return t.gst()[0];

def sec2gast(sec):
  t=GnssTime()
  t.from_sec(sec)
  return t.gst()[1];

def sec2cal(sec):
  t=GnssTime()
  t.from_sec(sec)
  return t.cal();

def cal2sec(yyyy=2000,mm=1,dd=1,h=0,m=0,s=0):
  t=GnssTime()
  if yyyy>2080: yyyy -= 100
  if mm>12: yyyy+=1; mm-=12
  t.from_date(yyyy,mm,dd,h,m,s)
  return t.sec();

def doy2sec(yyyy,doy,secd=0):
  t=GnssTime()
  doy=float(doy)
  if secd == 0:
    secd=(doy-int(doy))*86400
    doy = int(doy)
  t.from_doy(yyyy,doy,np.round(secd))
  return t.sec()

def mjd2sec(mjd):
  t=GnssTime()
  t.from_mjd(mjd)
  return t.sec()

def sec2dt64(sec):
  dt64 = np.datetime64("2000-01-01T12Z") + np.timedelta64(int(sec*1e6), 'us')
  return dt64

def sec2mth(sec):
  """ returns month + year in decimal : 0->11.9999999 """
  t=GnssTime()
  t.from_sec(sec)
  return t.mth()

def secfloor(sec):
  t=GnssTime()
  t.from_sec(sec)
  yyyy, doy, _ = t.doy()
  return doy2sec(yyyy,doy)
  
def secfloor_h(sec):
  t=GnssTime()
  t.from_sec(sec)
  yyyy, mm, dd, h, _, _ = t.cal()
  return cal2sec(yyyy, mm, dd, h,0,0)
  
def secceil(sec):
  t=GnssTime()
  t.from_sec(sec)
  yyyy, doy, _ = t.doy()
  return doy2sec(yyyy,doy+1)

def secceil_h(sec):
  t=GnssTime()
  t.from_sec(sec)
  yyyy, mm, dd, h, _, _ = t.cal()
  return cal2sec(yyyy, mm, dd,h,0,0)+3600
  
def sec2doy(sec):
  t=GnssTime()
  t.from_sec(sec)
  return t.doy()

def sec2cal_str(sec):
  t=GnssTime()
  t.from_sec(sec)
  yyyy, mm, dd, h, m, s = t.cal()
  str_out = "%04d%02d%02d_%02d%02d%02d"%(yyyy, mm, dd, h, m, s)
  return str_out

def sec2cal_str_full(sec):
  t=GnssTime()
  t.from_sec(sec)
  yyyy, mm, dd, h, m, s = t.cal()
  str_out = "%04d-%02d-%02d %02d:%02d:%02d"%(yyyy, mm, dd, h, m, s)
  return str_out
  
def sec2doy_str(sec):
  t=GnssTime()
  t.from_sec(sec)
  (yyyy,doy,secd)=t.doy()
  str_out="%04d-%05.1f" % (yyyy,doy+secd/86400)
  return str_out

def sec2doy_str_(sec):
  t=GnssTime()
  t.from_sec(sec)
  (yyyy,doy,secd)=t.doy()
  str_out="%04d_%03d" % (yyyy,doy)
  return str_out

def sec2hms_str(sec):
  t=GnssTime()
  t.from_sec(sec)
  (yyyy,mm,dd,h,m,s)=t.cal()
  str_out="%02d:%02d:%02d" % (h,m,s)
  return str_out
  
def cal_str_full2sec(cal_str_full):
  yyyy = int(cal_str_full[0:4])
  mm = int(cal_str_full[5:7])
  dd = int(cal_str_full[8:10])
  h = int(cal_str_full[11:13])
  m = int(cal_str_full[14:16])
  s = float(cal_str_full[17:])
  if yyyy == 0: yyyy = 2100
  if mm == 0: mm = 12
  if dd == 0: dd = 31
  if yyyy == 0: yyyy = 2100
  if yyyy == 0: yyyy = 2100
  return cal2sec(yyyy,mm,dd,h,m,s)

def sec2ws(sec):
  t=GnssTime()
  t.from_sec(sec)
  return t.week()
  
def ws2sec(w,s):  
  t=GnssTime()
  t.from_week(w,s)
  return t.sec()

def sec2yyyy(sec):
  (yyyy,doy,secd)=sec2doy(sec)
  doy_in_year = sec2doy(doy2sec(yyyy+1,0,0))[1]
  return yyyy+(doy+secd/86400-1)/doy_in_year

def yy2yyyy(yy):
  yyyy = 2000+yy
  if yy >= 50: yyyy = 1900+yy
  return yyyy

def yyyy2yy(yyyy):
  yy = yyyy-2000
  if yy < 0: yy +=100
  return yy

def get_lst_mth(secdeb,secfin):
  lst_sec_mth = []
  for sec in np.arange(secdeb, secfin+86400, 86400):
    t=GnssTime()
    t.from_sec(sec)
    yyyy, mth = t.mth()
    sec_mth = cal2sec(yyyy,np.ceil(mth),1)
    if not sec_mth in lst_sec_mth: lst_sec_mth.append(sec_mth)
  return lst_sec_mth

def get_last_day(sec):
  yyyy, mm, _, _, _, _ = sec2cal(sec)
  yyyy_next, mm_next, _, _, _, _ = sec2cal(cal2sec(yyyy,mm,28)+4*86400)
  return cal2sec(yyyy_next, mm_next, 1)-86400

def mk_ticks_from_sec(ntick, sec1, sec2, format_tick):
  tick_label=np.chararray(ntick,10,unicode=True)
  tick=np.linspace(sec1,sec2,ntick)
  for i in range(tick.shape[0]):
    if format_tick == "yyyy-doy":
      tick_label[i] = sec2doy_str(tick[i])
    elif format_tick == "hh:mm:ss":
      tick_label[i] = sec2hms_str(tick[i])
  return tick,tick_label

def get_time_ticks(limx,nticks=-1):
  ndays = np.ceil((limx[1]-limx[0])/86400)+1
  if ndays <= 2:
    if nticks == -1:
      (xticks,xtick_labels)=mk_ticks_from_sec(5,limx[0],limx[1],"hh:mm:ss")
    else:
      (xticks,xtick_labels)=mk_ticks_from_sec(nticks,limx[0],limx[1],"hh:mm:ss")
  else :
    yyyy, doy, _ = sec2doy(limx[0])
    sta = doy2sec(yyyy, doy)
    if nticks == -1: nticks = 6
    if ndays<6:
      ddoy = 0.5
      sto = doy2sec(yyyy, doy+ddoy*(nticks-1))
      (xticks,xtick_labels)=mk_ticks_from_sec(nticks,sta, sto,"yyyy-doy")
    else:
      ddoy = np.floor(ndays/(nticks-1))
      sto = doy2sec(yyyy, doy+ddoy*(nticks-1))
      if abs(sto-limx[-1])/86400>2*ddoy:
        nticks = nticks - 1
      ddoy = np.floor(ndays/(nticks-1))
      sto = doy2sec(yyyy, doy+ddoy*(nticks-1))
      (xticks,xtick_labels)=mk_ticks_from_sec(nticks,sta, sto,"yyyy-doy")
  return xticks,xtick_labels

def bock2sec(t):
  t_1e6 = t*1e6
  yy = np.floor(t_1e6/1e10)
  yyyy = 2000+yy
  mm = np.floor((t_1e6-yy*1e10)/1e8)
  dd = np.floor((t_1e6-yy*1e10-mm*1e8)/1e6)
  
  h = np.floor((t_1e6-yy*1e10-mm*1e8-dd*1e6)/1e4)
  m = np.floor((t_1e6-yy*1e10-mm*1e8-dd*1e6-h*1e4)/1e2)
  s = np.floor((t_1e6-yy*1e10-mm*1e8-dd*1e6-h*1e4-m*1e2))
  
  if not isinstance(t,np.ndarray):
     sec = cal2sec(yyyy,mm,dd,h,m,s)
  else:
    sec = np.zeros(t.shape)
    for i in np.arange(t.shape[0]): sec[i] = cal2sec(yyyy[i],mm[i],dd[i],h[i],m[i],s[i])
  return sec

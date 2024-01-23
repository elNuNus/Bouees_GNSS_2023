# name, dt, cmd, path out, name out
ubx , 3600, gpspipe -R            , ./ubx/ , raw_%s.ubx
nmea,   60, gpspipe -r            , ./nmea/, raw_%s.nmea
met ,   60, sleep 60 && echo "met", ./met/ , raw_%s.met

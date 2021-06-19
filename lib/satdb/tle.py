from satdb import tools
from datetime import datetime, timedelta

class TLE:
    def __init__(self):
        self.line0 = None
        self.line1 = None
        self.line2 = None
        self.epoch = None

    def fromdb(self, dbc, norad, epoch):
        sql = """
        select
        m.name,
        o.norad,
        m.id_short,
        m.classification_type,
        o.epoch,
        o.mean_motion_dot,
        o.mean_motion_ddot,
        o.bstar,
        o.element_set_no,
        o.inclination,
        o.raan,
        o.eccentricity,
        o.arg_of_pericenter,
        o.mean_anomaly,
        o.mean_motion,
        o.rev_at_epoch
        from orbelem as o inner join metadata as m on
        (o.norad = m.norad)
        where (o.norad, abs(timestampdiff(second, o.epoch, %s))) in
        (select norad, min(abs(timestampdiff(second, epoch, %s)))
        from orbelem where norad=%s group by norad)
        and o.norad=%s limit 1;
        """
        res = dbc.fetchone(sql, (epoch, epoch, norad, norad,))

        line0 = res[0]

        # Calculate the decimal day of year
        doy = tools.datetime2doy(res[4])
#        epoch = res[4]
#        boy = datetime(epoch.year, 1, 1, 0, 0, 0) # begin of year (YYYY-01-01T00:00:00)
#        doy = (epoch - boy).days + (epoch - boy).seconds / 86400.

        line1 = ''.join([
            '1',                                            # line number
            ' ',
            str(res[1]),                                    # NORAD id
            res[3],                                         # classification
            ' ',
            '%-8s' % res[2],                                # int. designator
            ' ',
            res[4].strftime('%y') + '%12.8f'% doy,          # epoch
            ' ',
            '%10s' % ('%8.8f' % res[5]).replace('0.', '.'), # mean motion dot
            ' ',
            tools.conv_exp_notation(res[6]),                # mean motion ddot
            ' ',
            tools.conv_exp_notation(res[7]),                # bstar
            ' ',
            '0',                                            # ephemeris type
            ' ',
            '%4d' % res[8],                                 # element set no
            ])

        line2 = ''.join([
            '2',                                            # line number
            ' ',
            str(res[1]),                                    # NORAD id
            ' ',
            '%8.4f' % res[9],                               # inclination
            ' ',
            '%8.4f' % res[10],                              # RAAN
            ' ',
            ('%9.7f' % res[11]).replace('0.', ''),          # eccentricity
            ' ',
            '%8.4f' % res[12],                              # arg of pericenter
            ' ',
            '%8.4f' % res[13],                              # mean anomaly
            ' ',
            '%11.8f' % res[14],                             # mean motion
            '%5d' % res[15],                                # rev @ epoch
            ])

        # Calculate the checksum for line1 and line2
        cs_line1 = tools.tle_checksum(line1)
        cs_line2 = tools.tle_checksum(line2)

        # If checksums are all okay, write lines to the object attributes
        if cs_line1 is not None and cs_line2 is not None:
            self.line0 = line0
            self.line1 = line1 + str(cs_line1)
            self.line2 = line2 + str(cs_line2)
            self.epoch = res[4]


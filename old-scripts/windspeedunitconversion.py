from wnpmonsoon.ncdata import NCdata
import numpy as np

uas = NCdata(file_, 'uas')
vas = NCdata(file_, 'uas')

wind_sp = np.sqrt(np.square(uas.variable)+np.square(vas.variable))

# TODO decide if this is a good idea / if there is a better way to do this
# Inheriting from another object?
variable = 'ws'
ws = NCdata('notrealfile', variable, create_new=True)
ws.var_name = variable
ws.model = uas.model_id
ws.var_units = uas.var_units
ws.variable = wind_sp
ws.lats = uas.lats
ws.lons = uas.lons
ws.time = uas.time
ws.calendar = uas.calendar
ws.t_units = uas.t_units

ws.write(outfile)

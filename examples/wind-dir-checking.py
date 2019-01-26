from wnpmonsoon.tools import olddegfromnorth, degfromnorth
import numpy as np

# Manually computed test points
ccw_east = np.array([60, 150, 225, 270, 330])
ccw_west = np.array([240, 330, 45, 90, 150])
cw_north = np.array([30, 300, 225, 180, 120])

# Converting ccw east to ccw west
if False in list(ccw_west == (ccw_east + 180) % 360):
    print('Failed test')
else:
    print('amen')

# Converting ccw east to cw north
if False in list(cw_north == (-ccw_east + 90) % 360):
    print('Failed test')
else:
    print('amen')

# Converting cw north to ccw west
if False in list(ccw_west == (-cw_north + 270) % 360):
    print('Failed test')

# Converting cw north to ccw east
if False in list(ccw_east == (-cw_north + 90) % 360):
    print('Failed test')

# Define test points
test_points = np.array([45, 60, 90, 120, 135, 150, 180, 210, 225, 315, 330])
test_uas = np.array([1, 1, 0, -np.sqrt(3), -1, np.sqrt(3), -1, -np.sqrt(3), -1, 1, -1, np.sqrt(3)])
test_vas = np.array([1, np.sqrt(3), 1, 1, -1, -1, 0, -1, np.sqrt(3), -1, 1, -1])

# Convert test points to deg from north using deg from west equation
print((-test_points + 270) % 360)

# Convert test points to deg from north using deg from east equation
print((-test_points + 90) % 360)

# Test old function against points -- need to un-comment olddegfromnorth if want to do this function
# print('testing old func')
# for index, value in enumerate(test_uas):
#     try:
#         print(olddegfromnorth(test_uas[index], test_vas[index]))
#     except:
#         print("err'd outt")

# Test new function against points
print('testing new func')
for index, value in enumerate(test_uas):
    try:
        print(degfromnorth(test_uas[index], test_vas[index]))
    except:
        print("err'd outt")

# manually run the test script
# test_30_deg()
# test_45_deg()
# test_60_deg()
# test_90_deg()
# test_120_deg()
# test_135_deg()
# test_150_deg()
# test_180_deg()
# test_210_deg()
# test_225_deg()
# test_240_deg()
# test_315_deg()
# test_330_deg()
# test_all_as_array()

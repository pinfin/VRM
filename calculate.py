from func import *
from design import *

from hyd.flow import G

# Design
# feed tube
feed_tube = Geometry()
feed_tube.r_inner = 16
feed_tube.thickness = 4
feed_tube.angle_slot = 12
feed_tube.high_slot = 16 * 2 * 3
feed_tube.count_slot = 2
# ---------------------------------

# rotor
rotor = Geometry()
rotor.r_inner = 21
rotor.angle_slot = 12

rotor.r_outer = 35
rotor.r_nozzle = 40

rotor.inner_thickness = 4
rotor.outer_thickness = 5

rotor.high_nozzle = 40 * 2 * 3
rotor.high = rotor.high_nozzle

rotor.angle_nozzle = 15
rotor.count_nozzle = 2
# ---------------------------------

# case
case = Geometry()
case.r_inner = 60
case.thickness = 5
case.angle_slot = 5
case.high = rotor.high_nozzle
# ---------------------------------

# valve
valve = Geometry()
valve.r_valve = (rotor.r_outer + rotor.outer_thickness)/2
valve.high = rotor.high_nozzle
# ---------------------------------

# Property fluid
gas = Fluid(288.4, 1.28)
air = Fluid()
# ---------------------------------

# Operation parameters
p_feed = 15
T_feed = 600
p_outlet = 1

pressure_rise_ratio = 3.5
rpm = 300
# ---------------------------------

working_angle = get_working_angle(case, valve)

volume_chamber = get_init_volume_chamber(rotor, case)
volume_expand = get_expansion_volume(rot=rotor, st=case, expand_angle=working_angle)

expand_ratio = (1 + volume_expand / volume_chamber) ** gas.k

nozzle_area = get_nozzle_area(rotor)
partition_area = get_partition_area(rotor, case)

# init parameters
p_chamber = p_outlet
T_chamber = 1000

# define parameters mode
mode = Regime(rpm=300, p_1=15, T1=600, p_0=1)

m_chamber = (p_chamber * 1E+5 * volume_chamber * 1E-9) / (gas.R * T_chamber)
m_inlet = get_mass_flow_inlet(st=feed_tube, rot=rotor, param=mode, fluid=air, p0=p_chamber, ksi=3.0)
m_mix_chamber = m_inlet + m_chamber
ro_mix = m_mix_chamber / (volume_chamber * 1E-9)

cp_air = air.R * air.k / (air.k - 1)
cp_gas = gas.R * gas.k / (gas.k - 1)

T_mix_chamber = (m_chamber * cp_gas * T_chamber + m_inlet * cp_air * T_feed) / (m_chamber * cp_gas + m_inlet * cp_air)
p_mix_chamber = m_mix_chamber / (volume_chamber * 1E-9) * gas.R * T_mix_chamber * 1E-5

p_heating = p_mix_chamber * pressure_rise_ratio
T_heating = (p_heating * 1E+5) / (gas.R * ro_mix)

ro_expand = m_mix_chamber / ((volume_chamber + volume_expand) * 1E-9)
p_expand = p_heating / expand_ratio
T_expand = T_heating/expand_ratio**((gas.k - 1)/gas.k)

m_chamber = ro_expand * (volume_chamber * 1E-9)
p_chamber = p_expand
T_chamber = T_expand

m_out = ro_expand * (volume_expand * 1E-9)
p_out = p_expand
T_out = T_expand

G_out = G(ksi=3, F=nozzle_area*2*1E-6, k=gas.k, ro=ro_expand, p1=p_out*1E+5, p0=p_outlet*1E+5)

time_exhaust = m_out / G_out
time_expand = working_angle / (rpm * pi / 30)

power_max = 2 * 1E+5 * (p_heating - p_expand) * partition_area * 1E-6 * (rotor.r_nozzle + case.r_inner) * 1E-3 * 0.5 * (rpm * pi / 30)
power_min = 2 * 1E+5 * (p_expand - p_outlet) * partition_area * 1E-6 * (rotor.r_nozzle + case.r_inner) * 1E-3 * (rpm * pi / 30)
print(power_max/1000, power_min/1000)

power_feed = 2 * 1E+5 * (p_feed - p_outlet) * partition_area * 1E-6 * (rotor.r_nozzle + case.r_inner) * 1E-3 * (rpm * pi / 30)

print(power_feed)


cycle = pi
inject = 12 * pi / 180
combustion = 12 * pi / 180





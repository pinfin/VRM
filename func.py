from design import Geometry
from fluid import Fluid
from param import Regime


def get_area_inlet(a1, a2, r, h, w):
    from math import pi

    a1 = a1 * pi / 180
    a2 = a2 * pi / 180
    r = r * 1E-3
    h = h * 1E-3
    w = w * pi / 30

    if a1 == a2:
        return r * h * a1 ** 2 / w

    if a1 > a2:
        return r * h * 0.5 * (2 * a1 - a2) * a2 / w

    if a2 > a1:
        return r * h * 0.5 * (2 * a2 - a1) * a1 / w


def get_mass_flow_inlet(st: Geometry, rot: Geometry, param: Regime, fluid: Fluid, p0, ksi):
    from hyd.flow import G

    sum_area = get_area_inlet(st.angle_slot, rot.angle_slot,
                              st.r_inner, st.high_slot, param.rpm)

    t1 = param.T_inlet
    p1 = param.p_inlet * 1E+5
    ro = fluid.get_ro(p1, t1)
    p0 = p0 * 1E+5

    return G(ksi, sum_area, fluid.k, ro, p1, p0)



if __name__ == "__main__":
    print("Test mode:")

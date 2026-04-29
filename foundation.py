# app.py
# โปรแกรมออกแบบฐานรากเยื้องศูนย์ (Eccentric Footing)
# ตามทฤษฎี Terzaghi Bearing Capacity Theory
# ใช้งานด้วย Streamlit

import streamlit as st
import math

st.set_page_config(page_title="Eccentric Footing - Terzaghi", layout="centered")

st.title("โปรแกรมคำนวณฐานรากเยื้องศูนย์")
st.subheader("ตามทฤษฎี Terzaghi Bearing Capacity Theory")

st.markdown("---")

# =========================
# รับค่าจากผู้ใช้
# =========================

P = st.number_input("แรงกดรวม P (kN)", value=1500.0)
Mx = st.number_input("โมเมนต์รอบแกน X, Mx (kN-m)", value=120.0)
My = st.number_input("โมเมนต์รอบแกน Y, My (kN-m)", value=80.0)

B = st.number_input("ความกว้างฐานราก B (m)", value=2.5)
L = st.number_input("ความยาวฐานราก L (m)", value=3.0)
Df = st.number_input("ความลึกฐานราก Df (m)", value=1.5)

gamma = st.number_input("หน่วยน้ำหนักดิน γ (kN/m³)", value=18.0)
c = st.number_input("Cohesion, c (kPa)", value=25.0)
phi = st.number_input("มุมเสียดทานภายใน φ (degree)", value=30.0)

FS_required = st.number_input("Factor of Safety ที่ต้องการ", value=3.0)

st.markdown("---")


# =========================
# ฟังก์ชันคำนวณ
# =========================

def terzaghi_bearing_capacity(P, Mx, My, B, L, Df, gamma, c, phi):
    # Eccentricity
    ex = Mx / P
    ey = My / P

    # Effective dimensions
    B_eff = B - 2 * ex
    L_eff = L - 2 * ey

    if B_eff <= 0 or L_eff <= 0:
        return None

    A_eff = B_eff * L_eff

    # Bearing capacity factors
    phi_rad = math.radians(phi)

    if phi == 0:
        Nc = 5.7
        Nq = 1.0
        Ngamma = 0.0
    else:
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (
            math.tan(math.radians(45 + phi / 2))
        ) ** 2

        Nc = (Nq - 1) / math.tan(phi_rad)
        Ngamma = 2 * (Nq + 1) * math.tan(phi_rad)

    # surcharge
    q = gamma * Df

    # Ultimate Bearing Capacity
    qult = (c * Nc) + (q * Nq) + (0.5 * gamma * B_eff * Ngamma)

    # Applied pressure
    q_applied = P / A_eff

    # Safety Factor
    FS = qult / q_applied

    return {
        "ex": ex,
        "ey": ey,
        "B_eff": B_eff,
        "L_eff": L_eff,
        "A_eff": A_eff,
        "Nc": Nc,
        "Nq": Nq,
        "Ngamma": Ngamma,
        "qult": qult,
        "q_applied": q_applied,
        "FS": FS
    }


# =========================
# ปุ่มคำนวณ
# =========================

if st.button("คำนวณ"):

    result = terzaghi_bearing_capacity(
        P, Mx, My, B, L, Df, gamma, c, phi
    )

    if result is None:
        st.error("Effective Dimension <= 0 กรุณาตรวจสอบค่าที่ป้อน")
    else:
        st.success("คำนวณสำเร็จ")

        st.markdown("## ผลการคำนวณ")

        st.write(f"### Eccentricity")
        st.write(f"ex = {result['ex']:.3f} m")
        st.write(f"ey = {result['ey']:.3f} m")

        if result["ex"] > B / 6 or result["ey"] > L / 6:
            st.warning("แรงตกนอก Kern ของฐานราก อาจเกิดแรงดึงใต้ฐาน")

        st.write(f"### Effective Dimensions")
        st.write(f"B' = {result['B_eff']:.3f} m")
        st.write(f"L' = {result['L_eff']:.3f} m")
        st.write(f"A' = {result['A_eff']:.3f} m²")

        st.write(f"### Bearing Capacity Factors")
        st.write(f"Nc = {result['Nc']:.3f}")
        st.write(f"Nq = {result['Nq']:.3f}")
        st.write(f"Nγ = {result['Ngamma']:.3f}")

        st.write(f"### Bearing Capacity")
        st.write(f"Ultimate Bearing Capacity = {result['qult']:.3f} kPa")
        st.write(f"Applied Bearing Pressure = {result['q_applied']:.3f} kPa")

        st.write(f"### Safety Check")
        st.write(f"Factor of Safety (FS) = {result['FS']:.3f}")

        if result["FS"] >= FS_required:
            st.success("ผลการออกแบบ: ปลอดภัย")
        else:
            st.error("ผลการออกแบบ: ไม่ปลอดภัย")

import math

def structural_design_footing():
    print("--- โปรแกรมออกแบบฐานรากแผ่คอขวด (SDM Standard) ---")
    
    # 1. รับค่าตัวแปรการออกแบบ (Input)
    dl = float(input("น้ำหนักบรรทุกคงที่ (Dead Load) (kg): "))
    ll = float(input("น้ำหนักบรรทุกจร (Live Load) (kg): "))
    q_all = float(input("ความสามารถการรับน้ำหนักดิน (Allowable Bearing) (kg/m²): "))
    fc_prime = float(input("กำลังอัดของคอนกรีต f'c (ksc): "))
    fy = float(input("กำลังรับแรงดึงเหล็กเสริม fy (ksc): "))
    col_size = float(input("ขนาดเสาตอม่อด้านเท่า (m): "))
    
    # 2. คำนวณขนาดฐานราก (Service Load)
    p_service = (dl + ll) * 1.10  # รวมน้ำหนักฐานรากประมาณ 10%
    area_req = p_service / q_all
    width = math.ceil(math.sqrt(area_req) * 10) / 10
    area_actual = width ** 2
    
    # 3. คำนวณแรงดันดินประลัย (Factored Load)
    p_u = (1.4 * dl) + (1.7 * ll)
    q_u = p_u / area_actual
    
    # 4. สมมติความหนาฐานราก (t) และระยะลึกประสิทธิผล (d)
    t = 0.50 # เริ่มต้นที่ 50 ซม.
    covering = 0.075 # ระยะหุ้ม 7.5 ซม.
    d = t - covering - 0.012 # หัก covering และครึ่งหนึ่งของเหล็ก 12-25mm
    
    # 5. ตรวจสอบแรงเฉือนทะลุ (Punching Shear)
    # เส้นรอบรูปวิกฤตที่ d/2 จากขอบเสา
    b0 = 4 * (col_size + d)
    v_u_punch = q_u * (area_actual - (col_size + d)**2)
    phi_v = 0.85
    v_c_punch = phi_v * 1.06 * math.sqrt(fc_prime) * (b0 * 100) * (d * 100)
    
    # 6. คำนวณเหล็กเสริม (Flexure Reinforcement)
    # ระยะจากขอบเสาถึงขอบฐานราก (Moment Arm)
    x = (width - col_size) / 2
    m_u = (q_u * width * (x**2)) / 2
    
    # หาปริมาณเหล็กเสริม (Simplified formula)
    phi_m = 0.90
    rn = m_u / (phi_m * width * (d**2) * 10) # 10 คือตัวแปรแปลงหน่วย ksc
    rho = (0.85 * fc_prime / fy) * (1 - math.sqrt(1 - (2 * rn / (0.85 * fc_prime))))
    as_required = max(rho, 0.0018) * (width * 100) * (d * 100) # ตรวจสอบเหล็กเสริมขั้นต่ำ

    # แสดงผล
    print("\n" + "="*30)
    print(f"ขนาดฐานราก: {width:.2f} x {width:.2f} เมตร")
    print(f"ความหนาที่ใช้: {t:.2f} เมตร (d = {d:.2f} ม.)")
    print(f"แรงเฉือนทะลุ (Vu): {v_u_punch:,.2f} kg")
    print(f"กำลังรับแรงเฉือนคอนกรีต (Phi Vc): {v_c_punch:,.2f} kg")
    
    if v_c_punch > v_u_punch:
        print(">> ผลการตรวจสอบแรงเฉือน: ผ่าน")
    else:
        print(">> ผลการตรวจสอบแรงเฉือน: ไม่ผ่าน (ต้องเพิ่มความหนาฐานราก)")
        
    print(f"ปริมาณเหล็กเสริมที่ต้องการ: {as_required:.2f} ตร.ซม.")
    print("="*30)

if __name__ == "__main__":
    structural_design_footing()

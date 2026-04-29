import math

def design_footing(P_dl, P_ll, q_all, f_c_prime, f_y, col_size):
    # 1. Load Combination (น้ำหนักประลัย)
    P_u = (1.4 * P_dl) + (1.7 * P_ll)
    
    # 2. หาขนาดฐานราก (ใช้น้ำหนักใช้งาน + เผื่อ 10%)
    P_service = (P_dl + P_ll) * 1.1
    area_req = P_service / q_all
    B = math.ceil(math.sqrt(area_req) * 10) / 10  # ปัดขึ้นทุก 10 ซม.
    
    # 3. แรงดันดินประลัยจริง
    q_u = P_u / (B**2)
    
    # 4. สมมติความหนาประสิทธิผล (d) เบื้องต้น (หน่วยเมตร)
    d = 0.40 
    
    # 5. ตรวจสอบ Punching Shear (แรงเฉือนทะลุ)
    # เส้นรอบรูปวิกฤต (b0) ที่ระยะ d/2 จากขอบเสา
    b0 = 4 * (col_size + d)
    V_u_punch = q_u * (B**2 - (col_size + d)**2)
    
    print(f"--- สรุปผลการออกแบบเบื้องต้น ---")
    print(f"ขนาดฐานรากที่ใช้: {B:.2f} x {B:.2f} m.")
    print(f"แรงดันดินประลัย (qu): {q_u:,.2f} kg/m²")
    print(f"แรงเฉือนทะลุที่เกิดขึ้น (Vu): {V_u_punch:,.2f} kg")

# ตัวอย่างการใส่ค่า: DL=20ตัน, LL=10ตัน, ดินรับได้ 15ตัน/ตร.ม., fc'=240, fy=4000, เสา 0.30ม.
design_footing(20000, 10000, 15000, 240, 4000, 0.30)

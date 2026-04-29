import math

def calculate_footing():
    print("--- โปรแกรมคำนวณขนาดฐานรากแผ่เบื้องต้น ---")
    
    try:
        # รับค่าจากผู้ใช้งาน
        column_load = float(input("ใส่น้ำหนักบรรทุกจากเสา (kg): "))
        soil_bearing_capacity = float(input("ใส่ความสามารถในการรับน้ำหนักบรรทุกของดิน (kg/m²): "))
        safety_factor_weight = 1.1  # เผื่อน้ำหนักตัวฐานรากเองประมาณ 10%
        
        # คำนวณน้ำหนักรวม
        total_load = column_load * safety_factor_weight
        
        # คำนวณพื้นที่ที่ต้องการ (Area = Load / Pressure)
        required_area = total_load / soil_bearing_capacity
        
        # คำนวณความกว้างด้านของฐานรากจัตุรัส (Width = sqrt(Area))
        width = math.sqrt(required_area)
        
        # ปัดเศษขึ้นเพื่อให้ได้ขนาดที่ใช้งานได้จริง (Step ละ 0.10 เมตร)
        final_width = math.ceil(width * 10) / 10
        
        print("\n--- ผลการคำนวณ ---")
        print(f"น้ำหนักรวมที่ใช้คำนวณ (รวมเผื่อน้ำหนักฐานราก 10%): {total_load:,.2f} kg")
        print(f"พื้นที่ฐานรากที่ต้องการขั้นต่ำ: {required_area:.4f} m²")
        print(f"ขนาดฐานรากที่แนะนำ: {final_width:.2f} x {final_width:.2f} เมตร")
        print(f"หน่วยแรงกดทับดินจริง: {total_load / (final_width**2):,.2f} kg/m²")

    except ValueError:
        print("กรุณากรอกตัวเลขให้ถูกต้อง")

if __name__ == "__main__":
    calculate_footing()

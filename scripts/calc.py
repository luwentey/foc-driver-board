#!/usr/bin/env python3
"""
FOC 驱动板参数计算脚本

本脚本展示了 AI 辅助硬件设计中的参数计算工作流。
使用 Claude Code 进行参数推导和验证。

主要计算内容：
1. 自举电容选型
2. MOSFET 功耗估算
3. 电流采样放大器增益计算
4. 散热需求分析
"""

import math

# ============================================================
# 1. 自举电容计算
# ============================================================

def calc_bootstrap_capacitor():
    """
    自举电容计算

    设计目标：为高端 MOSFET 栅极驱动提供足够的电荷

    计算公式：Cboot = Qg_total / ΔV
    - Qg_total: 总栅极电荷 + 漏电流电荷
    - ΔV: 允许的电压降 (VCC - Vf_diode - Vboot_min)

    参考：EG2133 datasheet + NCE6080K datasheet
    """

    print("=" * 60)
    print("1. 自举电容计算")
    print("=" * 60)

    # NCE6080K 栅极电荷
    Qg_mosfet = 90e-9  # 90nC
    Qc_boot_leakage = 10e-9  # 自举电容漏电流等效电荷
    Qg_total = Qg_mosfet + Qc_boot_leakage

    # 电压参数
    VCC = 12.0  # 推荐 VCC
    Vf_diode = 1.0  # FR107 正向压降
    Vboot_min = 10.5  # 最小自举电压 (VCC - Vf - 裕量)

    # 计算最小电容
    delta_V = VCC - Vf_diode - Vboot_min
    Cboot_min = Qg_total / delta_V

    # 选择电容（100倍余量）
    Cboot_selected = 1e-6  # 1μF

    print(f"输入参数：")
    print(f"  MOSFET 栅极电荷 Qg: {Qg_mosfet*1e9:.1f} nC")
    print(f"  自举电容漏电等效电荷: {Qc_boot_leakage*1e9:.1f} nC")
    print(f"  总电荷 Qg_total: {Qg_total*1e9:.1f} nC")
    print()
    print(f"电压参数：")
    print(f"  VCC: {VCC} V")
    print(f"  二极管正向压降 Vf: {Vf_diode} V")
    print(f"  最小自举电压 Vboot_min: {Vboot_min} V")
    print(f"  允许电压降 ΔV: {delta_V} V")
    print()
    print(f"计算结果：")
    print(f"  最小电容 Cboot_min: {Cboot_min*1e9:.2f} nF")
    print(f"  选择电容 (100x余量): {Cboot_selected*1e6:.0f} μF")
    print(f"  推荐封装: 0805 X7R 25V")
    print()

    return Cboot_selected


# ============================================================
# 2. MOSFET 功耗估算
# ============================================================

def calc_mosfet_power():
    """
    MOSFET 功耗计算

    功耗来源：
    1. 导通损耗：P_conduction = I² × Rds(on)
    2. 开关损耗：P_switching = 0.5 × V × I × (tr + tf) × fsw
    3. 体二极管续流损耗

    参考：NCE6080K datasheet
    """

    print("=" * 60)
    print("2. MOSFET 功耗估算")
    print("=" * 60)

    # 器件参数 (NCE6080K)
    Rds_on = 7e-3  # 7mΩ @ VGS=10V, Tj=25°C
    VDS_max = 60.0  # 60V
    Qg = 90e-9  # 90nC

    # 应用参数
    V_motor = 24.0  # 电机额定电压
    I_continuous = 20.0  # 持续电流
    I_peak = 80.0  # 峰值电流
    fsw = 20e3  # 开关频率 20kHz

    # 温度降额因子
    temp_factor = 1.5  # @ Tc=100°C, Rds(on) 增加约 50%

    # 导通损耗
    P_conduction = I_continuous**2 * Rds_on * temp_factor

    # 开关损耗估算
    # tr ≈ tf ≈ 20ns (典型值)
    tr = tf = 20e-9
    P_switching = 0.5 * V_motor * I_continuous * (tr + tf) * fsw

    # 总功耗 (单管)
    P_total_single = P_conduction + P_switching

    # 6管总功耗
    P_total_6ch = P_total_single * 6

    print(f"NCE6080K 参数：")
    print(f"  Rds(on): {Rds_on*1e3:.1f} mΩ @ VGS=10V")
    print(f"  VDS(max): {VDS_max} V")
    print(f"  Qg: {Qg*1e9:.0f} nC")
    print()
    print(f"应用条件：")
    print(f"  电机电压: {V_motor} V")
    print(f"  持续电流: {I_continuous} A")
    print(f"  峰值电流: {I_peak} A")
    print(f"  开关频率: {fsw/1e3:.0f} kHz")
    print()
    print(f"功耗计算（单管 @ 持续 20A）：")
    print(f"  导通损耗: {P_conduction:.2f} W")
    print(f"  开关损耗: {P_switching:.3f} W")
    print(f"  总功耗: {P_total_single:.2f} W")
    print()
    print(f"三相总功耗（6管）: {P_total_6ch:.2f} W")
    print()

    return {
        'P_conduction': P_conduction,
        'P_switching': P_switching,
        'P_total_single': P_total_single,
        'P_total_6ch': P_total_6ch
    }


# ============================================================
# 3. 电流采样放大器设计
# ============================================================

def calc_current_sensing():
    """
    电流采样放大器设计

    方案：下桥采样电阻 + 差分放大
    - 相电流采样：增益 10x，±20A 范围
    - 母线电流采样：增益 5x，0~80A 范围

    参考：RS624 datasheet
    """

    print("=" * 60)
    print("3. 电流采样放大器设计")
    print("=" * 60)

    # 电源参数
    VCC_op = 5.0  # 运放供电
    VREF = VCC_op / 2  # 2.5V 中点

    # 采样电阻
    Rsense = 5e-3  # 5mΩ

    # 相电流采样设计（±20A 范围）
    print("【相电流采样设计】")
    I_phase_max = 20.0  # ±20A

    # 增益计算
    # Vout = VREF + Isense × Rsense × Gain
    # 20A × 5mΩ × Gain = 1.0V (需要 1V 摆幅)
    # Gain = 1.0V / (20A × 5mΩ) = 10
    Gain_phase = 10.0

    # 反馈电阻选择
    R1_phase = 1e3  # 1kΩ
    R3_phase = Gain_phase * R1_phase  # 10kΩ

    # 电压范围
    Vout_phase_max = VREF + I_phase_max * Rsense * Gain_phase
    Vout_phase_min = VREF - I_phase_max * Rsense * Gain_phase

    print(f"  采样电阻: {Rsense*1e3:.0f} mΩ")
    print(f"  增益: {Gain_phase:.0f}x")
    print(f"  差分输入电阻 R1/R2: {R1_phase/1e3:.0f} kΩ")
    print(f"  反馈电阻 R3/R4: {R3_phase/1e3:.0f} kΩ")
    print(f"  输出范围: {Vout_phase_min:.2f}V ~ {Vout_phase_max:.2f}V")
    print()

    # 母线电流采样设计（0~80A 范围）
    print("【母线电流采样设计】")

    # 母线电流总是正向（电源 -> 电机）
    # 增益需要更低以覆盖更大范围
    I_bus_max = 80.0  # 80A 峰值
    Gain_bus = 5.0  # 增益 5x

    # 反馈电阻选择
    R33_bus = 2e3  # 2kΩ
    R35_bus = Gain_bus * R33_bus  # 10kΩ

    # 电压范围
    Vout_bus_min = VREF  # 0A 时 = VREF
    Vout_bus_max = VREF + I_bus_max * Rsense * Gain_bus

    print(f"  采样电阻: {Rsense*1e3:.0f} mΩ (与相电流共用)")
    print(f"  增益: {Gain_bus:.0f}x")
    print(f"  差分输入电阻 R33/R34: {R33_bus/1e3:.0f} kΩ")
    print(f"  反馈电阻 R35/R36: {R35_bus/1e3:.0f} kΩ")
    print(f"  输出范围: {Vout_bus_min:.2f}V ~ {Vout_bus_max:.2f}V")
    print()

    return {
        'Gain_phase': Gain_phase,
        'Gain_bus': Gain_bus,
        'VREF': VREF,
        'R1_phase': R1_phase,
        'R3_phase': R3_phase,
        'R33_bus': R33_bus,
        'R35_bus': R35_bus
    }


# ============================================================
# 4. 散热需求分析
# ============================================================

def calc_thermal():
    """
    散热需求分析

    估算 TO-252 封装在自然对流下的散热能力

    参考：NCE6080K thermal resistance
    """

    print("=" * 60)
    print("4. 散热需求分析")
    print("=" * 60)

    # 功耗数据 (from calc_mosfet_power)
    P_single = 2.8  # 单管导通损耗 @ 20A

    # TO-252 热阻参数
    Rtheta_JC = 3.0  # 结到壳热阻 (°C/W) - TO-252
    Rtheta_CS = 1.0  # 壳到散热片热阻
    Rtheta_CA = 40.0  # 壳到空气热阻 (自然对流，无散热片)

    # 计算温升
    # 有散热片
    Rtheta_total_heatsink = Rtheta_JC + Rtheta_CS + 2.0  # 假设散热片热阻
    Delta_T_heatsink = P_single * Rtheta_total_heatsink

    # 无散热片 (自然对流)
    Rtheta_total_nocooling = Rtheta_JC + Rtheta_CA
    Delta_T_nocooling = P_single * Rtheta_total_nocooling

    # 环境温度 25°C 下的结温
    T_junction_heatsink = 25 + Delta_T_heatsink
    T_junction_nocooling = 25 + Delta_T_nocooling

    print(f"单管功耗 @ 20A: {P_single:.1f} W")
    print()
    print(f"热阻参数：")
    print(f"  RθJC (结到壳): {Rtheta_JC} °C/W")
    print(f"  RθCS (壳到散热片): {Rtheta_CS} °C/W")
    print(f"  RθCA (壳到空气): {Rtheta_CA} °C/W")
    print()

    print(f"【有散热片】")
    print(f"  总热阻: {Rtheta_total_heatsink:.1f} °C/W")
    print(f"  温升: {Delta_T_heatsink:.1f} °C")
    print(f"  结温 (Ta=25°C): {T_junction_heatsink:.1f} °C ✓")
    print()

    print(f"【无散热片，自然对流】")
    print(f"  总热阻: {Rtheta_total_nocooling:.1f} °C/W")
    print(f"  温升: {Delta_T_nocooling:.1f} °C")
    print(f"  结温 (Ta=25°C): {T_junction_nocooling:.1f} °C ⚠")
    print()

    # 限制持续电流
    T_junction_max = 125.0  # MOSFET 最大结温
    T_margin = 25.0  # 裕量
    P_max_nocooling = (T_junction_max - T_margin - 25) / Rtheta_total_nocooling
    I_continuous_max = math.sqrt(P_max_nocooling / 7e-3)

    print(f"建议：无散热片时，限制持续电流 ≤ {I_continuous_max:.1f} A")
    print()


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print()
    print("FOC 驱动板参数计算")
    print("AI-Assisted Hardware Design Demo")
    print()

    calc_bootstrap_capacitor()
    calc_mosfet_power()
    calc_current_sensing()
    calc_thermal()

    print("=" * 60)
    print("计算完成！")
    print("=" * 60)

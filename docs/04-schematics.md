# FOC 驱动板 — 模块原理图（结构化连接表）

> 项目：FOC 三相无刷电机驱动板 | 日期：2026-05-07（v2 — 需求确认后更新）

---

## 1. EG2133 驱动电路

### 1.1 电源与去耦

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| VCC_12V | P1 端子 | EG2133.Pin7(VCC) | 10μF(X5R 0805) + 0.1μF(X7R 0603) 到 GND |
| GND | P1 端子 | EG2133.Pin8(GND) | 信号地平面 |

### 1.2 信号输入

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| PWM_H1 | J1.Pin1 | R7(100Ω) → EG2133.Pin1(HIN1) | 100Ω串联，HIN1下拉10kΩ到GND |
| PWM_H2 | J1.Pin2 | R8(100Ω) → EG2133.Pin2(HIN2) | 100Ω串联，HIN2下拉10kΩ到GND |
| PWM_H3 | J1.Pin3 | R9(100Ω) → EG2133.Pin3(HIN3) | 100Ω串联，HIN3下拉10kΩ到GND |
| PWM_L1 | J1.Pin4 | R10(100Ω) → EG2133.Pin4(LIN1) | 100Ω串联，LIN1上拉10kΩ到VCC |
| PWM_L2 | J1.Pin5 | R11(100Ω) → EG2133.Pin5(LIN2) | 100Ω串联，LIN2上拉10kΩ到VCC |
| PWM_L3 | J1.Pin6 | R12(100Ω) → EG2133.Pin6(LIN3) | 100Ω串联，LIN3上拉10kΩ到VCC |

### 1.3 U相驱动输出

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| HO1 | EG2133.Pin13(HO1) | R1(10Ω) → Q1.Gate | 高端MOSFET栅极驱动 |
| LO1 | EG2133.Pin11(LO1) | R2(10Ω) → Q2.Gate | 低端MOSFET栅极驱动 |
| VB1 | D1(FR107阴极) | EG2133.Pin14(VB1) | 自举电源 |
| VS1 | U_OUT | EG2133.Pin12(VS1) | 高端浮地 |
| BOOT1_A | VCC_12V | D1(FR107阳极) | 自举二极管 |
| BOOT1_K | D1(FR107阴极) | C_BOOT1(1μF) → VS1 | 自举电容 |

### 1.4 V相驱动输出

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| HO2 | EG2133.Pin16(HO2) | R3(10Ω) → Q3.Gate | 高端MOSFET栅极驱动 |
| LO2 | EG2133.Pin10(LO2) | R4(10Ω) → Q4.Gate | 低端MOSFET栅极驱动 |
| VB2 | D2(FR107阴极) | EG2133.Pin17(VB2) | 自举电源 |
| VS2 | V_OUT | EG2133.Pin15(VS2) | 高端浮地 |
| BOOT2_A | VCC_12V | D2(FR107阳极) | 自举二极管 |
| BOOT2_K | D2(FR107阴极) | C_BOOT2(1μF) → VS2 | 自举电容 |

### 1.5 W相驱动输出

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| HO3 | EG2133.Pin19(HO3) | R5(10Ω) → Q5.Gate | 高端MOSFET栅极驱动 |
| LO3 | EG2133.Pin9(LO3) | R6(10Ω) → Q6.Gate | 低端MOSFET栅极驱动 |
| VB3 | D3(FR107阴极) | EG2133.Pin20(VB3) | 自举电源 |
| VS3 | W_OUT | EG2133.Pin18(VS3) | 高端浮地 |
| BOOT3_A | VCC_12V | D3(FR107阳极) | 自举二极管 |
| BOOT3_K | D3(FR107阴极) | C_BOOT3(1μF) → VS3 | 自举电容 |

---

## 2. 功率 MOSFET 三相逆变桥

### 2.1 U相半桥

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| VMOTOR | P2 铜皮 | Q1.Drain | 24V，高端MOSFET漏极 |
| U_OUT | Q1.Source | Q2.Drain | 相输出节点，接VS1 |
| GND_PWR | Q2.Source | Rs_U(5mΩ) → GND_PWR_PLANE | 低端MOSFET源极经采样电阻接地平面 |
| Q1_GATE | R1(10Ω) | Q1.Gate | 10kΩ栅源下拉(R13) |
| Q2_GATE | R2(10Ω) | Q2.Gate | 10kΩ栅源下拉(R14) |
| U_OUT → M1 | M1 端子 | 电机U相 | 短而宽走线 |

### 2.2 V相半桥

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| VMOTOR | P2 铜皮 | Q3.Drain | 24V，高端MOSFET漏极 |
| V_OUT | Q3.Source | Q4.Drain | 相输出节点，接VS2 |
| GND_PWR | Q4.Source | Rs_V(5mΩ) → GND_PWR_PLANE | 低端MOSFET源极经采样电阻接地平面 |
| Q3_GATE | R3(10Ω) | Q3.Gate | 10kΩ栅源下拉(R15) |
| Q4_GATE | R4(10Ω) | Q4.Gate | 10kΩ栅源下拉(R16) |
| V_OUT → M2 | M2 端子 | 电机V相 | 短而宽走线 |

### 2.3 W相半桥

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| VMOTOR | P2 铜皮 | Q5.Drain | 24V，高端MOSFET漏极 |
| W_OUT | Q5.Source | Q6.Drain | 相输出节点，接VS3 |
| GND_PWR | Q6.Source | Rs_W(5mΩ) → GND_PWR_PLANE | 低端MOSFET源极经采样电阻接地平面 |
| Q5_GATE | R5(10Ω) | Q5.Gate | 10kΩ栅源下拉(R17) |
| Q6_GATE | R6(10Ω) | Q6.Gate | 10kΩ栅源下拉(R18) |
| W_OUT → M3 | M3 端子 | 电机W相 | 短而宽走线 |

### 2.4 VMOTOR 去耦

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| VMOTOR_GND | C_VM1(100μF/63V) 正极 | 负极→GND_PWR_PLANE | 电解电容，靠近Q1/Q3/Q5漏极 |
| VMOTOR_CER | C_VM2(1μF/100V) → GND_PWR_PLANE | ×3, 靠近每相 | 陶瓷去耦 |

### 2.5 母线电流采样电阻

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| GND_PWR_PLANE | Rs_U/Rs_V/Rs_W 低端 | Rs_BUS(5mΩ) 高端 | 板内功率地平面 |
| SYSTEM_GND | Rs_BUS(5mΩ) 低端 | P3 端子(外部电源地) | 5mΩ/5W 3637封装 |
| SENSE_BUS+ | Rs_BUS 高端(GND_PWR_PLANE侧) | R33(2kΩ) → RS624.Pin12(+IN_D) | 母线差分正输入 |
| SENSE_BUS- | Rs_BUS 低端(外部地侧) | R34(2kΩ) → RS624.Pin13(-IN_D) | 母线差分负输入 |

---

## 3. RS624 电流采样电路

### 3.1 电源

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| VCC_5V | J1.Pin8 | RS624.Pin11(V+) | 10μF(X5R 0805) + 0.1μF(X7R 0603) 去耦到 GND |
| GND | - | RS624.Pin4(V-) | 运放负电源=GND |

### 3.2 VREF 分压（ADC 中点参考）

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| VCC_5V | R19(10kΩ) | R20(10kΩ) → GND | 分压得 VREF = VCC_5V/2 = 2.5V |
| VREF | R19/R20 中点 | C_VREF(0.1μF) → GND | 缓冲后输出 |
| VREF | - | J2.Pin5 | 输出给 MCU ADC 参考 |

### 3.3 U相电流采样（运放 A）

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| SENSE_U+ | Rs_U 高端(接Q2.Source) | R21(1kΩ) → RS624.Pin3(+IN_A) | 差分正输入 |
| SENSE_U- | Rs_U 低端(接GND_PWR_PLANE) | R22(1kΩ) → RS624.Pin2(-IN_A) | 差分负输入 |
| FB_U+ | R21输出 | R23(10kΩ) → RS624.Pin1(OUT_A) | 正反馈电阻，增益=10 |
| FB_U- | R22输出 | R24(10kΩ) → VREF | 负反馈参考 |
| I_U | RS624.Pin1(OUT_A) | J2.Pin1 | U相电流采样输出 |

### 3.4 V相电流采样（运放 B）

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| SENSE_V+ | Rs_V 高端 | R25(1kΩ) → RS624.Pin5(+IN_B) | 差分正输入 |
| SENSE_V- | Rs_V 低端 | R26(1kΩ) → RS624.Pin6(-IN_B) | 差分负输入 |
| FB_V+ | R25输出 | R27(10kΩ) → RS624.Pin7(OUT_B) | 正反馈电阻，增益=10 |
| FB_V- | R26输出 | R28(10kΩ) → VREF | 负反馈参考 |
| I_V | RS624.Pin7(OUT_B) | J2.Pin2 | V相电流采样输出 |

### 3.5 W相电流采样（运放 C）

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| SENSE_W+ | Rs_W 高端 | R29(1kΩ) → RS624.Pin10(+IN_C) | 差分正输入 |
| SENSE_W- | Rs_W 低端 | R30(1kΩ) → RS624.Pin9(-IN_C) | 差分负输入 |
| FB_W+ | R29输出 | R31(10kΩ) → RS624.Pin8(OUT_C) | 正反馈电阻，增益=10 |
| FB_W- | R30输出 | R32(10kΩ) → VREF | 负反馈参考 |
| I_W | RS624.Pin8(OUT_C) | J2.Pin3 | W相电流采样输出 |

### 3.6 母线电流采样（运放 D）

| 网络 | 源端 | 目标端 | 参数/备注 |
|------|------|--------|-----------|
| SENSE_BUS+ | Rs_BUS 高端(GND_PWR_PLANE) | R33(2kΩ) → RS624.Pin12(+IN_D) | 差分正输入 |
| SENSE_BUS- | Rs_BUS 低端(外部地) | R34(2kΩ) → RS624.Pin13(-IN_D) | 差分负输入 |
| FB_BUS+ | R33输出 | R35(10kΩ) → RS624.Pin14(OUT_D) | 正反馈电阻，增益=5 |
| FB_BUS- | R34输出 | R36(10kΩ) → VREF | 负反馈参考 |
| I_BUS | RS624.Pin14(OUT_D) | J2.Pin4 | 母线电流采样输出 |

**母线采样计算**：
- 增益 G = R35/R33 = 10kΩ/2kΩ = 5
- Vout = VREF + (V_BUS+ - V_BUS-) × G
- 0A 时：Vout = 2.5V（中点）
- 40A 时：Vout = 2.5V + 40A × 5mΩ × 5 = 3.5V
- 80A 峰值：Vout = 2.5V + 80A × 5mΩ × 5 = 4.5V

---

## 4. 完整网络列表汇总

### 电源网络

| 网络名 | 电压 | 电流 | 去耦 |
|--------|------|------|------|
| VMOTOR | 24V额定(12-48V) | ≤80A | 100μF+3×1μF |
| VCC_12V | 12V | ≤500mA | 10μF+0.1μF |
| VB1/VB2/VB3 | ~11V(自举) | ~100μA | 3×1μF |
| VCC_5V | 5V | ≤5mA | 10μF+0.1μF |
| VREF | 2.5V (VCC_5V/2) | ≤1mA | 0.1μF |
| GND | 0V | - | 信号地 |
| GND_PWR_PLANE | 0V (板内) | ≤80A | 功率地平面 |
| SYSTEM_GND | 0V (外部) | ≤80A | 经Rs_BUS连接GND_PWR_PLANE |

### 信号网络

| 网络名 | 方向 | 电平 | 备注 |
|--------|------|------|------|
| PWM_H1/H2/H3 | IN | 3.3V/5V | 高电平有效 |
| PWM_L1/L2/L3 | IN | 3.3V/5V | 低电平有效 |
| HO1/HO2/HO3 | 内部 | 0~VBx | 高端驱动输出 |
| LO1/LO2/LO3 | 内部 | 0~VCC | 低端驱动输出 |
| U_OUT/V_OUT/W_OUT | OUT | 0~VMOTOR | 三相输出 |
| I_U/I_V/I_W | OUT | 1.5V~3.5V | 相电流采样输出，增益10× |
| I_BUS | OUT | 2.5V~4.5V | 母线电流采样输出，增益5× |
| VREF | OUT | 2.5V | ADC中点参考 |

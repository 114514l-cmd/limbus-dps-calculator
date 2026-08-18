# 边狱巴士 DPS 计算器 / Limbus Company DPS Calculator

[中文](#中文) | [English](#english)

---

## 中文

一款《边狱巴士（Limbus Company）》的玩家自制数值工具：计算人格技能的**精确伤害期望**（硬币翻转全枚举）、**拼点胜率**（蒙特卡洛模拟）、**循环 DPT**（按卡组频次加权），支持 E.G.O 资源模型与流血/燃烧/沉潜 DoT 结算。
数据来源是边狱巴士wiki
### 功能

- 📊 **精确伤害分布**：枚举技能全部 2ⁿ 硬币结果，输出期望 / 标准差 / 伤害范围
- ⚔️ **拼点模拟**：完整拼点规则蒙特卡洛（胜率 + 剩余硬币期望）
- 🔄 **循环伤害**：按卡组份数（S1×3 / S2×2 / S3×1，可调）计算一循环总伤与每回合期望（DPT）
- ✨ **E.G.O 模型**：罪孽资源收支校验，可发动次数 = min(各罪孽收入 ÷ 消耗)，计入替代出牌的机会成本
- 🩸 **DoT 结算**：流血（中招者行动触发）/ 沉潜（被命中触发）/ 燃烧（回合结束触发）分别建模
- 🌐 **数据一键导入**：内置全部 184 人格 + 110 个 E.G.O 的官方解包数值，搜索即用
- 🛠️ **自定义技能组**：跨人格组合技能、改写威力（强化技能变体）、编辑份数、挂 DoT
- 📤 Excel 报告导出；Windows 单文件 exe，免安装

### 下载与使用

1. 从 [Releases](../../releases) 下载 `边狱巴士DPS计算器.exe`
2. 双击运行（无需 Python 环境）
3. 点「从Wiki获取人格」导入你想要的人格，设置环境参数，点「计算伤害期望」

> ⚠️ **报毒说明**：本程序使用 PyInstaller 打包且未购买代码签名证书，Windows SmartScreen / 部分杀软可能误报。这是已知误报，不放心的话可以直接用源码运行：
> ```bash
> pip install openpyxl
> python limbus_gui.py
> ```

### 数据来源

- 人格 / E.G.O / 技能数值来自解包数据库 **[monthofjune/limbus_data](https://github.com/monthofjune/limbus_data)**（经 jsDelivr CDN 加载），在此致谢。
- 伤害公式为社区反推共识（暴击倍率 1.2x、等级差 ±3%/级 等），**非官方公示**，相关参数在代码 `CFG` 中集中可调。

### 已知简化

- DoT 为上限估算：未模拟层数溢出、混乱区与抵抗
- E.G.O 未计侵蚀态（Corrosion）与被动
- 条件触发增益（如充能加威力）需在数据中手动配置 `cond` 字段

### 免责声明

本工具为**非官方粉丝作品**，与 Project Moon 无任何关联，未受其认可或赞助。《边狱巴士 / Limbus Company》的全部游戏内容、角色、名称与数值版权归 **Project Moon** 所有。本工具完全免费、非商业用途，仅用于学习与交流。所有数值以游戏内实际表现为准。如有侵权请联系本人，将立即删除。

### License

代码以 [MIT License](LICENSE) 发布（游戏数据版权不属于本项目，见上方免责声明）。

---
## English

A player-made stat tool for **Limbus Company**: calculates personality skill **exact damage expectation** (full coin-flip enumeration), **contest win rates** (Monte Carlo simulation), and **cycle DPT** (weighted by deck frequency), supporting E.G.O resource models and Bleed/Burn/Sink DoT calculations. Data sourced from the Limbus Company wiki.

### Features

- 📊 **Exact Damage Distribution**: Enumerates all 2ⁿ coin outcomes for skills, outputs expectation / standard deviation / damage range
- ⚔️ **Contest Simulation**: Full contest rules Monte Carlo (win rate + remaining coin expectation)
- 🔄 **Cycle Damage**: Calculates total damage per cycle and expected per turn (DPT) based on deck composition (S1×3 / S2×2 / S3×1 adjustable)
- ✨ **E.G.O Model**: Sin resource balance check, max activation = min(sin income ÷ consumption), includes opportunity cost of card replacements
- 🩸 **DoT Calculations**: Models Bleed (triggered on target action) / Sink (triggered when hit) / Burn (triggered at turn end)
- 🌐 **One-click Data Import**: Built-in stat data for all 184 personalities + 110 E.G.O, ready to search and use
- 🛠️ **Custom Skill Sets**: Combine skills from different personalities, adjust power (enhanced skill variants), edit counts, add DoT
- 📤 Excel report export; single Windows exe, no install needed

### Download & Use

1. Download `Limbus Company DPS Calculator.exe` from [Releases](../../releases)
2. Double-click to run (no Python environment needed)
3. Click "Import Personality from Wiki" to load the personalities you want, set environment parameters, click "Calculate Damage Expectation"

> ⚠️ **Virus Warning**: This program is packaged with PyInstaller and lacks a code-signing certificate, so Windows SmartScreen / some antivirus software may flag it. This is a known false positive. If concerned, you can run directly from source:
> ```bash
> pip install openpyxl
> python limbus_gui.py
> ```

### Data Sources

Identity, E.G.O and skill statistics are fetched via jsDelivr CDN from the unpacked game database monthofjune/limbus_data. Credits to the maintainers.
Damage formulas are community reverse‑engineered consensus (1.2× crit multiplier, ±3% per level difference, etc.) and not officially published. Relevant parameters are centrally configurable in the CFG section of the source code.
Known Simplifications
DoT values are upper‑bound estimates; layer overflow, Stagger zones and resistances are not simulated.
Corroded E.G.O and passives are not modelled.
Conditional buffs (e.g. power gain from Charge) require manual cond field configuration in the data.
Disclaimer
This tool is a non‑official fan work, not affiliated with, endorsed or sponsored by Project Moon. All in‑game content, characters, names and numerical values of Limbus Company are copyright property of Project Moon. This tool is completely free and non‑commercial, intended only for study and discussion. All values should be cross‑referenced against actual in‑game behaviour. Please contact the author in case of copyright concerns and the project will be taken down immediately.
License
Code is released under the MIT License (game assets and data are not covered by this license; see the disclaimer above).

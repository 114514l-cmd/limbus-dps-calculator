# -*- coding: utf-8 -*-
"""无头测试：程序化调用 App 各功能，定位无效功能"""
import sys, traceback
sys.path.insert(0, ".")
import limbus_gui as G

results = []
def check(name, fn):
    try:
        fn(); results.append((name, "OK"))
    except Exception as e:
        results.append((name, f"FAIL: {e}"))
        traceback.print_exc()

app = G.App(); app.withdraw()

# 1. 主计算
check("主界面计算", lambda: app.calc())
# 2. 切换人格
def t2():
    app.ident_cb.current(2); app.refresh_skills(); app.calc()
check("切换人格+重算", t2)
# 3. 拼点（需要选中两行）
def t3():
    app.calc()
    kids = app.tree.get_children()
    app.tree.selection_set(kids[:2])
    import tkinter.messagebox as mb
    mb.showinfo = lambda *a, **k: None
    app.clash()
check("拼点模拟", t3)
# 4. 导出自定义弹窗流程（模拟添加）
def t4():
    app.custom_deck_dialog()
check("打开自定义技能组窗口", t4)
# 5. 新增人格弹窗
check("打开新增人格窗口", lambda: app.add_identity_dialog())
# 6. Wiki 模块
def t6():
    import wiki_fetch
    rows = wiki_fetch.list_identities()
    assert len(rows) > 100
    ident = wiki_fetch.convert_identity(rows[0][1])
    assert len(ident["skills"]) == 3
    e = wiki_fetch.convert_ego(wiki_fetch.list_egos()[0][1])
    assert e["cost"]
check("Wiki数据获取+转换", t6)
# 7. 自定义卡组计算逻辑
def t7():
    deck = [{"name":"S1","base_power":4,"coin_power":[3,3],"dmg_type":"slash","sin":"lust","copies":3},
            {"name":"E.G.O X","base_power":18,"coin_power":[6],"dmg_type":"pierce","sin":"gloom",
             "copies":1,"cost":{"lust":2},"is_ego":True},
            {"name":"S2","base_power":5,"coin_power":[4,4,4],"dmg_type":"blunt","sin":"gloom",
             "copies":2,"dot":{"type":"bleed","potency":3,"count":2}}]
    inc = G.sin_income(deck); assert inc == {"lust":3,"gloom":2}, inc
    uses = G.ego_uses(deck[1], inc); assert uses == 1, uses
    tot, det, hits = G.dot_cycle_damage(deck, enemy_flips=12)
    assert tot == 3*min(2,12)*2, tot
check("E.G.O/DoT引擎逻辑", t7)

app.destroy()
print("\n===== 测试结果 =====")
for n, r in results: print(f"  {n}: {r}")

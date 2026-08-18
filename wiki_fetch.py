# -*- coding: utf-8 -*-
"""
从 Wiki 数据源获取边狱巴士人格数据
数据源：monthofjune/limbus_data (GitHub, 经 jsdelivr CDN 加速)
包含全部184个人格的官方技能数值（基础威力/硬币威力/硬币数/伤害类型/罪孽属性）
"""
import json, os, sys, urllib.request

CDN = "https://cdn.jsdelivr.net/gh/monthofjune/limbus_data@main/{}"
FILES = ["identities.json", "identities_detail.json", "skills.json",
         "egos.json", "egos_detail.json"]
if getattr(sys, "frozen", False):
    _BASE = os.path.dirname(sys.executable)  # exe 同目录，可写
else:
    _BASE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(_BASE, "wiki_cache")


def _download(name):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, name)
    req = urllib.request.Request(CDN.format(name), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        open(path, "wb").write(r.read())
    return path


def load_source(refresh=False):
    """加载(或下载)源数据，返回 (identities, details, skills)"""
    out = []
    for name in FILES:
        path = os.path.join(CACHE_DIR, name)
        if refresh or not os.path.exists(path):
            path = _download(name)
        out.append(json.load(open(path, encoding="utf-8")))
    return out


def list_egos(refresh=False):
    """返回可选E.G.O列表：[(显示名, ego_id)]"""
    _, _, _, egos, _ = load_source(refresh)
    SINNER = {1:"Yi Sang",2:"Faust",3:"Don Quixote",4:"Ryoshu",5:"Meursault",6:"Hong Lu",
              7:"Heathcliff",8:"Ishmael",9:"Rodion",10:"Sinclair",11:"Outis",12:"Gregor"}
    rows = [(f"[{e['rarity'].upper()}] {e['name']} ({SINNER.get(e['sinnerId'],'?')})", e["id"]) for e in egos]
    rows.sort(key=lambda x: x[1])
    return rows


def convert_ego(ego_id, uptie="max"):
    """把E.G.O转换为技能格式（带罪孽消耗cost）"""
    _, _, skills, egos, egos_det = load_source()
    meta = next(e for e in egos if e["id"] == ego_id)
    det = egos_det[str(ego_id)]
    sk = skills[str(det["awakeningSkill"])]
    st = sk["stats"][-1] if uptie == "max" else sk["stats"][0]
    name = sk["levels"][-1]["name"] or meta["name"]
    return {
        "name": f"E.G.O {meta['name']}",
        "base_power": st["base"],
        "coin_power": [st["coin"]] * st["coins"],
        "dmg_type": meta.get("attackType") or sk.get("attackType") or "slash",
        "sin": meta.get("sin") or sk.get("sin") or "gloom",
        "cost": meta.get("resourceCost", {}),
        "is_ego": True,
    }


def list_identities(refresh=False):
    """返回可选人格列表：[(显示名, id)]，按罪人编号+星级排序"""
    idents, _, _, _, _ = load_source(refresh)
    rows = [(f"{'★' * i['star']} {i['title']} {i['name']}", i["id"]) for i in idents]
    rows.sort(key=lambda x: (x[1] // 100, -len(x[0].split(' ')[0]), x[0]))
    return rows


def convert_identity(ident_id, offense_level=50, uptie="max"):
    """把一个人格转换为本程序的 identities.json 格式。
    uptie: 'max' 取最高同步等级的数值。"""
    idents, details, skills, _, _ = load_source()
    meta = next(i for i in idents if i["id"] == ident_id)
    det = details[str(ident_id)] if str(ident_id) in details else details[ident_id]
    out_skills = []
    for atk in det["attackSkills"]:
        sk = skills[str(atk["skillId"])]
        if sk.get("defType") != "attack":
            continue
        stats = sk["stats"]
        st = stats[-1] if uptie == "max" else stats[0]
        name = sk["levels"][-1]["name"] or f"Skill {atk['slot']}"
        out_skills.append({
            "name": f"S{atk['slot']} {name}",
            "base_power": st["base"],
            "coin_power": [st["coin"]] * st["coins"],
            "dmg_type": sk.get("attackType") or "slash",
            "sin": sk.get("sin") or "gloom",
            "copies": atk.get("copies", {1: 3, 2: 2, 3: 1}.get(atk["slot"], 1)),
        })
    return {
        "name": f"{meta['title']} {meta['name']}",
        "note": f"Wiki数据 ｜ {'★' * meta['star']} ｜ 关键词:{','.join(meta.get('keywords', []))}",
        "offense_level": offense_level,
        "skills": out_skills,
    }


if __name__ == "__main__":
    rows = list_identities(refresh=True)
    print(f"共 {len(rows)} 个人格，示例：")
    for r in rows[:5]: print(" ", r)
    sample = convert_identity(rows[10][1])
    print(json.dumps(sample, ensure_ascii=False, indent=2))

import bpy
# MIT License - Carlsu 2023
# You can support me here: https://ko-fi.com/carlsu
# 
# This version is for the add-on, see translate_mmd.py for the script

VRChat = {
    "vrc.v_aa": "あ", 
    "vrc.v_ch": "ち",
    "vrc.v_dd": "ど",
    "vrc.v_e": "え",
    "vrc.v_ff": "ふ",
    "vrc.v_ih": "い",
    "vrc.v_kk": "か",
    "vrc.v_nn": "ん",
    "vrc.v_oh": "お",
    "vrc.v_ou": "う",
    "vrc.v_pp": "ぱ",
    "vrc.v_rr": "ら",
    "vrc.v_sil": "っ",
    "vrc.v_ss": "す",
    "vrc.v_th": "て"
}
Eyes = {
    "Blink": "まばたき",
    "Smile": "笑い",
    "Wink": "ウィンク",
    "Wink-a": "ウィンク右",
    "Wink-b": "ウィンク２",
    "Wink-c": "ｳｨﾝｸ２右",
    "Howawa": "なごみ",
    "> <": "はぅ",
    "Ha!!!": "びっくり",
    "Jito-eye": "じと目",
    "Kiri-eye": "ｷﾘｯ",
    "O O": "はちゅ目",
    "EyeStar": "星目",
    "EyeHeart": "はぁと",
    "EyeSmall": "瞳小",
    "EyeSmall-v": "瞳縦潰れ",
    "EyeUnderli": "光下",
    "EyeFunky": "恐ろしい子！",
    "EyeHi-off": "ハイライト消",
    "EyeRef-off": "映り込み消",
    "Joy": "喜び",
    "Wao?!": "わぉ?!",
    "Howawa ω": "なごみω",
    "Wail": "悲しむ",
    "Hostility": "敵意"
}
Mouth = {
    "a": "あ",
    "i": "い",
    "u": "う",
    "e": "え",
    "o": "お",
    "a 2": "あ２",
    "n": "ん",
    "Mouse_1": "▲",
    "Mouse_2": "∧",
    "□": "□",
    "Wa": "ワ",
    "Omega": "ω",
    "ω□": "ω□",
    "Niyari": "にやり",
    "Niyari2": "にやり２",
    "Smile": "にっこり",
    "Pero": "ぺろっ",
    "Bero-tehe": "てへぺろ",
    "Bero-tehe2": "てへぺろ２",
    "MouseUP": "口角上げ",
    "MouseDW": "口角下げ",
    "MouseWD": "口横広げ",
    "ToothAnon": "歯無し上",
    "ToothBnon": "歯無し下"
}
Brows = {
    "Serious": "真面目",
    "Trouble": "困る",
    "Smily": "にこり",
    "Get angry": "怒り",
    "UP": "上",
    "Down": "下"
}

def return_translations(vrc=True, eyes=True, mouth=True, brows=True):
    out = []
    out.append(["-- VRChat --"]+[f"{k}: {v}" for k, v in VRChat.items()] if vrc else [])
    out.append(["-- Eyes --"]+[f"{k}: {v}" for k, v in Eyes.items()] if eyes else [])
    out.append(["-- Mouth --"]+[f"{k}: {v}" for k, v in Mouth.items()] if mouth else [])
    out.append(["-- Brows --"]+[f"{k}: {v}" for k, v in Brows.items()] if brows else [])
    return out

def mmd_duplicate(move_keys=False, skip_duplicates=True, force_lowercase=False, vrc=True, eyes=True, mouth=True, brows=True):
    """move_keys: If True, will move each key to it's original key (slow)"""
    obj = bpy.context.object
    assert obj.type == "MESH", "Object needs to be a mesh"
    shapekeys = obj.data.shape_keys
    assert shapekeys, "No shapekeys found"
    shapekeys = shapekeys.key_blocks
    
    def top_to_bottom(index:int) -> None:
        bpy.ops.object.shape_key_move(type='TOP')
        for i in range(index):
            bpy.ops.object.shape_key_move(type='DOWN')
        
    def bottom_to_top(index:int) -> None:
        for i in range(index):
            bpy.ops.object.shape_key_move(type='UP')
    
    def dict_update(dict1:dict, dict2:dict, force_lowercase:bool=False) -> None:
        keys_lower = lambda x: {k.lower(): v for k, v in x.items()}
        dict1.update(keys_lower(dict2) if force_lowercase else dict2)
    
    assert vrc or eyes or mouth or brows, "At least one of vrc, eyes, mouth, brows must be True"
    translate = {}
    dict_update(translate, VRChat, force_lowercase) if vrc else None
    dict_update(translate, Eyes, force_lowercase) if eyes else None
    dict_update(translate, Mouth, force_lowercase) if mouth else None
    dict_update(translate, Brows, force_lowercase) if brows else None
            
    only_active = bpy.context.object.show_only_shape_key
    bpy.context.object.show_only_shape_key = True
    
    i = 0
    for key_index, key in enumerate(shapekeys):
        
        name = key.name.lower() if force_lowercase else key.name
        if name not in translate: continue
        new_name = translate[name]
        if skip_duplicates and translate[name] in shapekeys: continue
        
        obj.active_shape_key_index = key_index + i
        obj.shape_key_add(name=new_name, from_mix=True)
        new_index = len(shapekeys) - 1
        obj.active_shape_key_index = new_index
        if not move_keys: continue
        
        if new_index / 2 > key_index + i: # Distance from new_key to active_key is more than half of length of shapekeys
            top_to_bottom(key_index + i)
        else:
            bottom_to_top(new_index - key_index - 1 - i)
        i += 1
    
    bpy.context.object.show_only_shape_key = only_active
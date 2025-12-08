from PySide6 import QtWidgets, QtGui, QtCore
import substance_painter as sp
import itertools
import math
import os

plugin_widgets = []
MAX_PER_ROW = 10

# 新規にレイヤーを作るかどうかを制御するフラグ
add_layer_switch_flag = True
add_layer_switch_btn = None

# マスクを作成せずに塗りつぶしレイヤーに直接エフェクトを割り当てるかどうかを制御するフラグ
add_fill_layer_effect_switch_flag = False
add_fill_layer_effect_switch_btn = None

# エフェクト名とiconのファイル名を設定
icon_dir = {
    "Switch": "icon_Switch.png",
    "Mask": "icon_Mask.png",
    "Paint": "icon_Paint.png",
    "Fill": "icon_Fill.png",
    "Filter": "icon_Filter.png",
    "Generator": "icon_Generator.png",
    "Levels": "icon_Levels.png",
    "CompareMask": "icon_CompareMask.png",
    "ColorSelection": "icon_ColorSelection.png",
    "AnchorPoint": "icon_AnchorPoint.png",
    "icon_add_effect_layer": "icon_add_effect_layer.png",
    "AmbientOcclusion": "icon_AmbientOcclusion.png",
    "Curvature": "icon_Curvature.png",
    "Position": "icon_Position.png",
    "MaskEditor": "icon_MaskEditor.png",
    "Blur": "icon_Blur.png",
    "BlurDirectional": "icon_BlurDirectional.png",
    "Invert": "icon_Invert.png",
    "Transform": "icon_Transform.png",
    "Warp": "icon_Warp.png"   
}

# SwitchButtonがOFFのとき
NORMAL_STYLE = """
    QToolButton {
        border: none;
        background: transparent;
        padding: 0px;
        margin: 0px;
    }
    QToolButton:hover {
        background: rgba(255,255,255,0.04);
    }
    QToolButton:pressed {
        background: rgba(255,255,255,0.08);
    }
"""

# SwitchButtonがONのとき
SELECTED_STYLE = """
    QToolButton {
        border: none;
        background: rgba(255,255,255,0.10);
        padding: 0px;
        margin: 0px;
    }
    QToolButton:hover {
        background: rgba(255,255,255,0.12);
    }
    QToolButton:pressed {
        background: rgba(255,255,255,0.15);
    }
"""

def start_plugin():
    global add_layer_switch_btn, add_fill_layer_effect_switch_btn

    btn_size = 28
    plugin_dir = os.path.dirname(__file__) + "/icon"

    widget = QtWidgets.QWidget()
    widget.setWindowTitle("Add Effect")

    # 外側は縦レイアウト。行（HBox）が増えるイメージ
    outer_layout = QtWidgets.QVBoxLayout(widget)
    outer_layout.setContentsMargins(0,0,0,0)
    outer_layout.setSpacing(0)

    # アイコンのリスト化（順序を保つ）
    items = list(icon_dir.items())
    total = len(items)
    if total == 0:
        sp.ui.add_dock_widget(widget)
        plugin_widgets.append(widget)
        return

    # 必要行数
    rows = math.ceil(total / MAX_PER_ROW)

    # iterator を作って islice で分割していく（元の順を保持）
    it = iter(items)
    for r in range(rows):
        # その行専用のコンテナ＆横レイアウト
        row_container = QtWidgets.QWidget()
        row_layout = QtWidgets.QHBoxLayout(row_container)
        row_layout.setContentsMargins(0,0,0,0)
        row_layout.setSpacing(0)

        # その行に入れる要素数
        for effect_name, path_dir in itertools.islice(it, 0, MAX_PER_ROW):
            icon_path = os.path.join(plugin_dir, path_dir)
            icon = QtGui.QIcon(icon_path)
            if icon.isNull():
                print(f"「{plugin_dir}」内に{effect_name}のアイコンが存在しないか読み込めません：{icon_path}")

            btn = make_tool_btn(icon, btn_size, effect_name)
            row_layout.addWidget(btn)

            # Switchボタンだけ
            if effect_name == "Switch":
                add_layer_switch_btn = btn
                btn.clicked.connect(on_add_layer_button_switch_clicked)
            elif effect_name == "icon_add_effect_layer":
                add_fill_layer_effect_switch_btn = btn
                btn.clicked.connect(on_add_fill_layer_effect_button_switch_clicked)
            else:
                btn.clicked.connect(lambda checked=False, n=effect_name: on_button_clicked(n))

        outer_layout.addWidget(row_container, 0, QtCore.Qt.AlignLeft)

    # 必要なら伸縮を抑えるために余白用の伸ばしを追加
    outer_layout.addStretch(1)

    sp.ui.add_dock_widget(widget)
    plugin_widgets.append(widget)


# ボタン作成
def make_tool_btn(icon, btn_size, effect_name):
    tb = QtWidgets.QToolButton()
    tb.setIcon(icon)
    tb.setIconSize(QtCore.QSize(btn_size, btn_size))
    tb.setToolTip(effect_name) 
    tb.setFixedSize(btn_size, btn_size)
    tb.setAutoRaise(True)
    tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
    tb.setFocusPolicy(QtCore.Qt.NoFocus)
    tb.setStyleSheet(NORMAL_STYLE)
    if effect_name == "Switch" and add_layer_switch_flag:
        tb.setStyleSheet(SELECTED_STYLE)
    return tb

# switch_buttonの作成
def on_add_layer_button_switch_clicked():
    global add_layer_switch_flag, add_layer_switch_btn
    add_layer_switch_flag = not(add_layer_switch_flag)

    if add_layer_switch_flag:
        add_layer_switch_btn.setStyleSheet(SELECTED_STYLE)
    else:
        add_layer_switch_btn.setStyleSheet(NORMAL_STYLE)


def on_add_fill_layer_effect_button_switch_clicked():
    global add_fill_layer_effect_switch_flag, add_fill_layer_effect_switch_btn
    add_fill_layer_effect_switch_flag = not(add_fill_layer_effect_switch_flag)

    if add_fill_layer_effect_switch_flag:
        add_fill_layer_effect_switch_btn.setStyleSheet(SELECTED_STYLE)
    else:
        add_fill_layer_effect_switch_btn.setStyleSheet(NORMAL_STYLE)


# add_layer_switch_flagによって処理を切り替え
def on_button_clicked(effect_name):
    if add_layer_switch_flag:
        add_layer_mask_effect(effect_name)
    elif add_fill_layer_effect_switch_flag:
        add_layer_effect(effect_name)
    else:
        add_mask_effect(effect_name)


# 新規でレイヤー、マスク、エフェクトを追加
def add_layer_mask_effect(effect_name):
    global add_fill_layer_effect_switch_flag

    try:
        stack = sp.textureset.get_active_stack()
        insert_position = sp.layerstack.InsertPosition.from_textureset_stack(stack)
        new_layer = sp.layerstack.insert_fill(insert_position)
        new_layer.set_name("Fill layer")

        if not new_layer.has_mask():
            mask_background = sp.layerstack.MaskBackground.Black
            new_layer.add_mask(mask_background)
        if add_fill_layer_effect_switch_flag:
            position_mask_effect_stack = sp.layerstack.InsertPosition.inside_node(new_layer, sp.layerstack.NodeStack.Content)
        else:
            position_mask_effect_stack = sp.layerstack.InsertPosition.inside_node(new_layer, sp.layerstack.NodeStack.Mask)

        set_effet(effect_name, position_mask_effect_stack)

    except Exception as e:
        print(f"スクリプト処理中に予期せぬ例外が発生しました: {e}")


def add_layer_effect(effect_name):
    try:
        stack = sp.textureset.get_active_stack()
        if not stack:
            print("アクティブなテクスチャセットがありません。処理を終了します。")
            return 

        selected_nodes = sp.layerstack.get_selected_nodes(stack)
        if not selected_nodes:
            print("ノードが選択されていません。処理を終了します。")
            return

        for layer in selected_nodes:
            position_effect_stack = sp.layerstack.InsertPosition.inside_node(layer, sp.layerstack.NodeStack.Content)
            set_effet(effect_name, position_effect_stack)

    except Exception as e:
        print(f"スクリプト処理中に予期せぬ例外が発生しました: {e}")


# 既存のレイヤーにマスク、エフェクトを追加
def add_mask_effect(effect_name):
    try:
        stack = sp.textureset.get_active_stack()
        if not stack:
            print("アクティブなテクスチャセットがありません。処理を終了します。")
            return 

        selected_nodes = sp.layerstack.get_selected_nodes(stack)
        if not selected_nodes:
            print("ノードが選択されていません。処理を終了します。")
            return

        for layer in selected_nodes:
            if hasattr(layer, "has_mask") and hasattr(layer, "add_mask"):
                if not layer.has_mask():
                    mask_bg = sp.layerstack.MaskBackground.Black
                    layer.add_mask(mask_bg)
                    print("マスクを追加しました")
                position_mask_effect_stack = sp.layerstack.InsertPosition.inside_node(layer, sp.layerstack.NodeStack.Mask)
                set_effet(effect_name, position_mask_effect_stack)
            else:
                print("このノードにはマスクを追加できません")

    except Exception as e:
        print(f"スクリプト処理中に予期せぬ例外が発生しました: {e}")


# 付与するエフェクトを設定
def set_effet(effect_name, position):
    try:
        if (effect_name == "Mask"):
            return
        elif (effect_name == "Paint"):
            sp.layerstack.insert_paint(position) 
        elif (effect_name == "Fill"):
            sp.layerstack.insert_fill(position) 
        elif (effect_name == "Levels"):
            sp.layerstack.insert_levels_effect(position) 
        elif (effect_name == "CompareMask"):
            if add_fill_layer_effect_switch_flag:
                return print("塗りつぶしレイヤーに直接追加することはできません。")
            sp.layerstack.insert_compare_mask_effect(position) 
        elif (effect_name == "ColorSelection"):
            if add_fill_layer_effect_switch_flag:
                return print("塗りつぶしレイヤーに直接追加することはできません。")
            sp.layerstack.insert_color_selection_effect(position) 
        elif (effect_name == "AnchorPoint"):
            sp.layerstack.insert_anchor_point_effect(position, "AnchorPoint") 
        elif (effect_name == "Generator"):
            sp.layerstack.insert_generator_effect(position) 
        elif (effect_name == "Filter"):
            sp.layerstack.insert_filter_effect(position) 
        elif (effect_name == "AmbientOcclusion"):
            effect_resource = sp.resource.search("s:starterassets u:generator n:Ambient\\ Occlusion")[0]
            sp.layerstack.insert_generator_effect(position, effect_resource.identifier()) 
        elif (effect_name == "Curvature"):
            effect_resource = sp.resource.search("s:starterassets u:generator n:Curvature")[0]
            sp.layerstack.insert_generator_effect(position, effect_resource.identifier()) 
        elif (effect_name == "Position"):
            effect_resource = sp.resource.search("s:starterassets u:generator n:Position")[0]
            sp.layerstack.insert_generator_effect(position, effect_resource.identifier()) 
        elif (effect_name == "MaskEditor"):
            effect_resource = sp.resource.search("s:starterassets u:generator n:Mask\\ Editor")[0]
            sp.layerstack.insert_generator_effect(position, effect_resource.identifier()) 
        elif (effect_name == "Blur"):
            effect_resource = sp.resource.search("s:starterassets u:filter n:Blur")[0]
            sp.layerstack.insert_filter_effect(position, effect_resource.identifier()) 
        elif (effect_name == "BlurDirectional"):
            effect_resource = sp.resource.search("s:starterassets u:filter n:Blur\\ Directional")[0]
            sp.layerstack.insert_filter_effect(position, effect_resource.identifier()) 
        elif (effect_name == "Invert"):
            effect_resource = sp.resource.search("s:starterassets u:filter n:Invert")[0]
            sp.layerstack.insert_filter_effect(position, effect_resource.identifier()) 
        elif (effect_name == "Warp"):
            effect_resource = sp.resource.search("s:starterassets u:filter n:Warp")[0]
            sp.layerstack.insert_filter_effect(position, effect_resource.identifier()) 
        elif (effect_name == "Transform"):
            effect_resource = sp.resource.search("s:starterassets u:filter n:Transform")[0]
            sp.layerstack.insert_filter_effect(position, effect_resource.identifier()) 
    except Exception as e:
        print(f"Effect付与中に予期せぬ例外が発生しました。: {e}")


def close_plugin():
    for w in plugin_widgets:
        sp.ui.delete_ui_element(w)
    plugin_widgets.clear()


if __name__ == "__main__":
    start_plugin()

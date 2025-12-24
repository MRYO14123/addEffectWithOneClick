from PySide6 import QtWidgets, QtGui, QtCore
import substance_painter as sp
import itertools
import math
import os

plugin_widgets = []
MAX_PER_ROW = 10

# 新規にレイヤーを作るかどうかを制御するフラグ
add_layer_switch_flag = False
add_layer_switch_btn = None

# 塗りつぶしレイヤーかマスクレイヤーか
selected_fill_or_mask = "mask"
selected_fill_layer_btn = None
selected_mask_layer_btn = None

not_attached_mask = ["ColorMatch", "HeightToNormal", "BakedLightingEnvironment", "BakedLightingStylized", "PBRValidate"]

effect_info_map = {
    "WhiteMask": {
        "icon": "icon_WhiteMaskLayer.png",
        "type": "node"
    },
    "Mask": {
        "icon": "icon_MaskLayer.png",
        "type": "node"
    },
    "Paint": {
        "icon": "icon_Paint.png",
        "type": "node"
    },
    "Fill": {
        "icon": "icon_Fill.png",
        "type": "node"
    },
    "Filter": {
        "icon": "icon_Filter.png",
        "type": "node"
    },
    "Generator": {
        "icon": "icon_Generator.png",
        "type": "node"
    },
    "Levels": {
        "icon": "icon_Levels.png",
        "type": "node"
    },
    "CompareMask": {
        "icon": "icon_CompareMask.png",
        "type": "node"
    },
    "ColorSelection": {
        "icon": "icon_ColorSelection.png",
        "type": "node"
    },
    "AnchorPoint": {
        "icon": "icon_AnchorPoint.png",
        "type": "node"
    },
    "AmbientOcclusion": {
        "icon": "icon_AmbientOcclusion.png",
        "type": "generator",
        "search": "s:starterassets u:generator n:Ambient\\ Occlusion"
    },
    "Curvature": {
        "icon": "icon_Curvature.png",
        "type": "generator",
        "search": "s:starterassets u:generator n:Curvature"
    },
     "Position": {
        "icon": "icon_Position.png",
        "type": "generator",
        "search": "s:starterassets u:generator n:Position"
    },
    "MaskEditor": {
        "icon": "icon_MaskEditor.png",
        "type": "generator",
        "search": "s:starterassets u:generator n:Mask\\ Editor"
    },
    "UVBorderDistance": {
        "icon": "icon_UVBorderDistance.png",
        "type": "generator",
        "search": "s:starterassets u:generator n:UV\\ Border\\ Distance"
    },
    "BakedLightingEnvironment": {
        "icon": "icon_BakedLightingEnvironment.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Baked\\ Lighting\\ Environment"
    },
    "BakedLightingStylized": {
        "icon": "icon_BakedLightingStylized.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Baked\\ Lighting\\ Stylized"
    },
    "Blur": {
        "icon": "icon_Blur.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Blur"
    },
    "BlurDirectional": {
        "icon": "icon_BlurDirectional.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Blur\\ Directional"
    },
    "BlurSlope": {
        "icon": "icon_BlurSlope.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Blur\\ Slope"
    },
    "Bevel": {
        "icon": "icon_Bevel.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Bevel"
    },
    "Clamp": {
        "icon": "icon_Clamp.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Clamp"
    },
    "Mirror": {
        "icon": "icon_Mirror.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Mirror"
    },
    "Invert": {
        "icon": "icon_Invert.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Invert"
    },
    "Transform": {
        "icon": "icon_Transform.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Transform"
    },
    "Warp": {
        "icon": "icon_Warp.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Warp"
    },
    "MaskOutline": {
        "icon": "icon_MaskOutline.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Mask\\ Outline"
    },
    "Sharpen": {
        "icon": "icon_Sharpen.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Sharpen"
    },
    "Smoothstep": {
        "icon": "icon_Smoothstep.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Smoothstep"
    },
    "Threshold": {
        "icon": "icon_Threshold.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Threshold"
    },
    "Highpass": {
        "icon": "icon_Highpass.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Highpass"
    },
    "HistogramScan": {
        "icon": "icon_HistogramScan.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Histogram\\ Scan"
    },
    "HistogramShift": {
        "icon": "icon_HistogramShift.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Histogram\\ Shift"
    },
    "ColorBalance": {
        "icon": "icon_ColorBalance.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Color\\ Balance"
    },
    "ColorCorrect": {
        "icon": "icon_ColorCorrect.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Color\\ Correct"
    },
    "ColorMatch": {
        "icon": "icon_ColorMatch.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Color\\ Match"
    },
    "HSLPerceptive": {
        "icon": "icon_HSLPerceptive.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:HSL\\ Perceptive"
    },
    "ContrastLuminosity": {
        "icon": "icon_ContrastLuminosity.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Contrast\\ Luminosity"
    },
    "FillAreaColor": {
        "icon": "icon_FillAreaColor.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Fill\\ Area\\ Color"
    },
    "FillAreaMask": {
        "icon": "icon_FillAreaMask.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Fill\\ Area\\ Mask"
    },
    "DropShadow": {
        "icon": "icon_DropShadow.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Drop\\ Shadow"
    },
    "FXAA": {
        "icon": "icon_FXAA.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:FXAA"
    },
    "Glow": {
        "icon": "icon_Glow.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Glow"
    },
    "Gradient": {
        "icon": "icon_Gradient.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Gradient"
    },
    "GradientCurve": {
        "icon": "icon_GradientCurve.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Gradient\\ Curve"
    },
    "GradientDynamic": {
        "icon": "icon_GradientDynamic.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Gradient\\ Dynamic"
    },
    "HeightAdjust": {
        "icon": "icon_HeightAdjust.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Height\\ Adjust"
    },
    "HeightToNormal": {
        "icon": "icon_HeightToNormal.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Height\\ To\\ Normal"
    },
    "Posterize": {
        "icon": "icon_Posterize.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:Posterize"
    },
    "PBRValidate": {
        "icon": "icon_PBRValidate.png",
        "type": "filter",
        "search": "s:starterassets u:filter n:PBR\\ Validate"
    }
}

EFFECT_BUTTON_STYLE = """
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

NORMAL_ADD_NEW_FILL_LAYER_BUTTON_STYLE = """
    QToolButton {
        border: 1px solid #4d4d4d;
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

SELECTED_ADD_NEW_FILL_LAYER_BUTTON_STYLE = """
    QToolButton {
        border: 1px solid #4d4d4d;
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

NORMAL_LAYER_STYLE = """
    QToolButton {
        border: 1px solid #4d4d4d;
        border-radius: 4px;
        background: rgba(51, 51, 51,0.10);
        padding: 0px;
        margin: 0px;
    }
    QToolButton:hover {
        background: rgba(34,60,90,1);
        border: 1px solid #378ef0;
    }
"""

SELECTED_LAYER_STYLE = """
    QToolButton {
        border-radius: 4px;
        border: 1px solid #378ef0;
        background: rgba(51, 51, 51,0.10);
        padding: 0px;
        margin: 0px;
    }
"""

def start_plugin():
    global add_layer_switch_btn, selected_fill_layer_btn, selected_mask_layer_btn

    plugin_dir = os.path.dirname(__file__) + "/icon"

    widget = QtWidgets.QWidget()
    widget.setWindowTitle("エフェクト追加ボタン")

    # 縦レイアウト
    outer_layout = QtWidgets.QVBoxLayout(widget)
    outer_layout.setContentsMargins(0,0,0,0)
    outer_layout.setSpacing(0)

    # 設定ボタン格納BOX
    setting_button_container = QtWidgets.QWidget()
    setting_button_layout = QtWidgets.QHBoxLayout(setting_button_container)
    setting_button_layout.setContentsMargins(0,0,0,0)
    setting_button_layout.setSpacing(3)
    
    # 新規追加ボタン
    new_layer_button = QtWidgets.QToolButton()
    new_layer_button.setText("新規追加")
    new_layer_button.setFixedSize(70,30)
    new_layer_button.setStyleSheet(NORMAL_ADD_NEW_FILL_LAYER_BUTTON_STYLE)
    new_layer_button.clicked.connect(on_add_layer_button_switch_clicked)
    setting_button_layout.addWidget(new_layer_button)
    
    add_layer_switch_btn = new_layer_button
    
    # FillLayerボタン
    fill_layer_button = QtWidgets.QToolButton()
    setting_icon_path = os.path.join(plugin_dir, "icon_FillLayer.png")
    setting_icon = QtGui.QIcon(setting_icon_path)
    fill_layer_button.setIcon(setting_icon)
    fill_layer_button.setIconSize(QtCore.QSize(30, 30))
    fill_layer_button.setFixedSize(30, 30)
    fill_layer_button.setAutoRaise(True)
    fill_layer_button.setStyleSheet(NORMAL_LAYER_STYLE)
    fill_layer_button.clicked.connect(on_selected_fill_layer_clicked)
    setting_button_layout.addWidget(fill_layer_button)

    selected_fill_layer_btn = fill_layer_button

    # MaskLayerボタン
    mask_layer_button = QtWidgets.QToolButton()
    setting_icon_path = os.path.join(plugin_dir, "icon_MaskLayer.png")
    setting_icon = QtGui.QIcon(setting_icon_path)
    mask_layer_button.setIcon(setting_icon)
    mask_layer_button.setIconSize(QtCore.QSize(30, 30))
    mask_layer_button.setFixedSize(30, 30)
    mask_layer_button.setAutoRaise(True)
    mask_layer_button.setStyleSheet(SELECTED_LAYER_STYLE)
    mask_layer_button.clicked.connect(on_selected_mask_layer_clicked)
    setting_button_layout.addWidget(mask_layer_button)

    selected_mask_layer_btn = mask_layer_button


    outer_layout.addWidget(setting_button_container, 0, QtCore.Qt.AlignLeft)
 
    # アイコンのリスト化
    items = list(effect_info_map.items())
    total = len(items)
    if total == 0:
        sp.ui.add_dock_widget(widget)
        plugin_widgets.append(widget)
        return

    # 必要行数
    rows = math.ceil(total / MAX_PER_ROW)

    it = iter(items)
    for r in range(rows):
        # 横レイアウト
        row_container = QtWidgets.QWidget()
        row_layout = QtWidgets.QHBoxLayout(row_container)
        row_layout.setContentsMargins(0,0,0,0)
        row_layout.setSpacing(0)

        for effect_name, effect_info in itertools.islice(it, 0, MAX_PER_ROW):

            icon_file = effect_info.get("icon")
            if not icon_file:
                sp.logging.warning(f"{effect_name} にiconが定義されていません")
                continue

            icon_path = os.path.join(plugin_dir, icon_file)
            icon = QtGui.QIcon(icon_path)

            if icon.isNull():
                sp.logging.warning(f"アイコンが読み込めません: {icon_path}")

            btn = make_tool_btn(icon, 17, 28, 28, effect_name)
            row_layout.addWidget(btn)

            btn.clicked.connect(lambda checked=False, n=effect_name, e=effect_info: on_button_clicked(n,e))

        outer_layout.addWidget(row_container, 0, QtCore.Qt.AlignLeft)

    outer_layout.addStretch(1)

    sp.ui.add_dock_widget(widget)
    plugin_widgets.append(widget)


# ボタン作成
def make_tool_btn(icon, icon_size, btn_size_w, btn_size_h, effect_name):
    tb = QtWidgets.QToolButton()
    tb.setIcon(icon)
    tb.setIconSize(QtCore.QSize(btn_size_w, btn_size_h))
    tb.setToolTip(effect_name) 
    tb.setFixedSize(btn_size_w, btn_size_h)
    tb.setAutoRaise(True)
    tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
    tb.setFocusPolicy(QtCore.Qt.NoFocus)
    tb.setStyleSheet(EFFECT_BUTTON_STYLE)
    return tb


# 新規追加ボタンのスタイル変更
def on_add_layer_button_switch_clicked():
    global add_layer_switch_flag, add_layer_switch_btn
    add_layer_switch_flag = not(add_layer_switch_flag)

    if add_layer_switch_flag:
        add_layer_switch_btn.setStyleSheet(SELECTED_ADD_NEW_FILL_LAYER_BUTTON_STYLE)
    else:
        add_layer_switch_btn.setStyleSheet(NORMAL_ADD_NEW_FILL_LAYER_BUTTON_STYLE)


# 塗りつぶしレイヤーのスタイル変更と値更新
def on_selected_fill_layer_clicked():
    global selected_fill_or_mask, selected_fill_layer_btn, selected_mask_layer_btn
    if not selected_fill_or_mask == "fill":
        selected_fill_layer_btn.setStyleSheet(SELECTED_LAYER_STYLE)
        selected_mask_layer_btn.setStyleSheet(NORMAL_LAYER_STYLE)
        selected_fill_or_mask = "fill"
    

# マスクレイヤーのスタイル変更と値更新
def on_selected_mask_layer_clicked():
    global selected_fill_or_mask, selected_fill_layer_btn, selected_mask_layer_btn
    if not selected_fill_or_mask == "mask":
        selected_fill_layer_btn.setStyleSheet(NORMAL_LAYER_STYLE)
        selected_mask_layer_btn.setStyleSheet(SELECTED_LAYER_STYLE)
        selected_fill_or_mask = "mask"
    

# add_layer_switch_flagによって処理を切り替え
def on_button_clicked(effect_name, effect_info):
    global add_layer_switch_flag, selected_fill_or_mask
    if add_layer_switch_flag:
        add_layer_mask_effect(effect_name, effect_info)
    elif selected_fill_or_mask == "fill":
        add_layer_effect(effect_name, effect_info)
    elif selected_fill_or_mask == "mask":
        add_mask_effect(effect_name, effect_info)


# 新規でレイヤー、マスク、エフェクトを追加
def add_layer_mask_effect(effect_name, effect_info):
    global selected_fill_or_mask

    try:
        stack = sp.textureset.get_active_stack()
        insert_position = sp.layerstack.InsertPosition.from_textureset_stack(stack)
        new_layer = sp.layerstack.insert_fill(insert_position)
        new_layer.set_name("Fill layer")
        new_layer.set_source(sp.layerstack.ChannelType.BaseColor, sp.colormanagement.Color(0.735, 0.735, 0.735))
        new_layer.set_source(sp.layerstack.ChannelType.Metallic, sp.colormanagement.Color(0.0, 0.0, 0.0))
        new_layer.set_source(sp.layerstack.ChannelType.Roughness, sp.colormanagement.Color(0.3, 0.3, 0.3))
        new_layer.set_source(sp.layerstack.ChannelType.Normal, sp.colormanagement.Color(0.5, 0.5, 1.0))
        new_layer.set_source(sp.layerstack.ChannelType.Height, sp.colormanagement.Color(0.0, 0.0, 0.0))

        if not selected_fill_or_mask == "fill":
            mask_background = sp.layerstack.MaskBackground.Black
            if effect_name == "WhiteMask":
                mask_background = sp.layerstack.MaskBackground.White
            new_layer.add_mask(mask_background)
        if selected_fill_or_mask == "fill":
            position_mask_effect_stack = sp.layerstack.InsertPosition.inside_node(new_layer, sp.layerstack.NodeStack.Content)
        elif selected_fill_or_mask == "mask":
            position_mask_effect_stack = sp.layerstack.InsertPosition.inside_node(new_layer, sp.layerstack.NodeStack.Mask)

        set_effet(effect_name, position_mask_effect_stack, effect_info)

    except Exception as e:
        sp.logging.error(f"スクリプト処理中に予期せぬ例外が発生しました: {e}")


# 既存の塗りつぶしレイヤーにエフェクトを追加
def add_layer_effect(effect_name, effect_info):
    try:
        stack = sp.textureset.get_active_stack()
        if not stack:
            sp.logging.warning("アクティブなテクスチャセットがありません。処理を終了します。")
            return 

        selected_nodes = sp.layerstack.get_selected_nodes(stack)
        if not selected_nodes:
            sp.logging.warning("ノードが選択されていないため、エフェクトを追加できませんでした。")
            return

        for layer in selected_nodes:
            position_effect_stack = sp.layerstack.InsertPosition.inside_node(layer, sp.layerstack.NodeStack.Content)
            set_effet(effect_name, position_effect_stack, effect_info)

    except Exception as e:
        sp.logging.error(f"スクリプト処理中に予期せぬ例外が発生しました: {e}")


# 既存のレイヤーにマスク、エフェクトを追加
def add_mask_effect(effect_name, effect_info):
    try:
        stack = sp.textureset.get_active_stack()
        if not stack:
            sp.logging.warning("アクティブなテクスチャセットがありません。処理を終了します。")
            return 

        selected_nodes = sp.layerstack.get_selected_nodes(stack)
        if not selected_nodes:
            sp.logging.warning("ノードが選択されていないため、エフェクトを追加できませんでした。")
            return

        for layer in selected_nodes:
            if hasattr(layer, "has_mask") and hasattr(layer, "add_mask"):
                if not layer.has_mask():
                    mask_bg = sp.layerstack.MaskBackground.Black
                    if effect_name == "WhiteMask":
                        mask_bg = sp.layerstack.MaskBackground.White
                    layer.add_mask(mask_bg)
                position_mask_effect_stack = sp.layerstack.InsertPosition.inside_node(layer, sp.layerstack.NodeStack.Mask)
                set_effet(effect_name, position_mask_effect_stack, effect_info)
            else:
                sp.logging.warning("このノードにはマスクを追加できません")

    except Exception as e:
        sp.logging.error(f"スクリプト処理中に予期せぬ例外が発生しました: {e}")


# 付与するエフェクトを設定
def set_effet(effect_name, position, effect_info):
    global selected_fill_or_mask

    try:
        effect_type = effect_info["type"]

        if (effect_name == "Mask" or effect_name == "WhiteMask"):
            if selected_fill_or_mask == "fill":
                sp.logging.warning("塗りつぶしレイヤーに直接マスクを追加することはできません。")
            return
        elif (effect_name == "Paint"):
            sp.layerstack.insert_paint(position) 
        elif (effect_name == "Fill"):
            sp.layerstack.insert_fill(position) 
        elif (effect_name == "Levels"):
            sp.layerstack.insert_levels_effect(position) 
        elif (effect_name == "CompareMask"):
            if selected_fill_or_mask == "fill":
                return sp.logging.warning("塗りつぶしレイヤーに直接追加することはできません。")
            sp.layerstack.insert_compare_mask_effect(position) 
        elif (effect_name == "ColorSelection"):
            if selected_fill_or_mask == "fill" :
                return sp.logging.warning("塗りつぶしレイヤーに直接追加することはできません。")
            sp.layerstack.insert_color_selection_effect(position) 
        elif (effect_name == "AnchorPoint"):
            sp.layerstack.insert_anchor_point_effect(position, "AnchorPoint") 
        elif (effect_name == "Generator"):
            sp.layerstack.insert_generator_effect(position) 
        elif (effect_name == "Filter"):
            sp.layerstack.insert_filter_effect(position) 
        # effect_info_mapで設定した値を使用
        elif effect_type == "generator":
            res = sp.resource.search(effect_info["search"])[0]
            sp.layerstack.insert_generator_effect(position, res.identifier())
        elif effect_type == "filter":
            if effect_name in not_attached_mask and selected_fill_or_mask == "mask":
                return sp.logging.warning("マスクレイヤーに直接追加することはできません。")
            res = sp.resource.search(effect_info["search"])[0]
            sp.layerstack.insert_filter_effect(position, res.identifier())
    except Exception as e:
        sp.logging.error(f"Effect付与中に予期せぬ例外が発生しました。: {e}")


def close_plugin():
    for w in plugin_widgets:
        sp.ui.delete_ui_element(w)
    plugin_widgets.clear()


if __name__ == "__main__":
    start_plugin()


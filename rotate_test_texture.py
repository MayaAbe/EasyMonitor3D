import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

# 立方体の頂点座標
vertices = [
    (1, 1, -1), (1, -1, -1), (-1, -1, -1), (-1, 1, -1),
    (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1)
]

# 立方体の面
surfaces = [
    (0, 1, 2, 3),  # 背面
    (4, 5, 6, 7),  # 前面
    (0, 1, 5, 4),  # 右面
    (2, 3, 7, 6),  # 左面
    (0, 3, 7, 4),  # 上面 (top_image.png)
    (1, 2, 6, 5)   # 底面
]

# テクスチャ座標 (通常)
default_tex_coords = [
    (0, 0), (1, 0), (1, 1), (0, 1)
]

# 時計回りに90度回転させる (front_image.png, right_image.png)
tex_coords_cw_90 = [
    (1, 0), (1, 1), (0, 1), (0, 0)
]

# 反時計回りに90度回転させる (left_image.png)
tex_coords_ccw_90 = [
    (0, 1), (0, 0), (1, 0), (1, 1)
]

# 180度回転させる (bottom_image.png)
tex_coords_180 = [
    (1, 1), (0, 1), (0, 0), (1, 0)
]

# back_image.pngの上下を入れ替えたあと、時計回りに180度回転させる
tex_coords_flip_and_rotate_180 = [
    (0, 0), (0, 1), (1, 1), (1, 0)
]

# top_image.pngを裏返した後、180度回転させる
tex_coords_flip_top_180 = [
    (1, 0), (0, 0), (0, 1), (1, 1)
]

# 背景画像を反時計回りに180度回転させるテクスチャ座標
background_tex_coords_180 = [
    (1, 1), (0, 1), (0, 0), (1, 0)
]

# 背景用の四角形
background_vertices = [
    (-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)
]

# 画像をテクスチャとして読み込む
def load_texture(image_path):
    img = Image.open(image_path)
    img_data = img.convert("RGBA").tobytes()
    width, height = img.size
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture_id

# 背景の描画
def draw_background(texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for i, vertex in enumerate(background_vertices):
        glTexCoord2fv(background_tex_coords_180[i])  # 背景を反時計回りに180度回転させた座標
        glVertex3fv(vertex)
    glEnd()

# 立方体の描画
def draw_textured_cube(textures):
    for i, surface in enumerate(surfaces):
        glBindTexture(GL_TEXTURE_2D, textures[i])
        glBegin(GL_QUADS)
        # 各面に対して適切なテクスチャ座標を使用
        if i == 1:  # front_image.png (時計回りに90度)
            tex_coords = tex_coords_cw_90
        elif i == 2:  # right_image.png (時計回りに90度)
            tex_coords = tex_coords_cw_90
        elif i == 3:  # left_image.png (反時計回りに90度)
            tex_coords = tex_coords_ccw_90
        elif i == 0:  # back_image.png (上下反転+180度回転)
            tex_coords = tex_coords_flip_and_rotate_180
        elif i == 5:  # bottom_image.png (180度回転)
            tex_coords = tex_coords_180
        elif i == 4:  # top_image.png (裏返し+180度回転)
            tex_coords = tex_coords_flip_top_180
        else:  # それ以外は通常のテクスチャ座標
            tex_coords = default_tex_coords

        for j, vertex in enumerate(surface):
            glTexCoord2fv(tex_coords[j])  # 各面ごとのテクスチャ座標
            glVertex3fv(vertices[vertex])
        glEnd()

# 立方体の回転
def rotate_model(pitch, yaw, roll):
    glRotatef(pitch, 1, 0, 0)
    glRotatef(yaw, 0, 1, 0)
    glRotatef(roll, 0, 0, 1)

# ウィンドウのリサイズに対応してアスペクト比を調整
def resize_viewport(width, height):
    if height == 0:
        height = 1  # ゼロ除算を防ぐ
    aspect_ratio = width / height
    glViewport(0, 0, width, height)  # ウィンドウ全体に描画

    # 視点の設定
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, aspect_ratio, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# メイン処理
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)  # リサイズ可能に設定

    resize_viewport(display[0], display[1])  # 初期のアスペクト比を設定

    # 背景のテクスチャを読み込み
    background_texture = load_texture('background_image.png')  # 背景画像のパス

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    # 各面に張り付ける画像ファイルのパスを指定
    texture_paths = [
        'back_image.png',   # 背面
        'front_image.png',  # 前面
        'right_image.png',  # 右面
        'left_image.png',   # 左面
        'top_image.png',    # 上面
        'bottom_image.png'  # 底面
    ]

    textures = [load_texture(path) for path in texture_paths]

    pitch, yaw, roll = 0, 0, 0
    rotation_speed = 1.0

    clock = pygame.time.Clock()
    target_fps = 60

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # ウィンドウがリサイズされたときに呼び出し
            if event.type == VIDEORESIZE:
                resize_viewport(event.w, event.h)

        # 画面クリア
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 背景の描画
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)  # 背景描画時は深度テストを無効
        glTranslatef(0.0, 0.0, -1)  # 背景をカメラの後ろに表示
        draw_background(background_texture)
        glEnable(GL_DEPTH_TEST)  # 背景描画後に深度テストを再び有効化

        # 3D立方体を描画
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)  # 立方体の位置を調整
        pitch += rotation_speed
        yaw += rotation_speed
        roll += rotation_speed
        rotate_model(pitch, yaw, roll)
        draw_textured_cube(textures)

        pygame.display.flip()
        clock.tick(target_fps)

if __name__ == "__main__":
    main()

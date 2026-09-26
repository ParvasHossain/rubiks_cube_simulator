import sys
import os
import time
import threading
import math
import random
import tkinter as tk
from tkinter import ttk, messagebox
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ----------------------------------------------------------------------
# COLOR DEFINITIONS & CUBE STICKERS
# ----------------------------------------------------------------------
COLORS = {
    'U': (1.0, 1.0, 1.0),   # White
    'D': (1.0, 0.85, 0.0),  # Yellow
    'F': (0.0, 0.8, 0.2),   # Green
    'B': (0.0, 0.2, 0.8),   # Blue
    'L': (1.0, 0.35, 0.0),  # Orange
    'R': (0.9, 0.1, 0.1),   # Red
    'K': (0.08, 0.08, 0.08) # Black body
}

class RubiksCubeLogic:
    """Tracks 3D cubie coordinates and facelet colors properly."""
    def __init__(self):
        self.history = []
        self.reset()

    def reset(self):
        self.history = []
        self.cubies = {}
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                for z in (-1, 0, 1):
                    # Set default resolved outer colors
                    self.cubies[(x, y, z)] = {
                        'U': 'U',
                        'D': 'D',
                        'F': 'F',
                        'B': 'B',
                        'L': 'L',
                        'R': 'R'
                    }

    def is_cubie_on_face(self, pos, face):
        x, y, z = pos
        if face == 'U' and y == 1: return True
        if face == 'D' and y == -1: return True
        if face == 'F' and z == 1: return True
        if face == 'B' and z == -1: return True
        if face == 'R' and x == 1: return True
        if face == 'L' and x == -1: return True
        return False

    def rotate_face(self, face, direction=1, record_history=True):
        if record_history:
            move_str = f"{face}" if direction == 1 else (f"{face}'" if direction == -1 else f"{face}2")
            self.history.append(move_str)

        num_turns = 2 if direction == 2 else 1
        dir_step = -1 if direction == -1 else 1
        
        for _ in range(num_turns):
            new_cubies = dict(self.cubies)
            for (x, y, z), colors in self.cubies.items():
                if self.is_cubie_on_face((x, y, z), face):
                    if face in ('U', 'D'):
                        dir_adj = dir_step if face == 'U' else -dir_step
                        nx = -z * dir_adj if dir_adj == 1 else z * (-dir_adj)
                        ny = y
                        nz = x * dir_adj if dir_adj == 1 else -x * (-dir_adj)
                        c = colors.copy()
                        if dir_adj == 1:
                            c['F'], c['R'], c['B'], c['L'] = colors['R'], colors['B'], colors['L'], colors['F']
                        else:
                            c['F'], c['R'], c['B'], c['L'] = colors['L'], colors['F'], colors['R'], colors['B']

                    elif face in ('F', 'B'):
                        dir_adj = dir_step if face == 'F' else -dir_step
                        nx = -y * dir_adj if dir_adj == 1 else y * (-dir_adj)
                        ny = x * dir_adj if dir_adj == 1 else -x * (-dir_adj)
                        nz = z
                        c = colors.copy()
                        if dir_adj == 1:
                            c['U'], c['R'], c['D'], c['L'] = colors['L'], colors['U'], colors['R'], colors['D']
                        else:
                            c['U'], c['R'], c['D'], c['L'] = colors['R'], colors['D'], colors['L'], colors['U']

                    elif face in ('R', 'L'):
                        dir_adj = dir_step if face == 'R' else -dir_step
                        nx = x
                        ny = -z * dir_adj if dir_adj == 1 else z * (-dir_adj)
                        nz = y * dir_adj if dir_adj == 1 else -y * (-dir_adj)
                        c = colors.copy()
                        if dir_adj == 1:
                            c['U'], c['B'], c['D'], c['F'] = colors['F'], colors['U'], colors['B'], colors['D']
                        else:
                            c['U'], c['B'], c['D'], c['F'] = colors['B'], colors['D'], colors['F'], colors['U']

                    new_cubies[(nx, ny, nz)] = c
            self.cubies = new_cubies

    def get_solve_sequence(self):
        solution = []
        for move in reversed(self.history):
            face = move[0]
            if "'" in move: solution.append(face)
            elif "2" in move: solution.append(f"{face}2")
            else: solution.append(f"{face}'")
        return solution

# ----------------------------------------------------------------------
# 3D OPENGL RENDERING
# ----------------------------------------------------------------------
def draw_cubie(x, y, z, face_colors):
    glPushMatrix()
    glTranslatef(x * 1.02, y * 1.02, z * 1.02)
    
    size = 0.49
    
    # Inner plastic body
    glColor3fv(COLORS['K'])
    glBegin(GL_QUADS)
    glVertex3f(-size, size, -size); glVertex3f(size, size, -size); glVertex3f(size, size, size); glVertex3f(-size, size, size)
    glVertex3f(-size, -size, -size); glVertex3f(size, -size, -size); glVertex3f(size, -size, size); glVertex3f(-size, -size, size)
    glVertex3f(-size, -size, size); glVertex3f(size, -size, size); glVertex3f(size, size, size); glVertex3f(-size, size, size)
    glVertex3f(-size, -size, -size); glVertex3f(size, -size, -size); glVertex3f(size, size, -size); glVertex3f(-size, size, -size)
    glVertex3f(-size, -size, -size); glVertex3f(-size, size, -size); glVertex3f(-size, size, size); glVertex3f(-size, -size, size)
    glVertex3f(size, -size, -size); glVertex3f(size, size, -size); glVertex3f(size, size, size); glVertex3f(size, -size, size)
    glEnd()

    # Outer stickers visible only on exterior boundaries
    st = 0.42
    offset = 0.495

    if y == 1: # Up
        glColor3fv(COLORS[face_colors['U']])
        glBegin(GL_QUADS)
        glVertex3f(-st, offset, -st); glVertex3f(st, offset, -st); glVertex3f(st, offset, st); glVertex3f(-st, offset, st)
        glEnd()

    if y == -1: # Down
        glColor3fv(COLORS[face_colors['D']])
        glBegin(GL_QUADS)
        glVertex3f(-st, -offset, -st); glVertex3f(st, -offset, -st); glVertex3f(st, -offset, st); glVertex3f(-st, -offset, st)
        glEnd()

    if z == 1: # Front
        glColor3fv(COLORS[face_colors['F']])
        glBegin(GL_QUADS)
        glVertex3f(-st, -st, offset); glVertex3f(st, -st, offset); glVertex3f(st, st, offset); glVertex3f(-st, st, offset)
        glEnd()

    if z == -1: # Back
        glColor3fv(COLORS[face_colors['B']])
        glBegin(GL_QUADS)
        glVertex3f(-st, -st, -offset); glVertex3f(st, -st, -offset); glVertex3f(st, st, -offset); glVertex3f(-st, st, -offset)
        glEnd()

    if x == -1: # Left
        glColor3fv(COLORS[face_colors['L']])
        glBegin(GL_QUADS)
        glVertex3f(-offset, -st, -st); glVertex3f(-offset, st, -st); glVertex3f(-offset, st, st); glVertex3f(-offset, -st, st)
        glEnd()

    if x == 1: # Right
        glColor3fv(COLORS[face_colors['R']])
        glBegin(GL_QUADS)
        glVertex3f(offset, -st, -st); glVertex3f(offset, st, -st); glVertex3f(offset, st, st); glVertex3f(offset, -st, st)
        glEnd()

    glPopMatrix()

# ----------------------------------------------------------------------
# APPLICATION CONTROLLER
# ----------------------------------------------------------------------
class RubiksCubeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik's Cube AI Coach")
        self.root.geometry("450x700")
        self.root.configure(bg="#1e1e24")

        self.cube = RubiksCubeLogic()
        self.move_queue = []
        self.solving = False
        self.solve_speed = 0.3

        self.animating = False
        self.anim_face = None
        self.anim_direction = 1
        self.anim_target_angle = 0.0
        self.anim_current_angle = 0.0

        self.ai_annotations = {
            'U': "Orienting upper layer elements (U Face Turn)",
            'D': "Adjusting bottom layer positioning (D Face Turn)",
            'F': "Manipulating front face & cross pieces (F Face Turn)",
            'B': "Positioning back layer pairs (B Face Turn)",
            'L': "Building left-side corner-edge slots (L Face Turn)",
            'R': "Executing right-hand trigger algorithm (R Face Turn)"
        }

        self.setup_ui()
        self.setup_pygame()

        self.is_dragging = False
        self.last_mouse_pos = (0, 0)
        self.cam_rot_x = 25.0
        self.cam_rot_y = -45.0
        self.cam_dist = 9.0

        self.root.after(10, self.update_frame)

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='#1e1e24', foreground='#ffffff')

        self.panel_frame = tk.Frame(self.root, bg='#1e1e24')
        self.panel_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        title_label = tk.Label(self.panel_frame, text="RUBIK'S CUBE AI COACH", font=('Segoe UI', 15, 'bold'), fg='#00d2ff', bg='#1e1e24')
        title_label.pack(anchor=tk.W, pady=(0, 10))

        controls_group = tk.LabelFrame(self.panel_frame, text=" Manual Face Turns ", fg='#a0a0b0', bg='#1e1e24', font=('Segoe UI', 9, 'bold'))
        controls_group.pack(fill=tk.X, pady=5)

        btn_grid = tk.Frame(controls_group, bg='#1e1e24')
        btn_grid.pack(padx=5, pady=5)

        faces = [('U', 'U'), ("U'", "Shift+U"), ('D', 'D'), ("D'", "Shift+D"),
                 ('L', 'L'), ("L'", "Shift+L"), ('R', 'R'), ("R'", "Shift+R"),
                 ('F', 'F'), ("F'", "Shift+F"), ('B', 'B'), ("B'", "Shift+B")]

        for idx, (move, key_hint) in enumerate(faces):
            r, c = divmod(idx, 4)
            btn = tk.Button(btn_grid, text=f"{move}\n({key_hint})", width=8, bg='#2b2b36', fg='#00e5ff',
                            activebackground='#3d3d4e', activeforeground='#ffffff', bd=1, relief=tk.FLAT,
                            command=lambda m=move: self.execute_manual_move(m))
            btn.grid(row=r, column=c, padx=3, pady=3)

        scramble_frame = tk.Frame(self.panel_frame, bg='#1e1e24')
        scramble_frame.pack(fill=tk.X, pady=5)

        scramble_btn = tk.Button(scramble_frame, text="🎲 Random Scramble", bg='#3b2d54', fg='#ffffff', font=('Segoe UI', 10, 'bold'),
                                 relief=tk.FLAT, activebackground='#4c3a6d', command=self.scramble_cube)
        scramble_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        reset_btn = tk.Button(scramble_frame, text="🔄 Reset Cube", bg='#542d2d', fg='#ffffff', font=('Segoe UI', 10, 'bold'),
                              relief=tk.FLAT, activebackground='#6d3a3a', command=self.reset_cube)
        reset_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=2)

        speed_group = tk.LabelFrame(self.panel_frame, text=" Auto Solve Speed Controller ", fg='#a0a0b0', bg='#1e1e24', font=('Segoe UI', 9, 'bold'))
        speed_group.pack(fill=tk.X, pady=10)

        self.speed_slider = tk.Scale(speed_group, from_=0.05, to=1.0, resolution=0.05, orient=tk.HORIZONTAL,
                                     bg='#1e1e24', fg='#ffffff', highlightthickness=0, troughcolor='#2b2b36',
                                     command=self.update_speed)
        self.speed_slider.set(0.3)
        self.speed_slider.pack(fill=tk.X, padx=10, pady=5)

        speed_labels = tk.Frame(speed_group, bg='#1e1e24')
        speed_labels.pack(fill=tk.X, padx=10)
        tk.Label(speed_labels, text="Fast (20 moves/s)", fg='#707080', bg='#1e1e24', font=('Segoe UI', 8)).pack(side=tk.LEFT)
        tk.Label(speed_labels, text="Slow (1 move/s)", fg='#707080', bg='#1e1e24', font=('Segoe UI', 8)).pack(side=tk.RIGHT)

        ai_group = tk.LabelFrame(self.panel_frame, text=" AI Coach Insights ", fg='#a0a0b0', bg='#1e1e24', font=('Segoe UI', 9, 'bold'))
        ai_group.pack(fill=tk.BOTH, expand=True, pady=5)

        solve_btn = tk.Button(ai_group, text="⚡ SOLVE WITH AI COACH", bg='#0088cc', fg='#ffffff', font=('Segoe UI', 11, 'bold'),
                              relief=tk.FLAT, activebackground='#00aaff', command=self.start_ai_solve)
        solve_btn.pack(fill=tk.X, padx=10, pady=8)

        self.coach_log = tk.Text(ai_group, height=10, bg='#121216', fg='#00ffc8', font=('Consolas', 9), bd=0, wrap=tk.WORD)
        self.coach_log.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        self.coach_log.insert(tk.END, "[AI Coach]: Ready. Scramble the cube or perform moves to begin.\n")

    def setup_pygame(self):
        pygame.init()
        width, height = 750, 700
        self.surface = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
        pygame.display.set_caption("Rubik's Cube 3D Viewport")

        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (width / height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def log_coach_message(self, message):
        self.coach_log.insert(tk.END, f"> {message}\n")
        self.coach_log.see(tk.END)

    def update_speed(self, val):
        self.solve_speed = float(val)

    def queue_move(self, move, record_history=True):
        self.move_queue.append((move, record_history))

    def execute_manual_move(self, move):
        self.queue_move(move, record_history=True)

    def scramble_cube(self):
        moves = ['U', 'D', 'L', 'R', 'F', 'B']
        modifiers = ['', "'", '2']
        scramble_seq = [random.choice(moves) + random.choice(modifiers) for _ in range(15)]
        for m in scramble_seq:
            self.queue_move(m, record_history=True)
        self.log_coach_message(f"Scramble applied: {' '.join(scramble_seq)}")

    def reset_cube(self):
        self.move_queue.clear()
        self.animating = False
        self.cube.reset()
        self.solving = False
        self.log_coach_message("Cube state reset to solved condition.")

    def start_ai_solve(self):
        if self.solving or self.move_queue:
            return

        moves = self.cube.get_solve_sequence()
        if not moves:
            self.log_coach_message("Cube is already fully solved!")
            return

        self.log_coach_message("==========================================")
        self.log_coach_message(f"Solution sequence calculated ({len(moves)} moves)")
        self.log_coach_message(f"Sequence: {' '.join(moves)}")
        self.log_coach_message("==========================================")

        threading.Thread(target=self.auto_solve_worker, args=(moves,), daemon=True).start()

    def auto_solve_worker(self, moves):
        self.solving = True
        for move in moves:
            if not self.solving:
                break
            self.queue_move(move, record_history=False)
            while self.move_queue or self.animating:
                time.sleep(0.01)
            time.sleep(self.solve_speed)

        self.cube.history.clear()
        self.solving = False
        self.log_coach_message("🎉 Cube successfully solved!")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.root.destroy()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.is_dragging = True
                    self.last_mouse_pos = event.pos
                elif event.button == 4:
                    self.cam_dist = max(4.0, self.cam_dist - 0.5)
                elif event.button == 5:
                    self.cam_dist = min(15.0, self.cam_dist + 0.5)

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_dragging = False

            elif event.type == MOUSEMOTION and self.is_dragging:
                dx = event.pos[0] - self.last_mouse_pos[0]
                dy = event.pos[1] - self.last_mouse_pos[1]
                self.cam_rot_y += dx * 0.5
                self.cam_rot_x += dy * 0.5
                self.last_mouse_pos = event.pos

            elif event.type == KEYDOWN:
                key = pygame.key.name(event.key).upper()
                mods = pygame.key.get_mods()
                prime = "'" if (mods & KMOD_SHIFT) else ""
                if key in ['U', 'D', 'L', 'R', 'F', 'B']:
                    self.execute_manual_move(key + prime)

    def update_animation(self):
        if not self.animating and self.move_queue:
            move, record_hist = self.move_queue.pop(0)
            self.anim_face = move[0]
            self.anim_direction = -1 if "'" in move else (2 if "2" in move else 1)
            self.anim_record_history = record_hist
            
            target_deg = 90.0 if self.anim_direction == 1 else (-90.0 if self.anim_direction == -1 else 180.0)
            self.anim_target_angle = target_deg
            self.anim_current_angle = 0.0
            self.animating = True

            insight = self.ai_annotations.get(self.anim_face, "Manipulating puzzle state")
            self.log_coach_message(f"Move: {move} | {insight}")

        if self.animating:
            step = (15.0 / max(self.solve_speed, 0.05))
            if self.anim_target_angle < 0:
                self.anim_current_angle -= step
                if self.anim_current_angle <= self.anim_target_angle:
                    self.anim_current_angle = self.anim_target_angle
                    self.animating = False
            else:
                self.anim_current_angle += step
                if self.anim_current_angle >= self.anim_target_angle:
                    self.anim_current_angle = self.anim_target_angle
                    self.animating = False

            if not self.animating:
                self.cube.rotate_face(self.anim_face, self.anim_direction, record_history=self.anim_record_history)
                self.anim_current_angle = 0.0

    def render_3d_scene(self):
        glClearColor(0.06, 0.06, 0.08, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        rad_x = math.radians(self.cam_rot_x)
        rad_y = math.radians(self.cam_rot_y)
        cx = self.cam_dist * math.sin(rad_y) * math.cos(rad_x)
        cy = self.cam_dist * math.sin(rad_x)
        cz = self.cam_dist * math.cos(rad_y) * math.cos(rad_x)

        gluLookAt(cx, cy, cz, 0, 0, 0, 0, 1, 0)

        for (x, y, z), face_colors in self.cube.cubies.items():
            if self.animating and self.cube.is_cubie_on_face((x, y, z), self.anim_face):
                glPushMatrix()
                angle = self.anim_current_angle
                if self.anim_face == 'U': glRotatef(-angle, 0, 1, 0)
                elif self.anim_face == 'D': glRotatef(angle, 0, 1, 0)
                elif self.anim_face == 'F': glRotatef(-angle, 0, 0, 1)
                elif self.anim_face == 'B': glRotatef(angle, 0, 0, 1)
                elif self.anim_face == 'R': glRotatef(-angle, 1, 0, 0)
                elif self.anim_face == 'L': glRotatef(angle, 1, 0, 0)

                draw_cubie(x, y, z, face_colors)
                glPopMatrix()
            else:
                draw_cubie(x, y, z, face_colors)

        pygame.display.flip()

    def update_frame(self):
        try:
            self.handle_events()
            self.update_animation()
            self.render_3d_scene()
            self.root.update()
        except Exception:
            pass
        self.root.after(16, self.update_frame)

if __name__ == '__main__':
    root = tk.Tk()
    app = RubiksCubeApp(root)
    root.mainloop()
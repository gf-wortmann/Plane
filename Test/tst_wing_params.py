import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from scipy.interpolate import interp1d
import json
import csv
from pathlib import Path


class Wing:
    def __init__(self, le_x, le_z, te_x, te_z, name="Wing", n_points=200):
        self.name = name
        self.n_points = n_points
        self.source_file = None

        self.le_x_raw = np.asarray(le_x)
        self.le_z_raw = np.asarray(le_z)
        self.te_x_raw = np.asarray(te_x)
        self.te_z_raw = np.asarray(te_z)

        if not (len(self.le_x_raw) == len(self.le_z_raw) ==
                len(self.te_x_raw) == len(self.te_z_raw)):
            raise ValueError("Все массивы должны иметь одинаковую длину")

        self._sort_points()
        self._interpolate()
        self._validate()
        self._calculate_parameters()

    def _sort_points(self):
        idx = np.argsort(self.le_z_raw)
        self.le_z = self.le_z_raw[idx]
        self.le_x = self.le_x_raw[idx]

        te_idx = np.argsort(self.te_z_raw)
        self.te_z = self.te_z_raw[te_idx]
        self.te_x = self.te_x_raw[te_idx]

        if not np.allclose(self.le_z, self.te_z):
            f_te_x = interp1d(self.te_z, self.te_x,
                              kind='linear', fill_value='extrapolate')
            self.te_x = f_te_x(self.le_z)
            self.te_z = self.le_z.copy()

    def _interpolate(self):
        self.z_interp = np.linspace(self.le_z[0], self.le_z[-1], self.n_points)

        f_le_x = interp1d(self.le_z, self.le_x,
                          kind='cubic', fill_value='extrapolate')
        self.le_x_interp = f_le_x(self.z_interp)

        f_te_x = interp1d(self.te_z, self.te_x,
                          kind='cubic', fill_value='extrapolate')
        self.te_x_interp = f_te_x(self.z_interp)

        self.chord_interp = self.te_x_interp - self.le_x_interp

        if np.any(self.chord_interp <= 0):
            raise ValueError("Обнаружены отрицательные хорды!")

    def _validate(self):
        if np.any(self.chord_interp <= 0):
            raise ValueError("Хорда должна быть положительной во всех сечениях")
        if len(self.le_x) < 2:
            raise ValueError("Должно быть минимум 2 точки")

    def _calculate_parameters(self):
        self.area = simpson(self.chord_interp, self.z_interp)
        self.span = self.z_interp[-1] - self.z_interp[0]
        self.aspect_ratio = self.span ** 2 / self.area if self.area > 0 else 0

        int_c2 = simpson(self.chord_interp ** 2, self.z_interp)
        self.mac = int_c2 / self.area if self.area > 0 else 0

        int_c_z = simpson(self.chord_interp * self.z_interp, self.z_interp)
        self.z_mac = int_c_z / self.area if self.area > 0 else 0

        int_xle_c = simpson(self.le_x_interp * self.chord_interp, self.z_interp)
        self.x_mac = int_xle_c / self.area if self.area > 0 else 0

        self.x_quarter_mac = self.x_mac + 0.25 * self.mac

        self.chord_root = self.chord_interp[0]
        self.chord_tip = self.chord_interp[-1]
        self.taper_ratio = self.chord_tip / self.chord_root if self.chord_root > 0 else 0

        if self.span > 0:
            self.sweep_angle = np.arctan2(
                self.le_x_interp[-1] - self.le_x_interp[0],
                self.z_interp[-1] - self.z_interp[0]
            ) * 180 / np.pi
        else:
            self.sweep_angle = 0

    @classmethod
    def from_csv(cls, filepath, name=None, n_points=200,
                 z_col='z', le_x_col='le_x', te_x_col='te_x',
                 delimiter=',', encoding='utf-8'):
        filepath = Path(filepath)
        if name is None:
            name = filepath.stem

        data = []
        with open(filepath, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                data.append(row)

        if not data:
            raise ValueError(f"Файл {filepath} пуст")

        try:
            z = np.array([float(row[z_col]) for row in data])
            le_x = np.array([float(row[le_x_col]) for row in data])
            te_x = np.array([float(row[te_x_col]) for row in data])
        except KeyError as e:
            available = list(data[0].keys())
            raise KeyError(f"Колонка {e} не найдена. Доступны: {available}")

        wing = cls(le_x, z, te_x, z, name=name, n_points=n_points)
        wing.source_file = str(filepath)
        return wing

    @classmethod
    def from_json(cls, filepath, name=None, n_points=200, encoding='utf-8'):
        filepath = Path(filepath)
        if name is None:
            name = filepath.stem

        with open(filepath, 'r', encoding=encoding) as f:
            data = json.load(f)

        if isinstance(data, dict):
            try:
                le_x = np.array(data['le_x'])
                le_z = np.array(data['le_z'])
                te_x = np.array(data['te_x'])
                te_z = np.array(data['te_z'])
            except KeyError as e:
                raise KeyError(f"В JSON отсутствует ключ {e}")
        elif isinstance(data, list):
            if not data:
                raise ValueError("JSON массив пуст")
            try:
                z = np.array([item['z'] for item in data])
                le_x = np.array([item['le_x'] for item in data])
                te_x = np.array([item['te_x'] for item in data])
                if 'te_z' in data[0]:
                    te_z = np.array([item['te_z'] for item in data])
                else:
                    te_z = z.copy()
            except KeyError as e:
                available = list(data[0].keys())
                raise KeyError(f"Ключ {e} не найден. Доступны: {available}")
        else:
            raise TypeError(f"Неизвестный формат JSON")

        wing = cls(le_x, le_z, te_x, te_z, name=name, n_points=n_points)
        wing.source_file = str(filepath)
        return wing

    @classmethod
    def from_naca(cls, naca_number, chord=1.0, span=10.0,
                  num_points=100, name=None, n_points=200):
        if name is None:
            name = f"NACA {naca_number}"

        naca_str = str(naca_number).zfill(4)
        m = int(naca_str[0]) / 100.0
        p = int(naca_str[1]) / 10.0
        t = int(naca_str[2:4]) / 100.0

        beta = np.linspace(0, np.pi, num_points)
        x = (1 - np.cos(beta)) / 2

        yt = (t / 0.2) * (0.2969 * np.sqrt(x) - 0.1260 * x -
                          0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4)

        yc = np.zeros_like(x)
        if m > 0 and p > 0:
            mask1 = x <= p
            yc[mask1] = (m / p ** 2) * (2 * p * x[mask1] - x[mask1] ** 2)
            mask2 = x > p
            yc[mask2] = (m / (1 - p) ** 2) * ((1 - 2 * p) + 2 * p * x[mask2] - x[mask2] ** 2)

        z_coords = np.linspace(0, span, 10)
        le_x = np.zeros_like(z_coords)
        le_z = z_coords.copy()
        te_x = np.full_like(z_coords, chord)
        te_z = z_coords.copy()

        wing = cls(le_x, le_z, te_x, te_z, name=name, n_points=n_points)
        wing.source_file = f"NACA {naca_number} (сгенерирован)"
        return wing

    def calculate_mac(self):
        return {
            'mac': self.mac,
            'x_mac': self.x_mac,
            'z_mac': self.z_mac,
            'x_quarter': self.x_quarter_mac,
            'area': self.area,
            'span': self.span,
            'aspect_ratio': self.aspect_ratio,
            'taper_ratio': self.taper_ratio,
            'sweep_angle': self.sweep_angle,
            'chord_root': self.chord_root,
            'chord_tip': self.chord_tip
        }

    def get_chord_distribution(self):
        return self.z_interp.copy(), self.chord_interp.copy()

    def get_section(self, z_coord):
        idx = np.argmin(np.abs(self.z_interp - z_coord))
        return {
            'z': self.z_interp[idx],
            'le_x': self.le_x_interp[idx],
            'te_x': self.te_x_interp[idx],
            'chord': self.chord_interp[idx]
        }

    def plot_planform(self, show_mac=True, show_sections=True,
                      n_sections=10, figsize=(12, 8), save_path=None):
        fig, ax = plt.subplots(figsize=figsize)

        # Определяем, нужно ли отражать крыло
        z_min, z_max = self.z_interp[0], self.z_interp[-1]
        is_half = (z_min >= 0) and (z_max > 0)

        # Функция для отрисовки крыла
        def draw_wing(z_coords, le_x, te_x, alpha=1.0, flip=False):
            if flip:
                z_coords = -z_coords[::-1]
                le_x = le_x[::-1]
                te_x = te_x[::-1]
            else:
                z_coords = z_coords.copy()
                le_x = le_x.copy()
                te_x = te_x.copy()

            # Контур крыла
            x_contour = list(le_x)
            z_contour = list(z_coords)
            x_contour.extend(list(te_x[::-1]))
            z_contour.extend(list(z_coords[::-1]))
            x_contour.append(le_x[0])
            z_contour.append(z_coords[0])

            ax.fill(x_contour, z_contour, alpha=0.3 * alpha,
                    color='lightblue', edgecolor='blue', linewidth=2)
            ax.plot(le_x, z_coords, 'b-', linewidth=2, alpha=alpha,
                    label='Передняя кромка' if not flip else None)
            ax.plot(te_x, z_coords, 'r-', linewidth=2, alpha=alpha,
                    label='Задняя кромка' if not flip else None)

        # Рисуем основное крыло
        draw_wing(self.z_interp, self.le_x_interp, self.te_x_interp)

        # Если задана половина крыла, рисуем зеркальное отражение
        if is_half:
            draw_wing(self.z_interp, self.le_x_interp, self.te_x_interp,
                      alpha=0.5, flip=True)
            ax.axhline(y=0, color='black', linestyle='--', alpha=0.7,
                       label='Ось симметрии', linewidth=1.5)

        # Рисуем хорды в сечениях
        if show_sections:
            section_z = np.linspace(self.z_interp[0], self.z_interp[-1], n_sections)
            for z_sec in section_z:
                idx = np.argmin(np.abs(self.z_interp - z_sec))
                ax.plot([self.le_x_interp[idx], self.te_x_interp[idx]],
                        [self.z_interp[idx], self.z_interp[idx]],
                        'gray', linewidth=0.5, alpha=0.5)
                if is_half:
                    ax.plot([self.le_x_interp[idx], self.te_x_interp[idx]],
                            [-self.z_interp[idx], -self.z_interp[idx]],
                            'gray', linewidth=0.5, alpha=0.3)

        # Рисуем САХ
        if show_mac and self.mac > 0:
            if is_half:
                # Для половины крыла показываем САХ на обеих половинах
                for sign in [1, -1]:
                    ax.plot([self.x_mac, self.x_mac + self.mac],
                            [sign * self.z_mac, sign * self.z_mac],
                            'g-', linewidth=3, alpha=0.8 if sign == 1 else 0.4)
                    ax.plot(self.x_mac, sign * self.z_mac, 'go', markersize=8)
                    ax.plot(self.x_quarter_mac, sign * self.z_mac, 'g*', markersize=12)
            else:
                ax.plot([self.x_mac, self.x_mac + self.mac],
                        [self.z_mac, self.z_mac],
                        'g-', linewidth=3, label='САХ')
                ax.plot(self.x_mac, self.z_mac, 'go', markersize=8)
                ax.plot(self.x_quarter_mac, self.z_mac, 'g*', markersize=12,
                        label='Четверть хорды САХ')

        ax.set_xlabel('X (м) - вдоль хорды', fontsize=12)
        ax.set_ylabel('Z (м) - вдоль размаха', fontsize=12)
        ax.set_title(f'Форма крыла в плане: {self.name}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best')
        ax.axis('equal')

        info_text = (
            f"Площадь: {self.area:.3f} м²\n"
            f"Размах: {self.span:.3f} м\n"
            f"Удлинение: {self.aspect_ratio:.3f}\n"
            f"САХ: {self.mac:.3f} м\n"
            f"Корневая хорда: {self.chord_root:.3f} м\n"
            f"Концевая хорда: {self.chord_tip:.3f} м\n"
            f"Сужение: {self.taper_ratio:.3f}\n"
            f"Стреловидность: {self.sweep_angle:.1f}°"
        )

        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.5',
                          facecolor='white', alpha=0.8))

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig, ax

    def plot_chord_distribution(self, figsize=(10, 6), save_path=None):
        fig, ax = plt.subplots(figsize=figsize)

        # Определяем, нужно ли отражать
        is_half = (self.z_interp[0] >= 0) and (self.z_interp[-1] > 0)

        if is_half:
            # Для половины крыла показываем полную симметричную картину
            z_full = np.concatenate([-self.z_interp[::-1], self.z_interp])
            chord_full = np.concatenate([self.chord_interp[::-1], self.chord_interp])
            ax.plot(z_full, chord_full, 'b-', linewidth=2)
            ax.fill_between(z_full, 0, chord_full, alpha=0.3)
        else:
            ax.plot(self.z_interp, self.chord_interp, 'b-', linewidth=2)
            ax.fill_between(self.z_interp, 0, self.chord_interp, alpha=0.3)

        ax.axhline(y=self.mac, color='red', linestyle='--',
                   label=f'САХ = {self.mac:.3f} м')
        ax.axvline(x=self.z_mac, color='green', linestyle='--',
                   label=f'Z САХ = {self.z_mac:.3f} м')
        if is_half:
            ax.axvline(x=-self.z_mac, color='green', linestyle='--', alpha=0.5)

        ax.set_xlabel('Z (м) - вдоль размаха', fontsize=12)
        ax.set_ylabel('Хорда (м)', fontsize=12)
        ax.set_title(f'Распределение хорды по размаху: {self.name}',
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig, ax

    def save_to_csv(self, filepath, z_col='z', le_x_col='le_x',
                    te_x_col='te_x', delimiter=',', encoding='utf-8'):
        filepath = Path(filepath)
        with open(filepath, 'w', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=[z_col, le_x_col, te_x_col],
                                    delimiter=delimiter)
            writer.writeheader()
            for z, le_x, te_x in zip(self.le_z, self.le_x, self.te_x):
                writer.writerow({z_col: z, le_x_col: le_x, te_x_col: te_x})
        print(f"✅ Данные сохранены в: {filepath}")

    def save_to_json(self, filepath, include_params=True, encoding='utf-8'):
        filepath = Path(filepath)
        data = {
            'name': self.name,
            'le_x': self.le_x.tolist(),
            'le_z': self.le_z.tolist(),
            'te_x': self.te_x.tolist(),
            'te_z': self.te_z.tolist(),
        }
        if include_params:
            params = self.calculate_mac()
            data['parameters'] = params

        with open(filepath, 'w', encoding=encoding) as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Данные сохранены в: {filepath}")

    def __str__(self):
        source_info = f"\n  Источник: {self.source_file}" if self.source_file else ""
        return (
            f"Крыло: {self.name}{source_info}\n"
            f"  Площадь: {self.area:.3f} м²\n"
            f"  Размах: {self.span:.3f} м\n"
            f"  Удлинение: {self.aspect_ratio:.3f}\n"
            f"  САХ: {self.mac:.3f} м\n"
            f"  X носка САХ: {self.x_mac:.3f} м\n"
            f"  Z САХ: {self.z_mac:.3f} м\n"
            f"  X четверти хорды: {self.x_quarter_mac:.3f} м\n"
            f"  Корневая хорда: {self.chord_root:.3f} м\n"
            f"  Концевая хорда: {self.chord_tip:.3f} м\n"
            f"  Сужение: {self.taper_ratio:.3f}\n"
            f"  Стреловидность: {self.sweep_angle:.1f}°"
        )


# ============ ПРИМЕР ИСПОЛЬЗОВАНИЯ ============
if __name__ == "__main__":
    # Создание тестового крыла
    # z = np.array([0, 2, 4, 6, 8, 10])
    # le_x = 0.3 * z
    # te_x = le_x + np.linspace(3.0, 1.0, len(z))

    # wing = Wing(le_x, z, te_x, z, name="Тестовое крыло")
    wing = Wing.from_json("tst_elliptic_planform.json")
    print(wing)
    wing.extra

    # Визуализация
    wing.plot_planform(show_mac=True, show_sections=True)
    wing.plot_chord_distribution()
    plt.show()
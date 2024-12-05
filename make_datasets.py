
import os
import matplotlib.pyplot as plt
from matplotlib.table import Table
import random
import itertools
import csv
from matplotlib.colors import LinearSegmentedColormap


def adjust_color_lightness(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

def generate_cycled_colormap(num_courses, base_cmap='tab20'):
    colors = plt.get_cmap(base_cmap).colors
    adjusted_colors = []
    factor = 0.5  # Start with half lightness and increase
    increment = 0.5 / (num_courses // len(colors) + 1)  # Adjust increment based on overflow
    for i in range(num_courses):
        if i % len(colors) == 0 and i > 0:  # Each cycle through base colors
            factor += increment
        new_color = adjust_color_lightness(colors[i % len(colors)], factor)
        adjusted_colors.append(new_color)
    return adjusted_colors

# Function to generate random time slots between 9 AM to 10 PM at 30-minute intervals
def generate_time_slots(start_hour=9, end_hour=22, interval_minutes=30):
    return [f"{h:02d}:{m:02d}" for h in range(start_hour, end_hour + 1) for m in range(0, 60, interval_minutes)]

# Function to generate a timetable as a PNG image
def generate_timetable_image(filename, courses, days, time_slots, buildings, num_images=5, max_courses_per_image=4):
    with open(f'./test_datasets/{filename}_ground_truth.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Image', 'Course', 'Day', 'Start Time', 'End Time', 'Room'])
        num_courses = len(korean_courses)
        course_colors = generate_cycled_colormap(num_courses)
        course_to_color = {course: course_colors[i] for i, course in enumerate(korean_courses)}
        for img_num in range(num_images):
            course_to_room = {course: f"{random.choice(buildings)}{random.randint(101, 505)}" for course in courses}
            fig, ax = plt.subplots(figsize=(8, 12))
            ax.set_title('시간표', fontsize=16)
            ax.axis('off')
            table = Table(ax, bbox=[0, 0, 1, 1])

            cell_width = 1.0 / (len(days) + 1)
            cell_height = 1.0 / (len(time_slots) + 1)

            if img_num < 100 or img_num >= 300:
                fig.patch.set_facecolor('black')
                ax.patch.set_facecolor('black')
                text_color = 'white'
                filename = 'timetable_w'
            else:
                text_color = 'black'
                filename = 'timetable_b'

            # Populate headers for the table
            for i, day in enumerate([''] + days):
                cell = table.add_cell(0, i, cell_width, cell_height, text=day, loc='center', facecolor='none', edgecolor='none')
                cell.get_text().set_color(text_color)

            for j, time in enumerate([''] + time_slots):
                cell = table.add_cell(j, 0, cell_width, cell_height, text=time, loc='right', facecolor='none', edgecolor='none')
                cell.get_text().set_color(text_color)

            occupied_cells = set()
            course_count = {course: 0 for course in courses}
            while len(occupied_cells) < len(days) * max_courses_per_image:
                course = random.choice(courses)
                room = course_to_room[course]
                day = random.choice(days)
                duration = random.randint(2, 4)
                start_index = random.randint(0, len(time_slots) - duration)
                end_index = start_index + duration

                if course_count[course] < max_courses_per_image and not any((day, time_slots[index]) in occupied_cells for index in range(start_index, end_index)):
                    course_count[course] += 1
                    for index in range(start_index, end_index):
                        occupied_cells.add((day, time_slots[index]))
                        if index == start_index:
                            course_font_size = 14
                            max_chars = 3
                            wrapped_course = '\n'.join([course[i:i+max_chars] for i in range(0, len(course), max_chars)])
                            cell_text = f"{wrapped_course}\n{room}"
                            cell = table.add_cell(index + 1, days.index(day) + 1, cell_width, cell_height, text=cell_text, loc='center', facecolor=course_to_color[course])
                            cell.get_text().set_fontsize(course_font_size)
                        else:
                            cell = table.add_cell(index + 1, days.index(day) + 1, cell_width, cell_height, loc='center', facecolor=course_to_color[course])
                            cell.get_text().set_text('')
                        cell.get_text().set_color(text_color)
                        cell.set_edgecolor(course_to_color[course])
                        if index == start_index:
                            writer.writerow([f'{filename}_{img_num+1}.png', course, day, time_slots[start_index], time_slots[end_index-1], room])

            ax.add_table(table)
            plt.subplots_adjust(left=0.15, right=0.98, top=0.95, bottom=0.05)
            
            filepath = f'./test_datasets/{filename}_{img_num+1}.png'
            plt.savefig(filepath, dpi=300)
            plt.close()


            print(f"Saved: {filepath}")

# Prepare the required data
os.makedirs('./test_datasets', exist_ok=True)
plt.rcParams['font.family'] = 'Apple SD Gothic Neo'
plt.rcParams['font.size'] = 10

buildings = ['교', '공', '인', '사', '실본', '과', '의', '약', '치', '한']
korean_courses = [
    '데이터과학', '인공지능', '기계학습', '컴퓨터구조', '운영체제',
    '생물학', '화학', '물리학', '고급수학', '지구과학',
    '경제학', '사회학', '심리학', '문학', '역사학',
    '음악', '미술', '체육', '철학', '정치학',
    '언어학', '국제관계', '법학', '실용음악', '도예',
    '건축학', '동양학', '서양학', '문화인류학', '응용수학',
    '생명공학', '환경과학', '해양학', '우주과학', '의학',
    '통계학', '로봇공학', '나노공학', '재료과학', '에너지공학',
    '인문학', '교육학', '외국어', '행정학', '회계학',
    '마케팅', '정보시스템', '경영학', '패션디자인', '산업디자인',
    '그래픽디자인', '영상제작', '애니메이션', '게임디자인', '식품과학',
    '스포츠과학', '실내디자인', '도시계획', '관광학', '호텔경영',
    '영화학', '작곡', '연극', '무용', '미술사',
    '조소', '판화', '서양화', '동양화', '인테리어디자인',
    '사진학', '보건학', '약학', '간호학', '치위생학',
    '물리치료학', '임상병리학', '치의학', '한의학', '수의학'
]
days = ['월', '화', '수', '목', '금']
time_slots = generate_time_slots()
colors = plt.colormaps['tab20']
num_images = 40

generate_timetable_image('timetable', korean_courses, days, time_slots, buildings, num_images=num_images)

print('Timetable images saved in the datasets folder.')

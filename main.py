from lib import *

vertical_num = 10
horizontal_num = 10
csv_file = open("gift.csv", "r", encoding="utf-8")
csv_reader = csv.reader(csv_file)
csv_list = list(csv_reader)
horizontal_num = int(csv_list[0][0])
vertical_num = int(csv_list[0][1])
blindbox_gifts = csv_list[1:]
csv_file.close()

blindbox_list = []
box_list = []
for blindbox_gift in blindbox_gifts:
    for _ in range(int(blindbox_gift[1])):
        blindbox_list.append(BlindBox(blindbox_gift[2].strip(), blindbox_gift[0].strip()))
    item_dict[blindbox_gift[0].strip()] = int(blindbox_gift[1])
log(item_dict)

fullscreen_mode = True
window.init()
if fullscreen_mode:
    info = window.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = window.display.set_mode((WIDTH, HEIGHT), window.FULLSCREEN)
else:
    screen = window.display.set_mode((WIDTH, HEIGHT))
vertical_range = int(HEIGHT // (vertical_num+1))
horizontal_range = int(WIDTH // (horizontal_num+1))
opened_image = window.image.load(opened_box_link).convert_alpha()
opened_image = window.transform.scale(opened_image, (box_width, box_height))
closed_image = window.image.load(closed_box_link).convert_alpha()
closed_image = window.transform.scale(closed_image, (box_width, box_height))

class Box:
    def __init__(self, x, y, opened=False, blindbox=None):
        self.x = x
        self.y = y
        self.opened = opened
        self.blindbox = blindbox
    def open(self):
        self.opened = True
        item_dict[self.blindbox.name] -= 1
        log(item_dict)
        log(self.blindbox.name)
        calculate_chance()
        self.alert()
    def draw(self, screen):
        if self.opened:
            screen.blit(opened_image, (self.x - box_width / 2, self.y - box_height / 2))
        else:
            screen.blit(closed_image, (self.x - box_width / 2, self.y - box_height / 2))
    def alert(self):
        global alert_displayed, alert_text, alert_image, alert_image_height, alert_image_width
        alert_displayed = True
        alert_text = self.blindbox.name
        alert_image = window.image.load(self.blindbox.image).convert_alpha()
        # alert_image = window.transform.scale(alert_image, (200, 200))
        original_width, original_height = alert_image.get_size()
        alert_image_width = int(alert_image_height * original_width / original_height)
        alert_image = window.transform.scale(alert_image, (alert_image_width, alert_image_height))

for z in range(vertical_num):
    for i in range(horizontal_num):
        if len(blindbox_list):
            blindbox = blindbox_list.pop(random.randint(0, len(blindbox_list) - 1))
            box_list.append(Box((i+1) * horizontal_range, (z+1) * vertical_range, False, blindbox))
            box_quantity += 1
            

for box in box_list:
    # print(box.x, box.y, box.opened, box.blindbox.image, box.blindbox.name)
    log(box.blindbox.name)
def calculate_chance():
    total = box_quantity
    for key in item_dict:
        chance_dict[key] = item_dict[key] / total
    log(chance_dict)

window.display.set_caption("Minigame Blindbox")

running = True
font_bold = window.font.Font("fonts/arialbd.ttf", alert_font_size)
font = window.font.Font("fonts/arial.ttf", font_size)
calculate_chance()
while running:
    screen.fill(PINK)

    for box in box_list:
        if box.blindbox.name == None:
            continue
        box.draw(screen)
    if alert_displayed:
        window.draw.rect(screen, WHITE, ((WIDTH - alert_width)/2, (HEIGHT - alert_height)/2, alert_width, alert_height), border_radius=20)
        text_surface = font_bold.render(alert_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, (HEIGHT - alert_image_height) / 2 - alert_text_upshift))
        screen.blit(text_surface, text_rect)
        screen.blit(alert_image, ((WIDTH-alert_image_width)/2, (HEIGHT-alert_image_height)/2+alert_image_downshift))
        window.draw.circle(screen, RED, ((WIDTH + alert_width) // 2 - 35, (HEIGHT - alert_height) // 2 + 35), 20)
        line_thickness = 3
        circle_center = ((WIDTH + alert_width) // 2 - 35, (HEIGHT - alert_height) // 2 + 35)
        circle_radius = 20
        x1, y1 = circle_center[0] - int(circle_radius * 0.4), circle_center[1] - int(circle_radius * 0.4)
        x2, y2 = circle_center[0] + int(circle_radius * 0.4), circle_center[1] + int(circle_radius * 0.4)
        window.draw.line(screen, WHITE, (x1, y1), (x2, y2), line_thickness)
        window.draw.line(screen, WHITE, (x1, y2), (x2, y1), line_thickness)
    if data_displayed:
        # Draw the data display box
        window.draw.rect(screen, WHITE, ((WIDTH - data_displayed_width) / 2, (HEIGHT - data_displayed_height) / 2, data_displayed_width, data_displayed_height), border_radius=20)

        header_surface = font_bold.render("Vật phẩm còn lại", True, BLACK)
        header_rect = header_surface.get_rect(center=(WIDTH / 2, (HEIGHT - data_displayed_height) / 2 + line_spacing))
        screen.blit(header_surface, header_rect)

        # Draw table rows for item data
        table_start_y = (HEIGHT - data_displayed_height) / 2 + 2 * line_spacing
        row_height = 40
        col1_x = (WIDTH - data_displayed_width) / 2 + left_margin
        col2_x = (WIDTH + data_displayed_width) / 2 - left_margin - 200
        col3_x = (WIDTH + data_displayed_width) / 2 - left_margin

        # Display box quantity as the first row
        box_count_surface = font.render(f"Còn tổng cộng {box_quantity} hộp mù", True, BLACK)
        box_count_rect = box_count_surface.get_rect(topleft=(col1_x, table_start_y))
        screen.blit(box_count_surface, box_count_rect)

        # Display item data in subsequent rows
        for i, key in enumerate(item_dict):
            item_name_surface = font.render(key, True, BLACK)
            item_name_rect = item_name_surface.get_rect(topleft=(col1_x, table_start_y + (i + 1) * row_height))
            screen.blit(item_name_surface, item_name_rect)

            item_count_surface = font.render(str(item_dict[key]), True, BLACK)
            item_count_rect = item_count_surface.get_rect(topright=(col2_x, table_start_y + (i + 1) * row_height))
            screen.blit(item_count_surface, item_count_rect)
            #display chance on col3
            chance_surface = font.render(f"{chance_dict[key]*100:.2f}%", True, BLACK)
            chance_rect = chance_surface.get_rect(topright=(col3_x, table_start_y + (i + 1) * row_height))
            screen.blit(chance_surface, chance_rect)

    mouse_pos = window.mouse.get_pos()
    if mouse_pos[0] < 20 and mouse_pos[1] < 20:
        data_displayed = True
    else:
        data_displayed = False
    mouse_click = window.mouse.get_pressed()
    if mouse_click[0] and not mouse_click_handled:
        if not alert_displayed:
            for box in box_list:
                if not box.opened and box.x - box_width / 2 <= mouse_pos[0] <= box.x + box_width / 2 and box.y - box_height / 2 <= mouse_pos[1] <= box.y + box_height / 2:
                    box.open()
                    box_quantity -= 1
                    log(box_quantity)
        else:
            circle_x, circle_y = circle_center
            if (mouse_pos[0] - circle_x) ** 2 + (mouse_pos[1] - circle_y) ** 2 <= circle_radius ** 2:
                alert_displayed = False
        mouse_click_handled = True
    elif not mouse_click[0]:
        mouse_click_handled = False
    for event in window.event.get():
        if event.type == window.KEYDOWN and event.key == window.K_q and (event.mod & window.KMOD_CTRL) and (event.mod & window.KMOD_SHIFT):
            running = False
    window.display.flip()
window.quit()

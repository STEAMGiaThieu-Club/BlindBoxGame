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

fig_csv_file = open("fig.csv", "r", encoding="utf-8")
fig_csv_reader = csv.reader(fig_csv_file)
fig_csv_list = list(fig_csv_reader)
fig_csv_file.close()

fig_width = 200
fig_height = 200

blindbox_list = []
box_list = []
for blindbox_gift in blindbox_gifts:
    for _ in range(int(blindbox_gift[1])):
        blindbox_list.append(BlindBox(blindbox_gift[2].strip(), blindbox_gift[0].strip()))
    item_dict[blindbox_gift[0].strip()] = int(blindbox_gift[1])
log(item_dict)

# fullscreen_mode = False
fullscreen_mode = True
window.init()
icon_data = base64.b64decode(base64_image)
icon_image = window.image.load(io.BytesIO(icon_data))
window.display.set_icon(icon_image)
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
soldout_image = window.image.load("img/soldout.png").convert_alpha()
original_width, original_height = soldout_image.get_size()
new_width = int(120 * original_width / original_height)
soldout_image = window.transform.scale(soldout_image, (new_width, 120))

# class Window:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.displayed = False
#         self.images = []
#         self.texts = []
#     def add_close_button(self, x, y, height, width):
#         self.close_button = window.draw.circle(screen, RED, (x, y), 20)
#     def add_text(self, displaytext, x, y, height, width, font, color=BLACK):
#         text_surface = font.render(displaytext, True, color)
#         text_rect = text_surface.get_rect(center=(x, y))
#         self.texts.append([text_surface,text_rect])
#     def add_image(self, image, x, y, height, width):
#         self.images.append()

#     # def add_rect(self, x, y, height, width, color):
#     #     self.rect = window.draw.rect(screen, color, (x, y, height, width))
    
#     def display(self):
#         self.displayed = True
#         window.draw.rect(screen, WHITE, ((WIDTH - self.width)/2, (HEIGHT - self.height)/2, self.width, self.height), border_radius=20)
#         for image in self.images:
#             screen.blit(image, (x, y))
#         for text in self.texts:
#             screen.blit(text, (x, y))

fig_link = "img/fig/"
class Fig:
    def __init__(self, x, name, image, price, point_price, amount):
        self.amount = amount
        self.x = x
        self.name = name
        self.image = window.image.load(fig_link + image.strip()).convert_alpha()
        original_width, original_height = self.image.get_size()
        new_width = int(redeem_image_height * original_width / original_height)
        self.image = window.transform.scale(self.image, (new_width, redeem_image_height))
        self.price = price.strip()
        self.point_price = int(point_price)
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

    # def draw(self, screen):
    #     screen.blit(self.image, (self.x, self.y))

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
        original_width, original_height = alert_image.get_size()
        alert_image_width = int(alert_image_height * original_width / original_height)
        alert_image = window.transform.scale(alert_image, (alert_image_width, alert_image_height))

for z in range(vertical_num):
    for i in range(horizontal_num):
        if len(blindbox_list):
            blindbox = blindbox_list.pop(random.randint(0, len(blindbox_list) - 1))
            box_list.append(Box((i+1) * horizontal_range, (z+1) * vertical_range, False, blindbox))
            box_quantity += 1

fig_list = []
for i in range(len(fig_csv_list)):
    fig = Fig(i, fig_csv_list[i][0], fig_csv_list[i][1], fig_csv_list[i][2], fig_csv_list[i][3], fig_csv_list[i][4])
    fig_list.append(fig)
for i in fig_list:
    print(i.name, i.price, i.point_price)

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
normal_font = window.font.Font("fonts/arial.ttf", 30)
small_font = window.font.Font("fonts/arial.ttf", 20)
calculate_chance()
while running:
    screen.fill(PINK)
    window.draw.rect(screen, WHITE, (WIDTH - 150 - 20, 20, 150, 50), border_radius=20)
    #viết point vào center của box
    point_surface = font.render(f"Điểm: {point}", True, BLACK)
    point_rect = point_surface.get_rect(center=(WIDTH - 95, 45))

    screen.blit(point_surface, point_rect)

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

        table_start_y = (HEIGHT - data_displayed_height) / 2 + 2 * line_spacing
        row_height = 40
        col1_x = (WIDTH - data_displayed_width) / 2 + left_margin
        col2_x = (WIDTH + data_displayed_width) / 2 - left_margin - 200
        col3_x = (WIDTH + data_displayed_width) / 2 - left_margin

        box_count_surface = font.render(f"Còn tổng cộng {box_quantity} hộp mù", True, BLACK)
        box_count_rect = box_count_surface.get_rect(topleft=(col1_x, table_start_y))
        screen.blit(box_count_surface, box_count_rect)

        for i, key in enumerate(item_dict):
            item_name_surface = font.render(key, True, BLACK)
            item_name_rect = item_name_surface.get_rect(topleft=(col1_x, table_start_y + (i + 1) * row_height))
            screen.blit(item_name_surface, item_name_rect)

            item_count_surface = font.render(str(item_dict[key]), True, BLACK)
            item_count_rect = item_count_surface.get_rect(topright=(col2_x, table_start_y + (i + 1) * row_height))
            screen.blit(item_count_surface, item_count_rect)
            chance_surface = font.render(f"{chance_dict[key]*100:.2f}%", True, BLACK)
            chance_rect = chance_surface.get_rect(topright=(col3_x, table_start_y + (i + 1) * row_height))
            screen.blit(chance_surface, chance_rect)
    if redeem_displayed:
        # Draw the redeem box 1200x800
        window.draw.rect(screen, WHITE, ((WIDTH - redeem_width) / 2, (HEIGHT - redeem_height) / 2, redeem_width, redeem_height), border_radius=20)
        # Add title "Đổi quà"
        redeem_title_surface = font_bold.render(redeem_text, True, BLACK)
        redeem_title_rect = redeem_title_surface.get_rect(center=(WIDTH / 2, (HEIGHT - redeem_height) / 2 + line_spacing))
        screen.blit(redeem_title_surface, redeem_title_rect)
        # Add "(Giá trị tham khảo trên Shopee)" in the bottom right corner with smaller font
        reference_surface = small_font.render("(Giá trị tham khảo trên Shopee)", True, BLACK)
        reference_rect = reference_surface.get_rect(bottomright=(WIDTH - left_margin, HEIGHT - line_spacing))
        screen.blit(reference_surface, reference_rect)
        # Define the dimensions for each column and row
        column_width = redeem_width // 2
        row_height = (redeem_height - 3 * line_spacing) // 3  # Adjusted for title spacing
        row_offset = 60  # Additional offset for rows

        for i, fig in enumerate(fig_list[:6]):  # Limit to 6 figs for 2 columns and 3 rows
            col = i % 2  # Determine column (0 or 1)
            row = i // 2  # Determine row (0, 1, or 2)

            # Calculate positions
            x = (WIDTH - redeem_width) / 2 + col * column_width
            y = (HEIGHT - redeem_height) / 2 + row * row_height + line_spacing + row_offset  # Shifted down for title and offset

            # Update fig boundaries for click detection
            fig.x1 = x + 40
            fig.y1 = y
            fig.x2 = x + column_width - 40
            fig.y2 = y + row_height

            # Check if mouse is hovering over the current item
            mouse_pos = window.mouse.get_pos()
            is_hovered = fig.x1 <= mouse_pos[0] <= fig.x2 and fig.y1 <= mouse_pos[1] <= fig.y2

            # Draw border if hovered
            if is_hovered:
                window.draw.rect(screen, BLACK, (fig.x1, fig.y1, fig.x2 - fig.x1, fig.y2 - fig.y1), width=3, border_radius=10)

            # Draw the image on the left
            screen.blit(fig.image, (x + left_margin, y + (row_height - redeem_image_height) // 2))

            # Draw the text on the right, aligned to the right edge of the column
            text_x = x + column_width - left_margin
            name_surface = normal_font.render(fig.name, True, BLACK)
            name_rect = name_surface.get_rect(topright=(text_x, y + line_spacing))
            screen.blit(name_surface, name_rect)

            price_surface = normal_font.render(f"Giá trị: {fig.price}", True, BLACK)
            price_rect = price_surface.get_rect(topright=(text_x, y + line_spacing * 2))
            screen.blit(price_surface, price_rect)

            point_price_surface = normal_font.render(f"Điểm quy đổi: {fig.point_price}", True, BLACK)
            point_price_rect = point_price_surface.get_rect(topright=(text_x, y + line_spacing * 3))
            screen.blit(point_price_surface, point_price_rect)

            # If amount < 1, draw the soldout image in the center of the row
            if int(fig.amount) < 1:
                soldout_x = x + (column_width - soldout_image.get_width() - redeem_image_height // 2) // 2
                soldout_y = y + (row_height - soldout_image.get_height()) // 2
                screen.blit(soldout_image, (soldout_x, soldout_y))
    if submit_displayed:
        window.draw.rect(screen, WHITE, ((WIDTH - submit_width) / 2, (HEIGHT - submit_height) / 2, submit_width, submit_height), border_radius=20)
        submit_surface = font_bold.render(submit_text, True, BLACK)
        submit_rect = submit_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2-200))
        screen.blit(submit_surface, submit_rect)
        # hiện ảnh ở center
        screen.blit(submit_image, ((WIDTH - fig_width) / 2, (HEIGHT - fig_height) / 2))
        # hiện nút xác nhận và hủy cân đều 2 bên dưới ảnh
        button_width = 200
        button_height = 100
        button_spacing = 50  # khoảng cách giữa 2 nút
        button_y = HEIGHT / 2 + fig_height / 2 + 50  # vị trí y dưới ảnh

        # nút xác nhận bên phải
        confirm_x = WIDTH / 2 + button_spacing / 2
        confirm_hovered = confirm_x <= mouse_pos[0] <= confirm_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height
        if point >= submit_price:
            confirm_color = DARK_GREEN if confirm_hovered else GREEN
        else:
            confirm_color = GRAY
        window.draw.rect(screen, confirm_color, (confirm_x, button_y, button_width, button_height), border_radius=20)
        confirm_surface = font.render("Xác nhận", True, WHITE)
        confirm_rect = confirm_surface.get_rect(center=(confirm_x + button_width / 2, button_y + button_height / 2))
        screen.blit(confirm_surface, confirm_rect)

        # nút hủy bên trái
        cancel_x = WIDTH / 2 - button_width - button_spacing / 2
        cancel_hovered = cancel_x <= mouse_pos[0] <= cancel_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height
        cancel_color = DARK_RED if cancel_hovered else RED
        window.draw.rect(screen, cancel_color, (cancel_x, button_y, button_width, button_height), border_radius=20)
        cancel_surface = font.render("Hủy", True, WHITE)
        cancel_rect = cancel_surface.get_rect(center=(cancel_x + button_width / 2, button_y + button_height / 2))
        screen.blit(cancel_surface, cancel_rect)

    mouse_pos = window.mouse.get_pos()
    if mouse_pos[0] < 20 and mouse_pos[1] < 20:
        data_displayed = True
    else:
        data_displayed = False
    mouse_click = window.mouse.get_pressed()
    if mouse_click[0] and not mouse_click_handled:
        if redeem_displayed:
            if submit_displayed:
                if confirm_hovered:
                    if point >= submit_price:
                        point -= submit_price
                        for fig_item in fig_list:
                            if fig_item.name == submit_name:
                                fig_item.amount = str(int(fig_item.amount) - 1)
                                print(f"Đổi quà thành công: {submit_name}")
                                break
                        submit_displayed = False
                    else:
                        print("Không đủ điểm")
                elif cancel_hovered:
                    submit_displayed = False
            else:
                for fig in fig_list:
                    if fig.x1 <= mouse_pos[0] <= fig.x2 and fig.y1 <= mouse_pos[1] <= fig.y2:
                        if int(fig.amount) < 1:
                            print("Hết hàng")
                        else:
                            submit_displayed = True
                            submit_text = f"Xác nhận đổi {fig.point_price} điểm lấy {fig.name}?"
                            submit_name = fig.name
                            submit_image = fig.image
                            submit_price = fig.point_price
        else:
            if not alert_displayed:
                for box in box_list:
                    if not box.opened and box.x - box_width / 2 <= mouse_pos[0] <= box.x + box_width / 2 and box.y - box_height / 2 <= mouse_pos[1] <= box.y + box_height / 2:
                        if box.blindbox.name == "Điểm đổi quà x3": point += 3
                        if box.blindbox.name == "Điểm đổi quà x2": point += 2
                        if box.blindbox.name == "Điểm đổi quà x1": point += 1
                        box.open()
                        box_quantity -= 1
                        log(box_quantity)
            else:
                circle_x, circle_y = circle_center
                if (mouse_pos[0] - circle_x) ** 2 + (mouse_pos[1] - circle_y) ** 2 <= circle_radius ** 2:
                    alert_displayed = False
        mouse_pos = window.mouse.get_pos()
        if WIDTH - 150 - 20 <= mouse_pos[0] <= WIDTH - 20 and 20 <= mouse_pos[1] <= 70 and not submit_displayed:
            redeem_displayed = not redeem_displayed
        mouse_click_handled = True
    elif not mouse_click[0]:
        mouse_click_handled = False
    for event in window.event.get():
        if event.type == window.KEYDOWN and event.key == window.K_q and (event.mod & window.KMOD_CTRL) and (event.mod & window.KMOD_SHIFT):
            running = False
    window.display.flip()
    delay(0.02)
    # window.time.wait(10)
window.quit()

import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode

def generate_id_cards(excel_path, photo_folder, output_folder):
    df = pd.read_excel(excel_path)
    images = []

    # Load fonts
    font_bold = ImageFont.truetype("arialbd.ttf", 36)
    font_regular = ImageFont.truetype("arial.ttf", 32)
    font_small = ImageFont.truetype("arial.ttf", 26)

    for index, row in df.iterrows():
        name = str(row['Name'])
        role = str(row['Role'])
        id_no = str(row['ID'])
        phone = str(row['Phone'])
        email = str(row['Email'])
        join = str(row['Join'])
        expire = str(row['Expire'])
        blood = str(row.get('BloodGroup', 'O+'))  # optional

        # ----- FRONT CARD -----
        front = Image.new("RGB", (600, 900), "white")
        draw = ImageDraw.Draw(front)

        # 🔶 Extend Header background to cover up to Role (Manager) area
        draw.rectangle([(0, 0), (600, 420)], fill="#1e1e2f")  # Dark background
        draw.polygon([(0, 420), (600, 320), (600, 420)], fill="#f57c00")  # Orange shape
        draw.polygon([(0, 450), (600, 370), (600, 450)], fill="#fbc02d")  # Yellow shape

        # 🔶 Photo handling
        photo_filename = row['Photo'].strip()
        photo_path = os.path.join(photo_folder, photo_filename)

        if os.path.exists(photo_path):
            profile_img = Image.open(photo_path).resize((150, 150)).convert("RGB")

            # Circular mask
            mask = Image.new("L", (150, 150), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, 150, 150), fill=255)

            # Yellow border around photo
            circle_with_border = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
            draw_border = ImageDraw.Draw(circle_with_border)
            draw_border.ellipse((0, 0, 159, 159), fill="yellow")

            # Paste photo in border
            profile_img_rgba = profile_img.convert("RGBA")
            circle_with_border.paste(profile_img_rgba, (5, 5), mask)

            # Paste onto front card
            front.paste(circle_with_border, (220, 110), circle_with_border)

        else:
            draw.text((200, 150), "No Photo", font=font_regular, fill="white")
            print(f"[!] Photo not found for: {name} (Expected: {photo_path})")

        # 🔶 Name and Role centered under the photo, all inside dark area
        name_x = 300 - (font_bold.getlength(name.upper()) / 2)
        draw.text((name_x, 280), name.upper(), font=font_bold, fill="white")

        role_x = 300 - (font_regular.getlength(role.upper()) / 2)
        draw.text((role_x, 330), role.upper(), font=font_regular, fill="#cccccc")


        # Info fields below header
        # --- Info fields with left alignment and smaller font ---
        info_font = font_small
        info_x = 60
        info_y = 500
        line_height = 40

        # Helper function to draw multiline field
        def draw_field(draw, label, value, y):
            label_text = f"{label} : "
            max_width = 470
            full_text = label_text + value

            if font_small.getlength(full_text) <= max_width:
                draw.text((info_x, y), full_text, font=info_font, fill="#333")
                return y + line_height
            else:
                # Wrap long values like email
                max_chars = 35
                value_lines = [value[i:i+max_chars] for i in range(0, len(value), max_chars)]
                draw.text((info_x, y), label_text + value_lines[0], font=info_font, fill="#333")
                for line in value_lines[1:]:
                    y += line_height
                    draw.text((info_x + 30, y), line, font=info_font, fill="#333")
                return y + line_height

        # Draw all fields
        y_pos = info_y
        y_pos = draw_field(draw, "ID NO", id_no, y_pos)
        y_pos = draw_field(draw, "Phone", phone, y_pos)
        y_pos = draw_field(draw, "Email", email, y_pos)
        y_pos = draw_field(draw, "JOIN", join, y_pos)
        y_pos = draw_field(draw, "EXPIRE", expire, y_pos)



        # Save front image
        front_filename = f"{id_no}_{name}.png"
        front_path = os.path.join(output_folder, front_filename)
        front.save(front_path)
        images.append(front_filename)

        # ----- BACK CARD -----
        back = Image.new("RGB", (600, 900), "white")
        draw_back = ImageDraw.Draw(back)

        # Header background
        draw_back.rectangle([(0, 0), (600, 300)], fill="#1e1e2f")
        draw_back.polygon([(0, 300), (600, 200), (600, 300)], fill="#f57c00")  # orange
        draw_back.polygon([(0, 330), (600, 250), (600, 330)], fill="#fbc02d")  # yellow

        # Company Info
        draw_back.text((180, 100), "🌀", font=font_bold, fill="#ffc107")
        draw_back.text((230, 100), "COMPANY NAME", font=font_bold, fill="white")
        draw_back.text((230, 150), "ALWAYS WITH YOU", font=font_small, fill="white")

        # QR Code
        qr_data = f"{name} | {id_no} | {phone}"
        qr_img = qrcode.make(qr_data).resize((150, 150))
        back.paste(qr_img, (225, 340))

       # Blood group pill
        draw_back.rounded_rectangle((160, 520, 480, 570), radius=25, fill="#f57c00")
        draw_back.text((180, 532), f"{blood} Positive blood group", font=font_small, fill="white")


        # Note
        draw_back.text((80, 620), "Important Note", font=font_bold, fill="black")
        draw_back.text((80, 660), "Wear this badge with pride—you're \npart of something great.", font=font_small, fill="#444")

        # Signature (mock)
        draw_back.text((400, 800), "signature", font=font_small, fill="black")

        # Save back image
        back_filename = f"{id_no}_{name}_back.png"
        back_path = os.path.join(output_folder, back_filename)
        back.save(back_path)
        images.append(back_filename)

    return images

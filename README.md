# 🪪 ID Card Generator using Flask and PIL

![ID Screenshot](result.png)

This project generates professional employee ID cards using data from an Excel file and corresponding employee photos. It uses a Flask web interface to handle file uploads and displays real-time previews of the generated ID cards.

## 🚀 Features
- Excel Upload: Input employee details via Excel file.
- Photo Upload: Match and place employee images based on filename.
- Card Design: Automatically generates both front and back of ID cards.
- Preview & Download: Preview generated cards in browser and download PNGs.

---

## 🛠 Scripts Overview
- `app.py` → Main Flask application to run the web server and handle routes.
- `config.py` → Stores path and configuration variables.
- `utils/generator.py` → Core logic to generate and render ID cards using PIL.
- `templates/index.html` → Web interface for uploading Excel and viewing results.

---

## 📦 Dependencies

The project requires the following libraries, listed in `requirements.txt`:
- Flask  
- pandas  
- openpyxl  
- Pillow  
- qrcode  

## Install Dependencies

```bash
pip install -r requirements.txt

```

## 📥 Excel Format

```

Make sure your Excel file has the following columns:

| Name      | Role    | ID     | Phone       | Email             | Join       | Expire     | Photo     | BloodGroup |
|-----------|---------|--------|-------------|-------------------|------------|------------|-----------|------------|
| John Doe  | Manager | EMP001 | 9876543210  | john@example.com  | 2023-01-01 | 2025-01-01 | john.png  | A+         |

- The `Photo` column **must match** the filename in the `static/photos/` directory (e.g., `john.png` should exist there).

```
## 📤 Output

```

- All generated cards will be saved in the `static/id_cards/` folder as **PNG** files.
- You can preview them directly in your **browser** or download them for **printing**.


```
## 🌐 GitHub Integration

```

The project includes detailed steps for version control and pushing code to GitHub for easy collaboration and tracking.

```

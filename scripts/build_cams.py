import os
import urllib.request
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

os.makedirs('d:/trafficsensenew/frontend/public/cams', exist_ok=True)

# 12 Delhi Road Nodes and their sources
CAMS_CONFIG = [
    {
        'id': 'cam_orr_delhi',
        'camId': 'CAM-DEL-ORR-01',
        'name': 'Outer Ring Road (Dhaula Kuan)',
        'speed': '18 km/h',
        'count': '142 veh/min',
        'density': 'HIGH DENSITY - HEAVY CRAWL',
        'color': (239, 68, 68),
        'url': 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Outer_Ring_Road%2C_Nehru_Place_2.jpg',
        'local_fallback': 'd:/trafficsensenew/frontend/public/orr_snapshot.jpg',
        'detections': [
            (210, 310, 390, 470, 'CAR #09', '94%', '18 km/h'),
            (420, 290, 680, 520, 'BUS DTC #21', '98%', '14 km/h'),
            (710, 340, 840, 480, 'AUTO #15', '91%', '22 km/h'),
            (880, 330, 1070, 500, 'CAB #44', '95%', '19 km/h')
        ]
    },
    {
        'id': 'cam_ito_junction',
        'camId': 'CAM-DEL-ITO-02',
        'name': 'ITO Junction (Vikas Marg Link)',
        'speed': '14 km/h',
        'count': '158 veh/min',
        'density': 'HIGH DENSITY - SEVERE CONGESTION',
        'color': (239, 68, 68),
        'url': 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Roads_in_New_Delhi_11.jpg',
        'local_fallback': 'd:/trafficsensenew/frontend/public/cctv_cam.jpg',
        'detections': [
            (180, 280, 340, 440, 'CAR #03', '96%', '12 km/h'),
            (360, 260, 550, 480, 'BUS #10', '97%', '14 km/h'),
            (580, 310, 720, 450, 'AUTO #08', '89%', '15 km/h'),
            (750, 290, 930, 460, 'SUV #12', '93%', '14 km/h')
        ]
    },
    {
        'id': 'cam_aiims_flyover',
        'camId': 'CAM-DEL-RNG-03',
        'name': 'Ring Road (AIIMS Corridor)',
        'speed': '16 km/h',
        'count': '146 veh/min',
        'density': 'HIGH DENSITY - HOSPITAL ZONE',
        'color': (239, 68, 68),
        'url': 'https://upload.wikimedia.org/wikipedia/commons/c/c9/AIIMS_Flyover03.JPG',
        'local_fallback': 'd:/trafficsensenew/frontend/public/orr_snapshot.jpg',
        'detections': [
            (240, 330, 420, 490, 'AMBULANCE', '99%', '32 km/h'),
            (460, 310, 640, 480, 'CAR #31', '92%', '16 km/h'),
            (680, 320, 890, 510, 'TAXI #05', '95%', '15 km/h')
        ]
    },
    {
        'id': 'cam_mukarba_chowk',
        'camId': 'CAM-DEL-MKR-04',
        'name': 'Mukarba Chowk (GT Karnal Rd)',
        'speed': '19 km/h',
        'count': '138 veh/min',
        'density': 'HIGH DENSITY - FREIGHT CORRIDOR',
        'color': (239, 68, 68),
        'url': 'https://upload.wikimedia.org/wikipedia/commons/d/d9/Flyover_at_Vikaspuri_on_Outer_Ring_Road%2C_Delhi.jpg',
        'local_fallback': 'd:/trafficsensenew/frontend/public/hebbal_snapshot.jpg',
        'detections': [
            (200, 270, 440, 520, 'HGV TRUCK #02', '98%', '20 km/h'),
            (470, 320, 680, 490, 'INTERSTATE BUS', '96%', '22 km/h'),
            (720, 340, 880, 480, 'MINITRUCK', '92%', '24 km/h')
        ]
    },
    {
        'id': 'cam_vikas_marg',
        'camId': 'CAM-DEL-VKM-05',
        'name': 'Vikas Marg (Laxmi Nagar)',
        'speed': '24 km/h',
        'count': '92 veh/min',
        'density': 'MODERATE - TRANS-YAMUNA',
        'color': (245, 158, 11),
        'url': 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Roads_in_New_Delhi_11.jpg',
        'local_fallback': 'd:/trafficsensenew/frontend/public/cctv_cam.jpg',
        'detections': [
            (280, 320, 450, 460, 'CAR #14', '94%', '24 km/h'),
            (490, 330, 630, 450, 'AUTO #22', '90%', '26 km/h'),
            (670, 310, 880, 480, 'CAR #18', '93%', '23 km/h')
        ]
    },
    {
        'id': 'cam_rohtak_road',
        'camId': 'CAM-DEL-RTK-06',
        'name': 'Rohtak Road (Punjabi Bagh)',
        'speed': '26 km/h',
        'count': '88 veh/min',
        'density': 'MODERATE - INDUSTRIAL ROUTE',
        'color': (245, 158, 11),
        'url': 'https://upload.wikimedia.org/wikipedia/commons/d/d9/Flyover_at_Vikaspuri_on_Outer_Ring_Road%2C_Delhi.jpg',
        'local_fallback': 'd:/trafficsensenew/frontend/public/hebbal_snapshot.jpg',
        'detections': [
            (220, 340, 420, 490, 'TRUCK #11', '95%', '24 km/h'),
            (460, 330, 640, 470, 'CAR #07', '91%', '28 km/h'),
            (690, 340, 850, 480, 'AUTO #19', '88%', '27 km/h')
        ]
    },
    {
        'id': 'cam_cp_circle',
        'camId': 'CAM-DEL-CP-07',
        'name': 'Connaught Place Circle (Radial)',
        'speed': '22 km/h',
        'count': '104 veh/min',
        'density': 'MODERATE - CBD CIRCULAR',
        'color': (245, 158, 11),
        'url': None,
        'local_fallback': 'd:/trafficsensenew/frontend/public/landmarks/connaught_place.jpg',
        'detections': [
            (250, 320, 430, 470, 'SEDAN #12', '95%', '22 km/h'),
            (460, 330, 620, 460, 'CAB #08', '93%', '20 km/h'),
            (660, 310, 830, 460, 'SUV #04', '94%', '23 km/h')
        ]
    },
    {
        'id': 'cam_nh48_delhi',
        'camId': 'CAM-DEL-NH48-08',
        'name': 'NH-48 Airport Expressway',
        'speed': '28 km/h',
        'count': '95 veh/min',
        'density': 'MODERATE - AIRPORT ACCESS',
        'color': (245, 158, 11),
        'url': 'https://upload.wikimedia.org/wikipedia/commons/5/58/Delhi-Gurgaon_Expressway.jpg',
        'local_fallback': 'd:/trafficsensenew/frontend/public/ecity_snapshot.jpg',
        'detections': [
            (190, 300, 380, 450, 'AIRPORT TAXI', '97%', '30 km/h'),
            (410, 290, 600, 460, 'CAR #52', '94%', '32 km/h'),
            (640, 280, 840, 470, 'AIRPORT SHUTTLE', '98%', '28 km/h'),
            (870, 310, 1040, 460, 'SEDAN #19', '92%', '34 km/h')
        ]
    },
    {
        'id': 'cam_barapullah',
        'camId': 'CAM-DEL-BRP-09',
        'name': 'Barapullah Elevated Bypass',
        'speed': '44 km/h',
        'count': '48 veh/min',
        'density': 'LOW DENSITY - SMOOTH FLYOVER',
        'color': (16, 185, 129),
        'url': None,
        'local_fallback': 'd:/trafficsensenew/frontend/public/landmarks/barapullah.jpg',
        'detections': [
            (260, 340, 430, 470, 'SEDAN #01', '96%', '46 km/h'),
            (520, 330, 710, 470, 'SUV #15', '95%', '44 km/h'),
            (780, 350, 950, 480, 'CAR #23', '93%', '45 km/h')
        ]
    },
    {
        'id': 'cam_mathura_road',
        'camId': 'CAM-DEL-MTR-10',
        'name': 'Mathura Road (Ashram Underpass)',
        'speed': '38 km/h',
        'count': '54 veh/min',
        'density': 'LOW DENSITY - REGULATED FLOW',
        'color': (16, 185, 129),
        'url': 'https://upload.wikimedia.org/wikipedia/commons/6/68/Traffic_Congestion_-_Mathura_Road_-_New_Delhi_2014-05-13_2736.JPG',
        'local_fallback': 'd:/trafficsensenew/frontend/public/orr_snapshot.jpg',
        'detections': [
            (220, 320, 410, 470, 'CAR #11', '94%', '36 km/h'),
            (460, 310, 660, 480, 'BUS DTC #08', '97%', '32 km/h'),
            (720, 330, 890, 470, 'SEDAN #09', '95%', '39 km/h')
        ]
    },
    {
        'id': 'cam_aurobindo_marg',
        'camId': 'CAM-DEL-ARB-11',
        'name': 'Aurobindo Marg (Hauz Khas)',
        'speed': '36 km/h',
        'count': '58 veh/min',
        'density': 'LOW DENSITY - GREEN CORRIDOR',
        'color': (16, 185, 129),
        'url': 'https://upload.wikimedia.org/wikipedia/commons/6/65/Aurobindo_Road_near_Hauz_Khas%2C_New_Delhi.jpg',
        'local_fallback': 'd:/trafficsensenew/frontend/public/cctv_cam.jpg',
        'detections': [
            (290, 330, 470, 470, 'CAR #06', '96%', '35 km/h'),
            (530, 340, 710, 470, 'CAB #14', '94%', '38 km/h'),
            (760, 330, 920, 470, 'AUTO #03', '90%', '33 km/h')
        ]
    },
    {
        'id': 'cam_dnd_flyway',
        'camId': 'CAM-DEL-DND-12',
        'name': 'DND Flyway (Mayur Vihar - Noida)',
        'speed': '42 km/h',
        'count': '52 veh/min',
        'density': 'LOW DENSITY - EXPRESSWAY BRIDGE',
        'color': (16, 185, 129),
        'url': 'https://upload.wikimedia.org/wikipedia/commons/e/e8/DND_Flyway.jpg',
        'local_fallback': 'd:/trafficsensenew/frontend/public/highway_trails.jpg',
        'detections': [
            (210, 330, 400, 470, 'SUV #10', '97%', '44 km/h'),
            (450, 320, 650, 470, 'SEDAN #33', '96%', '42 km/h'),
            (710, 310, 910, 480, 'CAR #45', '95%', '46 km/h')
        ]
    }
]

def load_base_image(config):
    url = config.get('url')
    fallback = config.get('local_fallback')
    img = None
    if url:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'TrafficSenseDelhi/1.0 (GIS Assistant)'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                from io import BytesIO
                img = Image.open(BytesIO(resp.read())).convert('RGB')
                print(f"Downloaded online photo for {config['id']}")
        except Exception as e:
            print(f"Failed online download for {config['id']}: {e}")
    if img is None and fallback and os.path.exists(fallback):
        img = Image.open(fallback).convert('RGB')
        print(f"Loaded local fallback for {config['id']} from {fallback}")
    if img is None:
        img = Image.open('d:/trafficsensenew/frontend/public/cctv_cam.jpg').convert('RGB')
    return img

def render_synthetic_cam_overlay(img, cfg):
    # Resize to 1280 x 720 HD surveillance standard
    img = img.resize((1280, 720), Image.Resampling.LANCZOS)
    
    # Slight surveillance contrast and color enhancement
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.12)
    
    overlay = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        font_large = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 24)
        font_med = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 18)
        font_small = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 14)
        font_tiny = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 12)
    except:
        font_large = ImageFont.load_default()
        font_med = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
    
    # Subtle scanlines across frame
    for y in range(0, 720, 4):
        draw.line([(0, y), (1280, y)], fill=(0, 0, 0, 28))
    
    # Top Telemetry Bar
    draw.rectangle([(0, 0), (1280, 48)], fill=(10, 15, 29, 215))
    draw.line([(0, 48), (1280, 48)], fill=(56, 189, 248, 180), width=1)
    
    # Blinking REC dot
    draw.ellipse([(20, 16), (34, 30)], fill=(239, 68, 68, 255))
    draw.text((42, 14), "● REC [LIVE SURVEILLANCE FEED]", fill=(255, 255, 255, 255), font=font_med)
    
    # Camera Node & Location
    draw.text((460, 14), f"NODE: {cfg['camId']}", fill=(56, 189, 248, 255), font=font_med)
    draw.text((720, 14), f"LOC: {cfg['name']}", fill=(241, 245, 249, 240), font=font_small)
    
    # Timestamp
    draw.text((1060, 14), "2026-10-29 13:58:00 IST", fill=(226, 232, 240, 220), font=font_small)
    
    # Center Crosshair Reticle
    cx, cy = 640, 360
    ch_color = (56, 189, 248, 120)
    draw.line([(cx - 24, cy), (cx + 24, cy)], fill=ch_color, width=1)
    draw.line([(cx, cy - 24), (cx, cy + 24)], fill=ch_color, width=1)
    draw.ellipse([(cx - 10, cy - 10), (cx + 10, cy + 10)], outline=ch_color, width=1)
    
    # Computer Vision YOLO / Object Detection Bounding Boxes
    for box in cfg.get('detections', []):
        x1, y1, x2, y2, label, conf, spd = box
        bcolor = (0, 255, 170, 230)  # Neon mint green
        bg_tag = (10, 30, 25, 220)
        
        # Bounding box corners (brackets)
        k = 12
        w = 2
        # Top-left
        draw.line([(x1, y1), (x1 + k, y1)], fill=bcolor, width=w)
        draw.line([(x1, y1), (x1, y1 + k)], fill=bcolor, width=w)
        # Top-right
        draw.line([(x2, y1), (x2 - k, y1)], fill=bcolor, width=w)
        draw.line([(x2, y1), (x2, y1 + k)], fill=bcolor, width=w)
        # Bottom-left
        draw.line([(x1, y2), (x1 + k, y2)], fill=bcolor, width=w)
        draw.line([(x1, y2), (x1, y2 - k)], fill=bcolor, width=w)
        # Bottom-right
        draw.line([(x2, y2), (x2 - k, y2)], fill=bcolor, width=w)
        draw.line([(x2, y2), (x2, y2 - k)], fill=bcolor, width=w)
        
        # Dashed/faint box body
        draw.rectangle([(x1, y1), (x2, y2)], outline=(0, 255, 170, 70), width=1)
        
        # Label Tag Pill
        tag_text = f"{label} {conf} | {spd}"
        draw.rectangle([(x1, y1 - 20), (x1 + 180, y1)], fill=bg_tag)
        draw.rectangle([(x1, y1 - 20), (x1 + 180, y1)], outline=bcolor, width=1)
        draw.text((x1 + 6, y1 - 17), tag_text, fill=(255, 255, 255, 255), font=font_tiny)
    
    # Bottom Telemetry Overlay Strip
    draw.rectangle([(0, 670), (1280, 720)], fill=(10, 15, 29, 225))
    draw.line([(0, 670), (1280, 670)], fill=(56, 189, 248, 180), width=1)
    
    # Bottom Left: Speed and Volume Radar
    draw.text((20, 678), f"SPEED RADAR: {cfg['speed']}", fill=(56, 189, 248, 255), font=font_med)
    draw.text((260, 678), f"VOLUME: {cfg['count']}", fill=(241, 245, 249, 240), font=font_med)
    
    # Bottom Center: Status / Density Pill
    draw.text((540, 678), f"STATUS: {cfg['density']}", fill=cfg['color'] + (255,), font=font_med)
    
    # Bottom Right: Sensor Model & FPS
    draw.text((1020, 678), "FLIR-AI SENSOR · 30 FPS FHD", fill=(148, 163, 184, 220), font=font_small)
    
    # Composite overlay onto base image
    final_img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    return final_img

# Generate all 12 camera images
for cfg in CAMS_CONFIG:
    out_path = f"d:/trafficsensenew/frontend/public/cams/{cfg['id']}.jpg"
    print(f"Generating synthetic camera image for {cfg['id']}...")
    raw = load_base_image(cfg)
    processed = render_synthetic_cam_overlay(raw, cfg)
    processed.save(out_path, quality=92)
    print(f"[OK] Saved {out_path} ({os.path.getsize(out_path)} bytes)")

print("\nAll 12 synthetic traffic surveillance camera snapshots generated successfully!")

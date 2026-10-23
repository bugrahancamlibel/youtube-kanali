"""usage: python3 sheet.py out.png img1 img2 ... (tiles 4 per row at 480x270, labels with file name)"""
import sys
from PIL import Image, ImageDraw
out = sys.argv[1]; files = sys.argv[2:]
cols = 4; w, h = 480, 270
rows = (len(files) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * (h + 22)), (10, 10, 20))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert('RGB').resize((w, h))
    x, y = (i % cols) * w, (i // cols) * (h + 22)
    sheet.paste(im, (x, y + 22)); d.text((x + 6, y + 4), f.split('/')[-1], fill=(220, 220, 220))
sheet.save(out)

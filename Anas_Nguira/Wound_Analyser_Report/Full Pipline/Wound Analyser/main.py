from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import segmentation_models_pytorch as smp
import torch
from torchvision import transforms
from PIL import Image
import numpy as np
import uuid, time, io, os

app = FastAPI(title="API segmentation multiclass")

# dossier d’export
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ===================== CHARGER LE VRAI MODELE =====================

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = smp.DeepLabV3Plus(
    encoder_name="resnet101",
    encoder_weights=None,
    in_channels=3,
    classes=4       # IMPORTANT : même valeur qu’au training
)
model.load_state_dict(torch.load("best_multiclass_model.pth", map_location=device))
model.to(device)
model.eval()

print("🔥 Modèle DeepLabV3+ chargé correctement !")

# ===================== PREPROCESS =====================

preprocess = transforms.Compose([
    transforms.Resize((512, 512)),    # même resize que training
    transforms.ToTensor()
])

# couleurs (classe → RGB)
COLOR_MAP = np.array([
    [0, 0, 0],       # 0 = background
    [255, 0, 0],     # 1 = red (fibrin)
    [0, 255, 0],     # 2 = green (granulation)
    [0, 0, 255]      # 3 = blue (callus)
], dtype=np.uint8)

# ===================== FONCTION D'ANALYSE =====================

def analyze_colors(mask_path):
    img = Image.open(mask_path).convert("RGB")
    arr = np.array(img)
    h, w, _ = arr.shape
    total = h * w

    target = {
        (255, 0, 0): "fibrin_red",
        (0, 255, 0): "granulation_green",
        (0, 0, 255): "callus_blue"
    }

    counts = {name: np.sum(np.all(arr == rgb, axis=-1)) for rgb, name in target.items()}
    percentages = {name: round((c/total)*100, 2) for name, c in counts.items()}

    bg = total - sum(counts.values())
    percentages["background"] = round((bg/total)*100, 2)

    return percentages

# ===================== ENDPOINT =====================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Veuillez envoyer une image.")

    try:
        # Lire image
        data = await file.read()
        img = Image.open(io.BytesIO(data)).convert("RGB")

        # Préprocess
        x = preprocess(img).unsqueeze(0).to(device)

        # Inférence
        with torch.no_grad():
            logits = model(x)
            pred = torch.argmax(logits, dim=1).cpu().numpy()[0]  # (H,W)

        # Générer masque coloré
        color_mask = COLOR_MAP[pred]
        mask_img = Image.fromarray(color_mask)

        filename = f"mask_{int(time.time()*1000)}_{uuid.uuid4().hex[:6]}.png"
        path = os.path.join("static", filename)
        mask_img.save(path)

        # Analyse
        stats = analyze_colors(path)

        return {
            "original": file.filename,
            "mask_url": f"http://localhost:8000/static/{filename}",
            "analysis": stats
        }

    except Exception as e:
        raise HTTPException(500, f"Erreur interne : {e}")

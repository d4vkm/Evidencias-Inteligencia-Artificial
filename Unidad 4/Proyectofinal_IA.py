from ultralytics import YOLO
import torch

def train_model():
    model = YOLO("yolov8m.pt")  # O 'yolov8s.pt' para mejor precisión
    results = model.train(
        data="fa.v1i.yolov8\data.yaml",
         epochs=300,  # Aumentar épocas
         batch=16,
         imgsz=640,
         cls=1.5,  # Peso extra para clases minoritarias
         optimizer='AdamW',
         lr0=1e-3,
         patience=30,  # Early stopping si no mejora
         overlap_mask=True,
         name='emociones_v3'   
    )

if __name__ == "__main__":
    torch.multiprocessing.freeze_support()  # Crucial para Windows
    train_model()
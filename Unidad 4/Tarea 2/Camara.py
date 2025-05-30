from ultralytics import YOLO
import cv2

# 1. Cargar modelo con verificación
try:
    model = YOLO('runs/detect/emociones_model3/weights/last.pt')
    print("Clases del modelo:", model.names)
except Exception as e:
    print("Error cargando modelo:", e)
    exit()

# 2. Configurar cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara")
    exit()

# 3. Procesamiento de frames
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede leer el frame")
        break
    
    # 4. Detección con parámetros óptimos
    results = model(frame, 
                   imgsz=640,
                   conf=0.5,  # Umbral de confianza
                   iou=0.45,  # Umbral de NMS
                   device='0')  # Usar GPU
    
    # 5. Mostrar resultados
    if len(results) > 0:
        annotated_frame = results[0].plot()
        cv2.imshow("Detección", annotated_frame)
    else:
        print("No se detectaron objetos")
        cv2.imshow("Detección", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
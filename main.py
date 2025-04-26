from ultralytics import YOLO


#worker loads and prepares your data in the background, since you have 10 images you do not need it at all.
model = YOLO("yolov8n.yaml")
model.train(data="dataset.yaml", epochs=200, device="cuda",workers=0)


# model = YOLO("runs/detect/train/weights/best.pt")
# results = model("sample_id.png", save=True)

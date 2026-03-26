from ultralytics import YOLO

model = YOLO("D:\\SSDP\\traffic\\checkpoints\\best.pt")
print(model.names)
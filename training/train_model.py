from ultralytics import YOLO
from roboflow import Roboflow


def main():



    # Automatically get dataset path
    data_yaml = r"D:\SSDP\traffic\Ambulance-2\data.yaml"

    print("Dataset path:", data_yaml)

    # Load YOLO model
    model = YOLO("yolov8s.pt")

    # Train model
    model.train(
        data=data_yaml,
        epochs=40,
        imgsz=960,      # better for traffic cameras
        batch=2,
        device=0,
        workers=2,
        cache=True,
        plots=True,
        amp=False,

        # Augmentation
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=10,
        translate=0.1,
        scale=0.5,
        shear=2.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.2
    )

    print("Training complete")


if __name__ == "__main__":
    main()
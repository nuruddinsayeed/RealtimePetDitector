from ultralytics import YOLO

# Loading yolov8 model
model = YOLO('yolov8n.yaml')  # To build a new model using yolo nano version

# Using the model
results = model.train(data='pet_deteciton_config.yaml', epochs=90)  # train the model

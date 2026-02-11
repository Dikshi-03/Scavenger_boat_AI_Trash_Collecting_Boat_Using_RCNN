import torch
from torchvision import transforms
from PIL import Image
from picamera2 import Picamera2
import cv2

class VisionModule:
    def __init__(self, model_path, threshold=0.6, debug=False, show_boxes=True):
        # Use GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load TorchScript model
        self.model = torch.jit.load(model_path).to(self.device)
        self.model.eval()

        # Transform for images
        self.transform = transforms.Compose([transforms.ToTensor()])

        # Detection settings
        self.threshold = threshold
        self.debug = debug
        self.show_boxes = show_boxes

        # Initialize Pi Camera
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_preview_configuration(
            main={"format": 'RGB888', "size": (640, 480)}))
        self.camera.start()

    def detect_trash(self):
        # Capture frame
        frame = self.camera.capture_array()
        image = Image.fromarray(frame)

        # Convert to tensor
        img_tensor = self.transform(image).to(self.device)

        # Forward pass (TorchScript FasterRCNN returns (losses, detections))
        with torch.no_grad():
            outputs = self.model([img_tensor])  

        detections = outputs[1][0]  # take detections of the first image

        trash_detected = False
        boxes = []
        if "scores" in detections:
            scores = detections['scores'].cpu().numpy()
            all_boxes = detections['boxes'].cpu().numpy()

            for score, box in zip(scores, all_boxes):
                if score > self.threshold:
                    trash_detected = True
                    boxes.append((box, score))

        # Debug visualization
        if self.debug:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if trash_detected:
                cv2.putText(frame_bgr, "Trash Detected!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if self.show_boxes:
                    for (box, score) in boxes:
                        x1, y1, x2, y2 = box
                        cv2.rectangle(frame_bgr, (int(x1), int(y1)), (int(x2), int(y2)),
                                      (0, 255, 0), 2)
                        cv2.putText(frame_bgr, f"{score:.2f}", (int(x1), int(y1) - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow("Trash Detection", frame_bgr)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.close()
                exit(0)

        return trash_detected

    def close(self):
        self.camera.close()
        cv2.destroyAllWindows()

import torch
import torchvision.transforms as transforms
from PIL import Image
import os

def run_cnn_model(image_name, model_name, preprocessing): #might need to adjust the evaluation for different models

    device = 'cpu'
    # Load the model (ensure the model is in your project's directory)
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', f'{model_name}.pt')
    model = torch.load(model_path, map_location=torch.device(device))
    model.eval()

    # Preprocess the image
    image_path = os.path.join(os.path.dirname(__file__), '..', 'images', f'{image_name}')
    image = Image.open(image_path)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),          # Resize the image
        transforms.Grayscale(num_output_channels=3),  # Convert image to grayscale and replicate channels
        transforms.ToTensor(),                  # Convert the image to a PyTorch tensor
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize
    ])
    image = transform(image).unsqueeze(0)  # Add batch dimension
    image = image.to(torch.device(device))

    # Run the model
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
        probability = torch.nn.functional.softmax(outputs, dim=1)[0][predicted].item()

    # Convert class index to label (if necessary)
    # result_label = class_index_to_label(predicted.item())
    result_label = predicted.item()

    return result_label, probability

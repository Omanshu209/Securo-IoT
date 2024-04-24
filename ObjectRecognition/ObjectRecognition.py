from torch.nn import Linear as nn_Linear
from torch.cuda import is_available as cuda_is_available
from torch import load as load_model
from torch import max as torch_max
from torch import no_grad
from torchvision import transforms
from torchvision.models import resnet18

classes = [
    "Hand",
    "Face",
    "Pen", 
    "Water Bottle", 
    "Watch"
]

class ObjectRecogniser:
	
	def __init__(self, model_path = "Model/ObjectClassification_CNN_ResNet18.pt"):
		
		self.transform = transforms.Compose(
			[
				transforms.Resize((200, 300)),
				transforms.ToTensor(),
			]
		)
		
		self.device = "cuda" if cuda_is_available() else "cpu"
		self.Model = self.load_model(model_path)
		self.Model.eval()
	
	def load_model(self, model_path):
		Model = resnet18(pretrained = False)
		
		for parameter in Model.parameters():
			parameter.requires_grad = False
		
		Model.fc = nn_Linear(512, 5)
		
		Model.load_state_dict(
			load_model(
				model_path, 
				map_location = self.device
			)
		)
		
		return Model
	
	def transform_image(self, image):
		transformed_image = self.transform(image.convert("RGB"))
		return transformed_image
	
	def predict(self, transformed_image):
		with no_grad():
			y_pred = self.Model(transformed_image.unsqueeze(0).to(self.device))
			
			y_pred_tensor = torch_max(y_pred, 1)[1]
			y_pred_string = classes[y_pred_tensor]
		
		return y_pred_string
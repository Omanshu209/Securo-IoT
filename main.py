import os
from kivymd.app import MDApp
from kivy.lang import Builder
from PIL import Image, ImageDraw
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.label.label import MDLabel
from kivy.core.text import LabelBase, DEFAULT_FONT
from facenet_pytorch import MTCNN, InceptionResnetV1

LabelBase.register(DEFAULT_FONT, "assets/nasalization.ttf")

mtcnn = MTCNN(keep_all = True).eval()
resnet = InceptionResnetV1(pretrained = "vggface2").eval()

embeddings_users = {}
for user in os.listdir("users"):
	for img in os.listdir(f"users/{user}"):
		img_pil = Image.open(f"users/{user}/{img}")
		aligned = mtcnn(img_pil)
		embeddings = resnet(aligned).detach()
		embeddings_users[user] = embeddings

class SecurityApp(MDApp):
	
	def build(self):
		self.detect_num = 0
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "DeepPurple"
		self.theme_cls.material_style = "M3"
		return Builder.load_file("Design.kv")
	
	def on_start(self):
		for i in range(20):
			self.root.ids.faces.add_widget(
				MDSmartTile(
					MDLabel(
						text = "Person", 
						bold = True,
						color = (241 / 255, 6 / 255, 11 / 255, 1)
					), 
					
					id = str(i + 1), 
					radius = 24, 
					box_radius = [0, 0, 24, 24], 
					box_color = (1, 1, 1, 0.2), 
					source = "images/security_cam.png", 
					size_hint = (0.2, 0.2)
				)
			)
	
	def predict_faces(self):
		self.detect_num += 1
		
		self.root.ids.cam.export_to_png("images/clicked_image.png")
		clicked_image = Image.open("images/clicked_image.png")
		clicked_image_rgb = clicked_image.convert("RGB")
		boxes, _ = mtcnn.detect(clicked_image_rgb)
		
		for image in os.listdir("images"):
			if image.startswith("face"):
				os.remove(f"images/{image}")
		
		mtcnn(clicked_image_rgb, save_path = f"images/face{self.detect_num}.png")
		
		image_draw = clicked_image.copy()
		draw = ImageDraw.Draw(image_draw)
		if boxes is not None:
			for box in boxes:
				print(box.tolist())
				draw.rectangle(box.tolist(), outline = (255, 0, 0), width = 5)
		
		image_draw.save("images/predicted.png")
		self.root.ids.img_detected.source = "images/predicted.png"
		self.root.ids.img_detected.reload()
		
		for child in self.root.ids.faces.children[:]:
			if int(child.id) == 1:
				path = f"images/face{self.detect_num}.png"
			else:
				path = f"images/face{self.detect_num}_{child.id}.png"
			
			child.source = path if os.path.exists(path) else "images/security_cam.png"
			
		
		self.root.ids.status_label.text = "locked"
		self.root.ids.status_label.text_color = (1, 0, 0, 1)
	
	def verify_faces(self):
		def verify() -> bool:
			for user in os.listdir("images"):
				if user.startswith("face"):
					image = Image.open(f"images/{user}")
					aligned1 = mtcnn(image)
					embed1 = resnet(aligned1).detach()
					for ver_user in embeddings_users:
						embed2 = embeddings_users[ver_user]
						distance = (embed1 - embed2).norm().item()
						
						if(distance < 1):
							return True
			return False
		
		if(verify()):
			self.root.ids.status_label.text = "unlocked"
			self.root.ids.status_label.text_color = (0, 1, 0, 1)

if __name__ == "__main__":
	SecurityApp().run()
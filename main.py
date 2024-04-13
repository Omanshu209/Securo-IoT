import os
from kivymd.app import MDApp
from kivy.lang import Builder
from PIL import Image, ImageDraw
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.label.label import MDLabel
from kivy.core.text import LabelBase, DEFAULT_FONT
from facenet_pytorch import MTCNN, InceptionResnetV1

LabelBase.register(DEFAULT_FONT, "assets/nasalization.ttf")

mtcnn = MTCNN(keep_all = True)

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
					source = f"images/security_cam.png", 
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
				child.source = f"images/face{self.detect_num}.png"
			else:
				child.source = f"images/face{self.detect_num}_{child.id}.png"

if __name__ == "__main__":
	SecurityApp().run()
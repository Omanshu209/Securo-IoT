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
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "DeepPurple"
		self.theme_cls.material_style = "M3"
		return Builder.load_file("Design.kv")
	
	def predict_faces(self):
		self.root.ids.cam.export_to_png("images/clicked_image.png")
		clicked_image = Image.open("images/clicked_image.png")
		boxes, _ = mtcnn.detect(clicked_image.convert("RGB"))
		
		image_draw = clicked_image.copy()
		draw = ImageDraw.Draw(image_draw)
		if boxes is not None:
			for box in boxes:
				print(box.tolist())
				draw.rectangle(box.tolist(), outline = (255, 0, 0), width = 5)
		
		image_draw.save("images/predicted.png")
		self.root.ids.img_detected.source = "images/predicted.png"
		self.root.ids.img_detected.reload()

if __name__ == "__main__":
	SecurityApp().run()
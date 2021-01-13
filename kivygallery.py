from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
Builder.load_string("""
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Window kivy.core.window.Window
<Gallery>
	img_sources:["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg"]
	Carousel:
		id:gallery
		loop:True
		anim_type:"in_out_circ"
		on_current_slide:root.indicae_slide(*args)
		pos_hint:{"center_x":.5, "center_y":.5}
		
	GaleryButton:
		text:'<'
		size_hint:.05, .05
		pos_hint:{"center_x":.1, "center_y":.5}
		on_press:gallery.load_previous()
	GaleryButton:
		text:'>'
		size_hint:.05, .05
		pos_hint:{"center_x":.9, "center_y":.5}
		on_press:gallery.load_next()
	BoxLayout:
		id:gallery_navs
		spacing:10
		size_hint_x: .20 if len(self.children) <= 5 else .50
		size_hint_y: .05
		pos_hint:{"center_x":.5, "center_y":.05}


<GaleryButton>
	opacity:1 if self.collide_point(*Window.mouse_pos) else 0.5
	canvas.before:
		Color:
			rgba:get_color_from_hex(self.background_color)
		Ellipse:
			size:self.size
			pos:self.pos

<MyImage>:
	canvas.before:
		Rectangle:
			source:self.source
			size:self.size
			pos:self.pos
""")

class GaleryButton(ButtonBehavior, Label):
	background_color = StringProperty('#808080')

class MyImage(Label):
	source = StringProperty()

class Gallery(FloatLayout):
	img_sources = ListProperty([])
	def __init__(self,**kwargs):
		super(Gallery,self).__init__(**kwargs)
		Clock.schedule_once(self.accept_images, 0)

	def accept_images(self):
		for index, img_src in enumerate(self.img_sources):
			async_img = MyImage(source = img_src)
			self.ids.gallery.add_widget(async_img)
			self.ids.gallery_navs.add_widget(GaleryButton(text=str(index),
				on_press=self.load_currentslide,
				background_color="#1E90FF"))

		self.ids.gallery_navs.children[-1].disabled = True #last item in list is dissabled 
		Clock.schedule_interval(lambda dt:self.ids.gallery.load_next(), 6) #in every 6 seconds loads next slide

	def load_currentslide(self, button):
		gallery = self.ids.gallery
		gallery.load_slide(gallery.slides[int(button.text)])

	def indicae_slide(self, *args):
		gallery = self.ids.gallery
		navbtns = self.ids.gallery_navs.children
		for btn  in navbtns:
			if int(btn.text) == gallery.index:
				btn.disabled = True
			else:
				btn.disabled = False





class SimpleApp(App):
	def build(self):
		return Gallery()



SimpleApp().run()

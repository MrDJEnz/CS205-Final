class SpritePays():
    def __init__(self,surface,name_id):
        self.map_pays=surface
        self.name_pays=''
        self.id=int(name_id[-6:-4])
        self.bounds=surface.get_bounding_rect()

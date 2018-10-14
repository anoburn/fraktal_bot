class parameters:

    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x_center = 0.
        self.y_center = 0.
        self.zoom = 1.
        self.max_iteration = 10
        self.width = 480
        self.height = 480
        self.booster = 1.
        self.boosted = False
    
    def to_string(self):
        text = str(self.x_center) + " " + str(self.y_center) + " "
        text += str(self.zoom) + " " + str(self.max_iteration) + " "
        text += str(self.width) + " " + str(self.height)
        
        return text
    
    def zoom_in(self):
        self.zoom *= pow(0.9, self.booster)
    
    def zoom_out(self):
        self.zoom *= pow(1.1, self.booster)
        
    def more_detail(self):
        self.max_iteration *= pow(1.25, self.booster)
        if(self.max_iteration > 200):
            self.max_iteration = 200
            return "Maximum detail reached. (Have mercy with my PC ...)"
    
    def less_detail(self):
        self.max_iteration *= pow(0.75, self.booster)
        
    def move_up(self):
        self.y_center -= self.zoom * 0.1 * self.booster
    
    def move_down(self):
        self.y_center += self.zoom * 0.1 * self.booster
        
    def move_left(self):
        self.x_center -= self.zoom * 0.1 * self.booster
        
    def move_right(self):
        self.x_center += self.zoom * 0.1 * self.booster
        
    def toggle_boost(self):
        if(self.boosted):
            self.boosted = False
            self.booster = 1.
            return "Boost deactivated"
        else:
            self.boosted = True
            self.booster = 5.
            return "Boost activated"

    def set_size(self, x, y):
        self.width  = x
        self.height = y

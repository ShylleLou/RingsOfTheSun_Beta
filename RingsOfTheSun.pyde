"""
Name: Shylle Yocte
Email: 3044817@gscs.ca
Final Project: Rings of the Sun

Issues with program (Gonna try to fix):
    - for some reason, it wont let me use one variable for audio for me to share across functions
    - quad() @ mouseClicked() does not appear sometimes (systematic)
    - when popping one off the asteoids from multiple copies, it removes the other asteroids too in some occasion (random)
    - need to restrict the laser from drawing when starting game, as well as thetarget cursor after game over when pushin return button
    
To add/ fix:
    - MAKE TWINKLING STARS APPEAR AFTER GAME OVER
          - already checked that the size is okay
    - restrict laser and target cursor
    

"""
add_library('sound')

score = 0
current_function = "MenuScreen"

music = [ "723909__kevp888__2024-02-16_background-sound_game-music_remix.wav", "667375__bloodpixelhero__retro-tense-loop.wav"]
MCursor = loadImage("Main_Cursor.png")

background_volume = 1.0
effect_volume = 1.0


global Background_sound, click

def setup():
    size (1000, 700)
    frameRate(-1)
    global Background_sound, music
    Background_sound = SoundFile(this, music[0])
    Background_sound.stop()
    Background_sound.loop()
    MCursor = loadImage("Main_Cursor.png")
    MCursor.resize(70, 70)
    cursor(MCursor, 0, 0)
    #makes up initial star positions
    for _ in range(0, 5):
        star_x = random(0, width)
        star_y = random(0, height)
        show_stars.append(Star(star_x, star_y))
    return

#THIS SETS UP THE TARGETCURSOR


def target_cursor(x, y):
    strokeWeight(2)
    noFill()
    ellipse(x, y, 5, 5)
    ellipse(x, y, 50, 50)
    line (x, y - 40, x, y - 20)
    line (x, y + 39, x, y + 19)
    line (x - 40, y, x - 20, y )
    line (x + 40, y, x + 20, y )
    

#THIS IS THE MENU SCREEN SECTION    

class Button:
    
    def __init__(self, x_coord, y_coord, width, height, button_name, play):
        self.x_coord = x_coord 
        self.y_coord = y_coord 
        self.width = width
        self.height = height
        self.button_name = button_name
        self.play = play
        
    def display_button(self):
        noFill()
        stroke(255)
        #creates the button while getting its position and size from the text
        rect(self.x_coord - self.width/2, self.y_coord - self.height/2, self.width, self.height)
        fill(255)
        textAlign(CENTER,CENTER)
        textSize(35)
        text(self.button_name, self.x_coord , self.y_coord )
        
    #restricts to where the mouse can interact with buttons
    def mouse_interact(self):
        return (self.x_coord - self.width/2 < mouseX < self.x_coord + self.width/2 and self.y_coord - self.height/2 < mouseY < self.y_coord + self.height/2)

def Menu_screen():
    global current_function, Background_sound, music, MCursor, effect_volume
    img = loadImage("MenuBackground.png")
    background(img)
    font = createFont("InYourFaceJeffory.ttf", 1)
    noTint()
    textFont(font)
    textAlign(CENTER, CENTER)
    fill(255)
    textSize(150)
    text("Rings of the Sun", width/2, height/2-130)
    strokeWeight(2)
    #Buttons
    Button_1 = Button(width/2, 360, 200, 50, "Start Game", play_game)
    Button_1.display_button()
    
    Button_2 = Button(width/2, 430, 200, 50, "Settings", settings_game)
    Button_2.display_button()
    
    Button_3 = Button(width/2, 500, 200, 50, "Quit", close_game)
    Button_3.display_button()
    
    highest_num = "-"
    scores_data = []
    f = open("scores.txt", "r")
    for line in f:
        record_data = int(line.rstrip())
        scores_data.append(record_data)
        highest_num = max(scores_data)
    f.close()
    font = createFont("VCR_OSD_MONO_1.001.ttf", 1)
    textFont(font)
    textSize(15)
    text("Highest score: " + str(highest_num), width/2, height/2-40)
    
    click = SoundFile(this, "506052__mellau__button-click-3.wav")
    
    if Button_1.mouse_interact() and mousePressed :
        click.play()
        click.amp(effect_volume)
        play_game()
        Background_sound.stop()
        Background_sound = SoundFile(this, music[1])
        Background_sound.loop()
        noCursor()
        current_function = "PlayScreen"
    
    
    if Button_2.mouse_interact() and mousePressed :
        click.play()
        click.amp(effect_volume)
        settings_game()
        current_function = "Settings"
    
    
    if Button_3.mouse_interact() and mousePressed :
        click.play()
        click.amp(effect_volume)
        Background_sound.stop()
        current_function = "QuitGame"
    

        
#THIS THE PLAY SCREEN SECTION

fade = 0

#stores multiple asteroids by coordinates
visible_ast = []
game_over = False
show_stars = []

class Star:
    #(self, gives image, startign ast_size, position x, position y)
    def __init__(self, star_x, star_y):
        self.star_x = star_x
        self.star_y = star_y
        self.max_length = 10
        self.twinkling = True
        self.twinkle_i = 1
        self.twinkling_velocity = random(0.5, 3.0)
        
    def twinkle(self):
        if self.twinkling:
            self.max_length += self.twinkle_i * self.twinkling_velocity
            if self.max_length >= 15 or self.max_length <= 5:
                #length goes down by one as twinkle effect if go beyond the range
                self.twinkle_i *= -1
                
    def stop_twinkle(self):
        self.twinkling = False
        
    def spawn_star(self):
        fill(255)
        ellipse(self.star_x, self.star_y, 5, 5)
        strokeWeight(2)
        #North Line
        line(self.star_x, self.star_y, self.star_x, self.star_y - self.max_length)
        #South Line
        line(self.star_x, self.star_y, self.star_x, self.star_y + self.max_length)  
        #West Line
        line(self.star_x, self.star_y, self.star_x - self.max_length, self.star_y)  
        #East Line
        line(self.star_x, self.star_y, self.star_x + self.max_length, self.star_y) 
        
def display_stars():
    global show_stars, game_over
    if game_over:
        for star in show_stars:
            star.stop_twinkle()
            star.spawn_star()
    
    if not game_over:
        for star in show_stars:
            star.twinkle()
            star.spawn_star()
            
class Asteroids:
    #(self, gives image, startign ast_size, position x, position y)
    def __init__(self, ast_size, ast_number, ast_x, ast_y, fade):
        self.ast_size = ast_size
        self.ast_number = ast_number
        self.ast_x = ast_x
        self.ast_y = ast_y
        self.ast_pic = None
        self.fade = fade

    def spawn_asteroid(self):
        asteroids = ["Asteroid_1.png", "Asteroid_2.png", "Asteroid_3.png", "Asteroid_4.png", "Asteroid_5.png"]
        if self.ast_size < 90:
            self.fade += 5.0 
            tint(255, int(self.fade))
        else:
            noTint()
        self.ast_pic = loadImage(asteroids[int(self.ast_number)])
        self.ast_pic.resize(0, int(self.ast_size))
        image(self.ast_pic, self.ast_x - int(self.ast_size)/2, self.ast_y - int(self.ast_size)/2)
        
    def interact_asteroid(self):
        if self.ast_size <= 500:
            num_x = self.ast_x - mouseX
            #multiply together to get a positive number when negative
            num_x = num_x * num_x
            #sq root number back to original value
            num_x = num_x ** .5
            num_y = self.ast_y - mouseY
            #multiply together to get a positive number when negative
            num_y = num_y * num_y
            #sq root number back to original value
            num_y = num_y ** .5
            #pythagorean theorem (x^2 + y^2 = r^2 ----> (x^2 + y^2)^1/2 = r)   
            r = ((num_x ** 2) + (num_y ** 2))**.5
            r = int(r)
            #ast_size is divided by 2 ( for max range) because other half goes out of circle radius
        else:
            self.ast_size = self.ast_size 
        return r < (self.ast_size/2)
    
    def grow(self, rate):
        global game_over, visible_ast, stars_out 
        if self.ast_size <= 500 and game_over == False:
            self.ast_size += rate
        else:
            #this calls all code for game_over
            game_over = True
            for ast in visible_ast:
                #keeps it at that size
                self.ast_size = self.ast_size

def play_game():
    global score, visible_ast, fade, game_over, Background_sound
    font = createFont("VCR_OSD_MONO_1.001.ttf", 1)
    textFont(font)
    img = loadImage("outer_space.png")
    background(img)
    noStroke()
    fill(0)
        
    ###MAKE SMALLEST AST GO BEHIND THE BIGGEST AST
            
    #this makes asteroid one at a time and can make multiple depending on score
    if score <= 10 and len(visible_ast) < 1:
        ast_size = 1
        ast_number = random(0,5)
        ast_x = random(0, width)
        ast_y = random(0, height)
        visible_ast.append(Asteroids(ast_size, ast_number, ast_x, ast_y, fade))
        #this applies to only a single asteroid
        for ast in visible_ast:
            #prevents ast from getting overlapped by return button
            if 0 <= ast_x <= 255 and height-110 <= ast_y <= height:
                visible_ast.remove(ast)
        
    if score > 10 and len(visible_ast) < 2:
        ast_size = 1
        ast_number = random(0,5)
        ast_x = random(0, width)
        ast_y = random(0, height)
        visible_ast.append(Asteroids(ast_size, ast_number, ast_x, ast_y, fade))
        #this applies to only a single asteroid
        for ast in visible_ast:
            if 0 <= ast_x <= 255 and height-110 <= ast_y <= height:
                visible_ast.remove(ast)
        
        
    if score > 25 and len(visible_ast) < 3:
        ast_size = 1
        ast_number = random(0,5)
        ast_x = random(0, width)
        ast_y = random(0, height)
        visible_ast.append(Asteroids(ast_size, ast_number, ast_x, ast_y, fade))
        #this applies to only a single asteroid
        for ast in visible_ast:
            if 0 <= ast_x <= 255 and height-110 <= ast_y <= height:
                visible_ast.remove(ast)
        
        
    if score > 40 and len(visible_ast) < 4:
        ast_size = 1
        ast_number = random(0,5)
        ast_x = random(0, width)
        ast_y = random(0, height)
        visible_ast.append(Asteroids(ast_size, ast_number, ast_x, ast_y, fade))
        #this applies to only a single asteroid
        for ast in visible_ast:
            if 0 <= ast_x <= 255 and height-110 <= ast_y <= height:
                visible_ast.remove(ast)
        
        
    if score > 65 and len(visible_ast) < 5:
        ast_size = 1
        ast_number = random(0,5)
        ast_x = random(0, width)
        ast_y = random(0, height)
        visible_ast.append(Asteroids(ast_size, ast_number, ast_x, ast_y, fade))
        #this applies to only a single asteroid
        for ast in visible_ast:
            if 0 <= ast_x <= 255 and height-110 <= ast_y <= height:
                visible_ast.remove(ast)
        
    # this applies for all asteroids    
    for ast in visible_ast:
        ast.spawn_asteroid()
        if score <= 10:
            ast.grow(1.0)
        elif score > 10:
            ast.grow(2.0)
        elif score > 25:
            ast.grow(4.0)
        elif score > 40:
            ast.grow(5.0)
        elif score > 65:
            ast.grow(6.0)
        elif score > 90:
            ast.grow(8.0)
            
    if game_over:
        Background_sound.stop()
        for ast in visible_ast:
            ast.spawn_asteroid()
        fill(175, 0, 0, 120)
        rect(0, 0, width, height)
        textAlign(CENTER, CENTER)
        fill(255, 0, 0)
        textSize(120)
        text("GAME OVER", width/2, height/2-40)
        textSize(20)
        text("Press 'r' to restart", width/2, height/2+40)
        MCursor = loadImage("Main_Cursor.png")
        MCursor.resize(70, 70)
        cursor(MCursor, 0, 0)

            
    Return_Menu()

    if not game_over:
        target_cursor(mouseX, mouseY)
        
    display_stars()
    
        
def mouseClicked():
    global visible_ast, score, fade, game_over, effect_volume, current_function
    if current_function == "PlayScreen":
        if game_over:
            return
        for ast in visible_ast:
            if ast.interact_asteroid():
                fade = 0
                explode = SoundFile(this, "322490__liamg_sfx__explosion-7d.wav")
                explode.play()
                explode.amp(effect_volume)
                score += 1
                visible_ast.remove(ast)
        if not (0 <= mouseX  <= 255 and height-110 <= mouseY <= height):
            fill(255)
            quad(mouseX - 2, mouseY  , mouseX + 2 , mouseY , width/2 + 50 , height , width/2 - 50 , height )
            
            
def startAgain():
    global score, ast_size, Background_sound, add_toSize, visible_ast, game_over
    #restarts the music
    #Background_sound.loop()
    score = 0
    visible_ast = []
    game_over = False
    
    
def keyPressed():
    global Background_sound, music, effect_volume
    #game resets back to 0 if 'r' key is pressed; score and diameter back to uno
    if key == "r":
        #added sound effects for a charm
        restart_effect = SoundFile(this, "258020__kodack__arcade-bleep-sound.wav")
        restart_effect.play()
        restart_effect.amp(effect_volume)
        Background_sound.stop()
        Background_sound = SoundFile(this, music[1])
        Background_sound.loop()
        f = open("scores.txt", "a")
        f.write(str(score) + "\n")
        f.close()
        startAgain()
        
        
#THIS IS THE SETTINGS SECTION (Adjust audio etc...)
    

lever_posX1 = 680
lever_posX2 = 680
lever_y1 = 270  
lever_y2 = 430
lever_width = 10
lever_height = 40
dragging1 = False
dragging2 = False

def settings_game():
    img = loadImage("MenuBackground.png")
    background(img)
    Return_Menu()
    textAlign(CENTER, CENTER)
    textSize(75)
    text("Settings", width/2, 100)
    textSize(30)
    text("Background Volume", width/2, height/2 - 140)
    text("Effects", width/2, height/2 + 20)
    line_lever(290, 300, 280)
    line_lever(450, 460, 440)
    

def line_lever(y_line, y1, y2):
    strokeWeight(3)
    line(300, y_line, 700, y_line)
    #creates the ticks
    for x in range(320, 681, 60):
        line (x, y1, x , y2)
    lever()

def mousePressed():
    global dragging1, dragging2, lever_posX1, lever_posX2, lever_width, lever_height, lever_y1, lever_y2
    # Check if the mouse is pressed within the lever's area
    if lever_posX1 - lever_width / 2 <= mouseX <= lever_posX1 + lever_width / 2 and lever_y1 <= mouseY <= lever_y1 + lever_height:
        dragging1 = True
    elif lever_posX2 - lever_width / 2 <= mouseX <= lever_posX2 + lever_width / 2 and lever_y2 <= mouseY <= lever_y2 + lever_height:
        dragging2 = True

def mouseReleased():
    global dragging1, dragging2
    dragging1 = False
    dragging2 = False

def mouseDragged():
    global lever_posX1, lever_posX2, dragging1, dragging2, Background_sound, background_volume, effect_volume
    tick_effect = SoundFile(this, "342200__christopherderp__videogame-menu-button-click.wav")
    if dragging1:
        temporary_posX1 = lever_posX1
        if 650 <= mouseX < width:
            lever_posX1 = 680
            background_volume = 1.0
        elif 590 <= mouseX < 650:
            lever_posX1 = 620
            background_volume = 0.83
        elif 530 <= mouseX < 590:
            lever_posX1 = 560
            background_volume = 0.66
        elif 470 <= mouseX < 530:
            lever_posX1 = 500
            background_volume = 0.49
        elif 410 <= mouseX < 470:
            lever_posX1 = 440
            background_volume = 0.32
        elif 350 <= mouseX < 410:
            lever_posX1 = 380
            background_volume = 0.15
        elif 0 <= mouseX < 350:
            lever_posX1 = 320
            background_volume = 0
        if temporary_posX1 != lever_posX1:
            tick_effect.play()
            tick_effect.amp(effect_volume)
        
    if dragging2:
        temporary_posX2 = lever_posX2
        if 650 <= mouseX < width:
            lever_posX2 = 680
            effect_volume = 1.0
        elif 590 <= mouseX < 650:
            lever_posX2 = 620
            effect_volume = 0.83
        elif 530 <= mouseX < 590:
            lever_posX2 = 560
            effect_volume = 0.66
        elif 470 <= mouseX < 530:
            lever_posX2 = 500
            effect_volume = 0.49
        elif 410 <= mouseX < 470:
            lever_posX2 = 440
            effect_volume = 0.32
        elif 350 <= mouseX < 410:
            lever_posX2 = 380
            effect_volume = 0.15
        elif 0 <= mouseX < 350:
            lever_posX2 = 320
            effect_volume = 0
        if temporary_posX2 != lever_posX2:
            tick_effect.play()
            tick_effect.amp(effect_volume)

def lever():
    global lever_posX1, lever_posX2, lever_width, lever_height, lever_y1, lever_y2
    strokeWeight(2)
    fill(108, 66, 193)
    rect(lever_posX1 - lever_width / 2, lever_y1, lever_width, lever_height)
    rect(lever_posX2 - lever_width / 2, lever_y2, lever_width, lever_height)

    
#THIS IS THE EXIT BUTTON
def close_game():
    exit()
    
#THIS IS A BACK BUTTON
def Return_Menu():
    global current_function, music, Background_sound, score, effect_volume
    font = createFont("VCR_OSD_MONO_1.001.ttf", 1)
    textFont(font)
    strokeWeight(2)
    ReturnBack = Button(135, height - 65, 200, 50, "Return", Menu_screen)
    #shows rectangle(button) for this line of button_name
    ReturnBack.display_button()
    if ReturnBack.mouse_interact() and mousePressed :
        if current_function == "PlayScreen":
            Background_sound.stop()
            Background_sound = SoundFile(this, music[0])
            Background_sound.loop()
            f = open("scores.txt", "a")
            f.write(str(score) + "\n")
            f.close()
        startAgain()
        current_function = "MenuScreen"
        click = SoundFile(this, "506052__mellau__button-click-3.wav")
        click.play()
        click.amp(effect_volume)
        MCursor = loadImage("Main_Cursor.png")
        MCursor.resize(70, 70)
        cursor(MCursor, 0, 0)

def draw():
    global current_function, Background_sound, background_volume, show_stars, game_over, MCursor
    #these draws out function that is initiated when users click a button
    Background_sound.amp(background_volume)
        
    if current_function == "MenuScreen":
        #this is what the program is currently displaying
        Menu_screen()
    if current_function == "PlayScreen":
        play_game()
        fill(255)
        textSize(20)
        text("Score: " +  str(score), 90, 40)
    if current_function == "Settings":
        settings_game()
    if current_function == "QuitGame":
        close_game()
    return

    

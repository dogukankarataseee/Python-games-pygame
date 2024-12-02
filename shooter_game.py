# Kütüphaneler 
from pygame import*
from random import randint # rastgele sayı oluşturan kütüphane

#  Arayüz işlemleri
win_width = 700             # genişlik
win_height = 500            # yükseklik
img_back = "galaxy.jpg"     # arka plan resmi
music_back = "space.ogg"    # fon müziği
music_fire = "fire.ogg"     # mermi sesi
display.set_caption("Shooter Game")                 # Başlık
window = display.set_mode((win_width,win_height))   # Pencere
background = transform.scale(image.load(img_back),(win_width,win_height)) # arkaplan

# Müzik işlemleri
mixer.init() # fonksiyonlar aktarılır
mixer.music.load(music_back)
mixer.music.play()
fire_sound = mixer.Sound(music_fire)

# font işlemleri
font.init()
font1 = font.Font(None,36)
font2 = font.Font(None,80)

# Oyun sonu yazıları
win = font2.render("YOU WIN !!!",True,(255,0,0))    # kırmızı renkte you win yazısı
lose = font2.render("YOU LOSE !!!",True,(0,0,255))  # mavi renkte you lose yazısı


# SINIFLAR
# main class = ana sınıf kavramı = diğer sınıflar buradan özellik alacaklar
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self) # resimlerin özelliklerini çalıştırabilmek için hazır sınıf

        self.speed = player_speed
        self.image = transform.scale(image.load(player_image),(size_y,size_y)) 

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # pencereye gelen resimleri birleştirmeye yarar
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

# oyuncu = alttaki gemi sınıfı oluşturuldu
class Player(GameSprite):
    # geminin sağa ve sola hareketi için kullanılacak fonksiyon
    def update(self):
        keys = key.get_pressed() # tuşlar ile alakalı bir nesne 
        # sola gitme işlemi
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        # sağa gitme işlemi
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    # ATEŞ ETME FONKSİYONU
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet) # her bir mermi gruba dahil edilir
        

# düşman = yukarıdan gelen gemiler
class Enemy(GameSprite):
    # geminin rastgele ve otomatik bir şekilde  oluşması ve aşagı inmesi
    def update(self):
        self.rect.y += self.speed # otomatik bir şekilde aşagı inme işlemi
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80) # 80 ile 620 arasında bir sayı
            self.rect.y = 0 # başlangıç ayarı
            lost = lost + 1 # lost += 1 ikisi de aynı işlem
            

# mermi sınıfı = yukarı hareket sağlayacak
class Bullet(GameSprite):
    # mermi atış işlemi
    def update(self):
        self.rect.y += self.speed
        
        # ekranın üstüne gelince kaybolsun
        if  self.rect.y < 0:
            self.kill() # ust noktaya gelince mermi kaybolsun

# karakter ekleme işlemleri
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
# gemi  nesnesi
ship = Player(img_hero,5,400,80,100,10)

# mermi grubu uluşturulması
bullets = sprite.Group()

# uzaylı nesnesi
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5)) # tek nesne
    monsters.add(monster) # nesnelerin hepsini gruba attık


# Global Değişkenler
finish = False  # oyun bitti değişkeni
run = True      # oyunu başlatan değişken
score = 0       # oyun puanı
lost = 0        # kaçırılan uzaylılar
music_playing = True  # müzik ilp başta çaldığı içinn true yaptık 

# OYUN DÖNGÜSÜ = FONKSİYONEL İŞLEMLER
while run:
    #Kapat düğmesi
    for e in event.get():
        if e.type == QUIT:
           run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE or e.key == K_x:
                fire_sound.play() # ateş etme efekti çalıştı
                ship.fire() # her space sonrasında mermi oluşur
            # arkaplan müziğini kapatma ve açma işlemi
            elif e.key == K_m:
                if music_playing == True:
                    mixer.music.pause()
                else:
                    mixer.music.unpause()
                music_playing = not music_playing
            # yeniden başlatma tuşu 
            elif e.key == K_r:
                finish = False
                score = 0
                lost = 0
                # ekrandakş mermileri temizledik
                for b in bullets:
                    b.kill()
                # ekrandaki uzaylıları temizler    
                for m in monsters:
                    m.kill()
                # uzaylıları yeniden oluşturduk.
                for i in range(1,6):
                    monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5)) # tek nesne
                    monsters.add(monster) # nesnelerin hepsini gruba attık

        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 3: # sağ click
                fire_sound.play() # ateş etme efekti çalıştı
                ship.fire() # her space sonrasında mermi oluşur
        
    
    if not finish:
        window.blit(background,(0,0))

        # ekrana metin yazdırma işlemi
        # score
        text = font1.render("Puan: " +str(score),1,(255,0,0)) # kırmızı renkli score yazısı
        window.blit(text,(10,20)) # sol ust köşe
        # lost
        text_lose = font1.render("Kayıp: " +str(lost),1,(255,0,0)) # kırmızı renkli score yazısı
        window.blit(text_lose,(10,50)) # sol ust köşe

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        
        # karakter birleşme durumları
        # mermiler ile uzaylıların birleşme kontrolu
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1 # birleşme durumu sonucunda puan gelir
            monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5)) # tek nesne
            monsters.add(monster) # nesnelerin hepsini gruba attık 
        
        # kaybetme durumu
        if sprite.spritecollide(ship,monsters,False) or lost >= 10:
            finish = True
            window.blit(lose,(200,200))
        
        # kazanma durumu
        if score >=10:
            finish = True
            window.blit(win,(200,200))
            
        display.update()
    
    time.delay(50) # fps yedek fonksiyon 0.05 saniye gecikme meydana gelir 

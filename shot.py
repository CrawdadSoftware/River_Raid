import cores

class Shot:
    def __init__(self, win, shoting, x, y):
        self.x = x  # Pozycja strzału w osi X
        self.y = y  # Pozycja strzału w osi Y
        self.w = 5  # Szerokość strzału
        self.h = 15  # Wysokość strzału
        self.shoting = shoting  # Stan strzelania
        self.win = win  # Okno gry
        self.cor = cores.cor  # Kolory obiektów

    def show(self, planex, planey):
        # Jeśli strzał jest aktywny
        if self.shoting:
            self.shoting = False  # Dezaktywacja strzelania
            # Resetowanie pozycji strzału, jeśli jest poza ekranem
            if self.y <= 0:
                self.x = planex  # Ustawienie pozycji X strzału na pozycję samolotu
                self.y = planey  # Ustawienie pozycji Y strzału na pozycję samolotu
        # Przesuwanie strzału w górę ekranu
        if self.y > -self.h:
            self.y -= 6
        # Rysowanie strzału na ekranie
        self.win.fill(self.cor[13], rect=[self.x, self.y, self.w, self.h])

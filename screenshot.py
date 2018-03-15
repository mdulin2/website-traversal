from ghost import Ghost
ghost = Ghost(wait_timeout=4)
ghost.open('http://www.google.com')
ghost.capture_to('screen_shot.png')

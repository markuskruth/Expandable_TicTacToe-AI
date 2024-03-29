import keyboard,time,random,copy
import concurrent.futures
import multiprocessing

size = 780

aloittaja = 1 #0=pelaaja, 1=AI
koko = 6
win_condition = 4
depth = 3

weight = 3
synti = 5


#0 = tyhjä, 1 = pelaaja, 2 = AI
lauta = [[]]
for i in range(koko):
	for j in range(koko):
		lauta[i].append(0)

	if i != koko-1:
		lauta.append([])


vuoro = aloittaja

def display(board):
	global vuoro

	pygame.event.get()
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	mouse_board_x = int(mouse[0]/int(780/koko))
	mouse_board_y = int(mouse[1]/int(780/koko))

	win.fill((255,255,255))

	over = game_over(board)

	viivaväri = (255,229,204)
	for i in range(koko):
		pygame.draw.line(win,viivaväri,(0,i*int(780/koko)),(780,i*int(780/koko)),5)
		pygame.draw.line(win,viivaväri,(i*int(780/koko),0),(i*int(780/koko),780),5)

	if not over:
		pygame.draw.rect(win,(240,240,240),(mouse_board_x*int(780/koko)+2, mouse_board_y*int(780/koko)+2, int(780/koko)-4, int(780/koko)-4))


	n = 10
	for i in range(len(board)):
		for j in range(len(board)):
			if board[i][j] == 1:
				#kaunista
				pygame.draw.line(win,(0,0,0),(j*int(780/koko)+5,i*int(780/koko)+n),((j+1)*int(780/koko)-5,(i+1)*int(780/koko)-n),15)
				pygame.draw.line(win,(0,0,0),(j*int(780/koko)+5,(i+1)*int(780/koko)-n),((j+1)*int(780/koko)-10,i*int(780/koko)+n),15)

			elif board[i][j] == 2:
				pygame.draw.circle(win,(0,0,0),(int(j*int(780/koko)+(int(780/koko)/2)),int(i*int(780/koko)+(int(780/koko)/2))),int(360/koko),12)



	väri = (200,200,100)
	fontSize = int(size/4)
	font = pygame.font.SysFont("bookshelf", fontSize)
	font2 = pygame.font.SysFont("bookshelf", int(fontSize/1.5))
	ai_winText = font.render("AI WINS", 1, väri)
	player_winText = font.render("PLAYER WINS", 1, väri)
	draw_text = font.render("DRAW", 1, väri)
	restart_text = font2.render("RESTART",1,(128,255,0))

	if over:
		kumpi = voitoncheck(board)
		if kumpi == 1000:
			pygame.draw.rect(win,(0,0,0),(size/7-size/50, size/2.5, fontSize*3, 150))
			win.blit(ai_winText,(size/7, size/2.4))

		elif kumpi == -1000:
			pygame.draw.rect(win,(0,0,0),(size/7-size/50, size/2.5, fontSize*3, 150))
			win.blit(player_winText,(size/7, size/2.4))

		else:
			pygame.draw.rect(win,(0,0,0),(size/5-size/50, size/2.5, fontSize*2.5, 150))
			win.blit(draw_text,(size/5+size/50, size/2.4))

		pygame.draw.rect(win,(0,0,0),(size/5.2, size/1.3, fontSize*2.45, fontSize/2))

		if 150<mouse[0]<150+483 and 600<mouse[1]<600+90:
			pygame.draw.rect(win,(50,50,50),(size/5.2, size/1.3, fontSize*2.45, fontSize/2))

			if click[0] == 1:
				time.sleep(0.2)

				board = [[]]
				for i in range(koko):
					for j in range(koko):
						board[i].append(0)

					if i != koko-1:
						board.append([])

				vuoro = aloittaja

		win.blit(restart_text,(size/4.2,size/1.28))


	pygame.display.update()

def player_move(board):
	global vuoro

	pygame.event.get()
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	mouse_board_x = int(mouse[0]/int(780/koko))
	mouse_board_y = int(mouse[1]/int(780/koko))

	if click[0] == 1:
		if board[mouse_board_y][mouse_board_x] == 0:
			pygame.draw.rect(win,(255,255,230),(mouse_board_x*int(780/koko)+2, mouse_board_y*int(780/koko)+2, int(780/koko)-4, int(780/koko)-4))
			pygame.display.update()

			time.sleep(0.2)

			if vuoro%2 == 0:
				board[mouse_board_y][mouse_board_x] = 1
			else:
				board[mouse_board_y][mouse_board_x] = 2
			vuoro += 1


def vaakaVoitto(i,board):
	global weight
	pisteet = 0
	last_p = 0
	max_pisteet_p_final = 0
	max_pisteet_ai_final = 0
	for j in range(len(board)):
		if board[i][j] != 0: #jos tarkastellaan kohtaa jossa on pelaajan tai AI:n merkki
			if board[i][j] == last_p:
				pisteet += 1
			else:
				if last_p == 1:
					max_pisteet_p_final += pisteet**weight-1
				elif last_p == 2:
					max_pisteet_ai_final += pisteet**weight-1
				last_p = board[i][j]
				pisteet = 1
		else:
			if last_p == 1:
				max_pisteet_p_final += pisteet**weight-1
			elif last_p == 2:
				max_pisteet_ai_final += pisteet**weight-1
			pisteet = 0
			last_p = 0

		if pisteet == win_condition:
			if last_p == 1:
				return -1000
			else:
				return 1000

	if last_p == 1:
		max_pisteet_p_final += pisteet**weight-1
	elif last_p == 2:
		max_pisteet_ai_final += pisteet**weight-1


	return max_pisteet_ai_final - max_pisteet_p_final

def pystyVoitto(i,board):
	global weight
	pisteet = 0
	last_p = 0
	max_pisteet_p_final = 0
	max_pisteet_ai_final = 0
	for j in range(len(board)):
		if board[j][i] != 0:
			if board[j][i] == last_p:
				pisteet += 1
			else:
				if last_p == 1:
					max_pisteet_p_final += pisteet**weight-1
				elif last_p == 2:
					max_pisteet_ai_final += pisteet**weight-1
				last_p = board[j][i]
				pisteet = 1
		else:
			if last_p == 1:
				max_pisteet_p_final += pisteet**weight-1
			elif last_p == 2:
				max_pisteet_ai_final += pisteet**weight-1
			pisteet = 0
			last_p = 0

		if pisteet == win_condition:
			if last_p == 1:
				return -1000
			else:
				return 1000

	if last_p == 1:
		max_pisteet_p_final += pisteet**weight-1
	elif last_p == 2:
		max_pisteet_ai_final += pisteet**weight-1

	return max_pisteet_ai_final - max_pisteet_p_final

#returnaa -10 jos pelaaja voittaa, 10 jos AI voittaa, 0 muuten
def voitoncheck(board):
	global weight

	move_eval = 0
	for i in range(len(board)):

		#jos jompikumpi voittaa vaakariveillä
		tulos = vaakaVoitto(i,board)
		if abs(tulos) == 1000:
			return tulos

		#print("Vaakatulos:",tulos)
		move_eval += tulos



		#jos jompikumpi voittaa pystyriveillä
		tulos = pystyVoitto(i,board)
		if abs(tulos) == 1000:
			return tulos

		#print("Pystytulos:",tulos)
		move_eval += tulos



	#jos jompikumpi voittaa vinoriveillä
	for i in range(koko):

		#lähtee vasenta reunaa alaspäin tutkimaan oikealle alas lähteviä vinosuoria
		max_pisteet_p = 0
		max_pisteet_ai = 0
		pisteet = 0
		max_pisteet = 0
		last_p = 0
		for k in range(koko):
			if k+i < koko and board[k+i][k] != 0:
				if board[k+i][k] == last_p:
					pisteet += 1
				else:
					if last_p == 1:
						max_pisteet_p += pisteet**weight-1
					elif last_p == 2:
						max_pisteet_ai += pisteet**weight-1
					last_p = board[k+i][k]
					pisteet = 1
			else:
				if last_p == 1:
					max_pisteet_p += pisteet**weight-1
				elif last_p == 2:
					max_pisteet_ai += pisteet**weight-1
				pisteet = 0
				last_p = 0

			if pisteet == win_condition:
				if last_p == 1:
					return -1000
				else:
					return 1000

		if last_p == 1:
			max_pisteet_p += pisteet**weight-1
		elif last_p == 2:
			max_pisteet_ai += pisteet**weight-1

		max_pisteet = max_pisteet_ai - max_pisteet_p
		move_eval += max_pisteet


		#lähtee vasenta reunaa ylöspäin tutkimaan oikealle ylös lähteviä vinosuoria
		max_pisteet_p = 0
		max_pisteet_ai = 0
		max_pisteet = 0
		pisteet = 0
		last_p = 0
		for k in range(koko):
			if k+1+i <= koko and board[-(k+1+i)][k] != 0:
				if board[-(k+1+i)][k] == last_p:
					pisteet += 1
						
				else:
					if last_p == 1:
						max_pisteet_p += pisteet**weight-1
					elif last_p == 2:
						max_pisteet_ai += pisteet**weight-1
					last_p = board[-(k+1+i)][k]
					pisteet = 1
			else:
				if last_p == 1:
					max_pisteet_p += pisteet**weight-1
				elif last_p == 2:
					max_pisteet_ai += pisteet**weight-1
				pisteet = 0
				last_p = 0

			if pisteet == win_condition:
				if last_p == 1:
					return -1000
				else:
					return 1000

		if last_p == 1:
			max_pisteet_p += pisteet**weight-1
		elif last_p == 2:
			max_pisteet_ai += pisteet**weight-1

		max_pisteet = max_pisteet_ai - max_pisteet_p
		move_eval += max_pisteet


		#lähtee yläreunaa oikealle päin tutkimaan oikealle alas lähteviä vinosuoria
		max_pisteet = 0
		max_pisteet_p = 0
		max_pisteet_ai = 0
		pisteet = 0
		last_p = 0
		for k in range(koko-i):
			if k+i != k:
				if board[k][k+i] != 0:
					if board[k][k+i] == last_p:
						pisteet += 1
					else:
						if last_p == 1:
							max_pisteet_p += pisteet**weight-1
						elif last_p == 2:
							max_pisteet_ai += pisteet**weight-1
						last_p = board[k][k+i]
						pisteet = 1
				else:
					if last_p == 1:
						max_pisteet_p += pisteet**weight-1
					elif last_p == 2:
						max_pisteet_ai += pisteet**weight-1
					pisteet = 0
					last_p = 0

				if pisteet == win_condition:
					if last_p == 1:
						return -1000
					else:
						return 1000


		if last_p == 1:
			max_pisteet_p += pisteet**weight-1
		elif last_p == 2:
			max_pisteet_ai += pisteet**weight-1

		max_pisteet = max_pisteet_ai - max_pisteet_p
		move_eval += max_pisteet


		#lähtee alareunaa oikealle päin tutkimaan oikealle ylös lähteviä vinosuoria
		max_pisteet_p = 0
		max_pisteet_ai = 0
		max_pisteet = 0
		pisteet = 0
		last_p = 0
		for k in range(koko-i):
			if k+i != k:
				if board[-(k+1)][k+i] != 0:
					if board[-(k+1)][k+i] == last_p:
						pisteet += 1
						
					else:
						if last_p == 1:
							max_pisteet_p += pisteet**weight-1
						elif last_p == 2:
							max_pisteet_ai += pisteet**weight-1
						last_p = board[-(k+1)][k+i]
						pisteet = 1
				else:
					if last_p == 1:
						max_pisteet_p += pisteet**weight-1
					elif last_p == 2:
						max_pisteet_ai += pisteet**weight-1
					pisteet = 0
					last_p = 0

				if pisteet == win_condition:
					if last_p == 1:
						return -1000
					else:
						return 1000

		if last_p == 1:
			max_pisteet_p += pisteet**weight-1
		elif last_p == 2:
			max_pisteet_ai += pisteet**weight-1

		max_pisteet = max_pisteet_ai - max_pisteet_p
		move_eval += max_pisteet

	return move_eval

def game_over(board):
	done = True
	for i in range(len(board)):
		if 0 in board[i]:
			done = False

	if abs(voitoncheck(board)) == 1000 or done:
		return True

	return False




def legal_moves(board):
	moves = []

	for i in range(len(board)):
		for j in range(len(board)):
			if board[i][j] == 0:
				moves.append([i,j])

	return moves


def minimax(board,isMax,depth,alpha,beta):
	global depthcounter,synti

	eval = voitoncheck(board)

	#jos pelaaja on voittanut
	if eval == -1000:
		return eval

	#jos AI on voittanut
	if eval == 1000:
		return eval

	kaikki_movet = legal_moves(board)

	#jos tasapeli
	if len(kaikki_movet) == 0:
		return 0

	if depth == depthcounter:
		return eval


	if isMax:
		maksimoi = -9999

		for move in kaikki_movet: #käydään läpi kaikki mahdolliset siirrot
			if good_move(board,move):
				board[move[0]][move[1]] = 2 #tehdään siirto laudalla

				maksimoi = max(maksimoi, minimax(board,False,depth,alpha,beta))
				alpha = max(alpha,maksimoi)

				board[move[0]][move[1]] = 0 #undoataan tehty move

				# Alpha Beta Pruning
				if beta <= alpha+synti:
					break


		return maksimoi


	else:
		minimoi = 9999

		for move in kaikki_movet:
			if good_move(board,move):
				board[move[0]][move[1]] = 1 #tehdään siirto laudalla

				minimoi = min(minimoi,minimax(board,True,depth+1,alpha,beta))
				beta = min(beta,minimoi)

				board[move[0]][move[1]] = 0

				if beta <= alpha+synti:
					break

		return minimoi


def subEngine(board,move):
	global depthcounter
	if good_move(board,move):
		depthcounter = depth
	else:
		depthcounter = depth-0

	boarderi = copy.deepcopy(board)

	boarderi[move[0]][move[1]] = 2
	eval = minimax(boarderi,False,0,-999,999)
	boarderi[move[0]][move[1]] = 0

	return eval,move


def engine(board):
	global depthcounter
	looppi = 0
	parhaat_movet = []

	paras_move_eval = -9999
	paras_move = [0,0]

	kaikki_movet = legal_moves(board)


	print("LEN:",len(kaikki_movet))
	a = 0
	results = []

	with concurrent.futures.ProcessPoolExecutor() as executor:
		results = [executor.submit(subEngine,board,move) for move in kaikki_movet]

		for f in concurrent.futures.as_completed(results):
			print(f.result())
			siirto = f.result()[1]
			eval = f.result()[0]

			if eval >= paras_move_eval:
				paras_move = siirto
				paras_move_eval = eval

	#for move in kaikki_movet:
	#	eval,move = subEngine(board,move)
#
#		if eval >= paras_move_eval:
#			paras_move = move
#			paras_move_eval = eval


	print("Tämän moven evaluation on:",paras_move_eval)
	if paras_move_eval == 1000:
		print("haha wtf ez why so idiot????")

	return paras_move


def good_move(board,move):
	paikat = []

	for i in range(koko):
		for j in range(koko):
			if board[i][j] != 0:
				paikat.append([i,j])

	y = move[0]
	x = move[1]

	for paikka in paikat:
		#ylös
		if y-1 > 0 and paikka == [y-1,x]:
			return True

		#alas
		if y+1 < koko and paikka == [y+1,x]:
			return True

		#vasen
		if x-1 > 0 and paikka == [y,x-1]:
			return True

		#oikea
		if x+1 < koko and paikka == [y,x+1]:
			return True

		#yläoikea
		if x+1 < koko and y-1 > 0 and paikka == [y-1,x+1]:
			return True

		#ylävasen
		if x-1 > 0 and y-1 > 0 and paikka == [y-1,x-1]:
			return True

		#alaoikea
		if x+1 < koko and y+1 < koko and paikka == [y+1,x+1]:
			return True

		#alavasen
		if x-1 > 0 and y+1 < koko and paikka == [y+1,x-1]:
			return True

	return False





testi = [[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0]]

if __name__ == "__main__":
	import pygame
	pygame.init()
	win = pygame.display.set_mode((size,size))
	multiprocessing.freeze_support()
	first_move = True
	while True:
		if keyboard.is_pressed("q"):
			time.sleep(0.2)
			pygame.display.quit()
			pygame.quit()
			exit()

		tila = game_over(lauta)

		if vuoro%2 == 0:
			if tila == False:
				player_move(lauta)

		else:
			if tila == False:
				if first_move and vuoro == 1:
					siirto = [round(koko/2),round(koko/2)]

				else:
					alkuAika = time.time()
					siirto = engine(lauta)
					loppuAika = time.time()
					print("Runtime:",str(round(loppuAika - alkuAika,2))+"s")
				lauta[siirto[0]][siirto[1]] = 2
				vuoro += 1

		display(lauta)
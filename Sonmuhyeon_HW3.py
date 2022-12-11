
import random
import time
import sys
from cs1graphics import *

### 1. FACES and SUITS list 작성
FACES = list(range(2, 11)) + ['Jack', 'Queen', 'King', 'Ace' ]
SUITS = [ 'Clubs', 'Diamonds', 'Hearts', 'Spades' ]

CARD_SIZE = (40, 80)
RADIUS = 3


class Card(object):
  """A card has a face and suit."""
  def __init__(self, face, suit):
    ## 2.  assert를 사용해서 face와 suit가 FACES와 SUITS에서만 뽑히도록 하고, face suit attribute 작성
    
    assert(face in FACES and suit in SUITS)
    self.face = face
    self.suit = suit
    self.graphics = None
    

  def __str__(self):
    article = "a "
    if self.face in [8, "Ace"]:
        article = "an "
    ### 3.  an 8 of diamond, a Queen of spade 같은 꼴의 str 리턴

    return article + str(self.face) + " of " + self.suit

  def value(self):
    """Returns the face value of the card."""
    ### 4. J Q K는 10, A는 11 리턴
    if type(self.face) == int:
      return self.face
    if self.face == "Ace":
      return 11
    return 10

# --------------------------------------------------------------------

def create_clubs(symbol):
  """Create clubs on layer symbol."""
  circle1 = Circle(RADIUS, Point(0, -RADIUS))
  circle1.setFillColor('black')
  circle1.setBorderWidth(0)
  symbol.add(circle1)
            
  circle2 = Circle(RADIUS, Point(-RADIUS, 0))
  circle2.setFillColor('black')
  circle2.setBorderWidth(0)
  symbol.add(circle2)
    
  circle3 = Circle(RADIUS, Point(RADIUS, 0))
  circle3.setFillColor('black')
  circle3.setBorderWidth(0)
  symbol.add(circle3)
  
  triangle = Polygon(Point(0, 0), 
                     Point(-RADIUS*2, RADIUS*3), 
                     Point(RADIUS*2, RADIUS*3))
  triangle.setFillColor('black')
  triangle.setBorderWidth(0)
  symbol.add(triangle)
  
def create_diamonds(symbol):
  ## 5. create diamonds
  diamond = Square(3 * RADIUS)
  diamond.setFillColor('red')
  diamond.setBorderWidth(0)
  diamond.rotate(30)
  symbol.add(diamond)
        
def create_hearts(symbol):
  ## 6. create hearts
  circle1 = Circle(RADIUS, Point(-RADIUS, -RADIUS))
  circle1.setFillColor('red')
  circle1.setBorderWidth(0)
  symbol.add(circle1)
            
  circle2 = Circle(RADIUS, Point(RADIUS, -RADIUS))
  circle2.setFillColor('red')
  circle2.setBorderWidth(1)
  symbol.add(circle2)
            
  triangle = Polygon(Point(-RADIUS*2, -RADIUS), 
                     Point(RADIUS*2, -RADIUS), 
                     Point(0, RADIUS*2))
  triangle.setFillColor('red')
  triangle.setBorderWidth(0)
  symbol.add(triangle)

def create_spades(symbol):
    
  ## 7. create spades
  circle1 = Circle(RADIUS, Point(-RADIUS, RADIUS))
  circle1.setFillColor('black')
  circle1.setBorderWidth(0)
  symbol.add(circle1)
            
  circle2 = Circle(RADIUS, Point(RADIUS, RADIUS))
  circle2.setFillColor('black')
  circle2.setBorderWidth(0)
  symbol.add(circle2)
  
  triangle1 = Polygon(Point(-RADIUS*3, RADIUS), 
                      Point(RADIUS*3, RADIUS), 
                      Point(0, -RADIUS*3))
  triangle1.setFillColor('black')
  triangle1.setBorderWidth(0)
  symbol.add(triangle1)
  
  triangle2 = Polygon(Point(0, 0), 
                      Point(-RADIUS*3, RADIUS*4), 
                      Point(RADIUS*3, RADIUS*4))
  triangle2.setFillColor('black')
  triangle2.setBorderWidth(0)
  symbol.add(triangle2)

# --------------------------------------------------------------------

class CardGraphics(object):
  """Graphical representation of a card."""
  
  def __init__(self, card, hidden = False):
    self.l = Layer()

    # background card
    self.bg = Rectangle(CARD_SIZE[0], CARD_SIZE[1])
    if hidden:
      self.bg.setDepth(0)
      self.bg.setFillColor('gray')
    else:
      self.bg.setDepth(100)
      self.bg.setFillColor('white')
    self.l.add(self.bg)
    
# 8. symbol for center, card suit에 맞는 symbol layer을 만들어서 self.l에 add하기
    symbol = Layer()
    if card.suit == "Diamonds":
      create_diamonds(symbol)
    elif card.suit == "Hearts":
      create_hearts(symbol)
    elif card.suit == "Clubs":
      create_clubs(symbol)
    else:
      create_spades(symbol)
    self.l.add(symbol)
    
    # text for left-top and right-bottom
    if card.suit in ['Diamonds', 'Hearts']:
      color = 'red'
    else:
      color = 'black'

    if type(card.face) == int:
      num = str(card.face)
    else:
      num = card.face[0]
    
    # left-top text
    lt_num = Text()
    lt_num.setMessage(num)
    lt_num.setFontColor(color)
    lt_num_dim = lt_num.getDimensions()
    lt_num.moveTo(-CARD_SIZE[0]/2 + lt_num_dim[0]/2, 
                   -CARD_SIZE[1]/2 + lt_num_dim[1]/2)
    self.l.add(lt_num)
        
    # 9. right-bottom text 작성하시오
    rb_num = Text()
    rb_num.setMessage(num)
    rb_num.setFontColor(color)
    rb_num_dim = lt_num.getDimensions()
    rb_num.moveTo(CARD_SIZE[0]/2 - rb_num_dim[0]/2, 
                  CARD_SIZE[1]/2 - rb_num_dim[1]/2)
    self.l.add(rb_num)

  def show(self):
    self.bg.setDepth(100)
    self.bg.setFillColor('white')
# --------------------------------------------------------------------

class Deck(object):
  """A deck of cards."""
  def __init__(self):
    """Create a deck of 52 cards and shuffle them."""
    ### 10. 52개의 카드를 만들고 random module을 사용, 섞으시오
    
    self.cards = []
    for suit in SUITS:
      for face in FACES:
        self.cards.append(Card(face, suit))
    random.shuffle(self.cards)

  def draw(self):
    """Draw the top card from the deck."""
    return self.cards.pop()
    
# --------------------------------------------------------------------

class Hand(object):                    ########## 테이블에서 보여지는 카드들 (player 별로)
  """A hand of cards displayed on a table."""

  def __init__(self, x, y, canvas):
    """Create an empty hand displayed at indicated position on canvas."""
    self.canvas = canvas
    self.x = x
    self.y = y
    self.graphics = []
    self.hand = []

  def add(self, card, hidden = False):
    """Add a new card to the hand."""
    self.hand.append(card)
    gr = CardGraphics(card, hidden)
    gr.l.moveTo(self.x + CARD_SIZE[0] * 2 * len(self.graphics), self.y)
    self.canvas.add(gr.l)
    self.graphics.append(gr)
    
  def clear(self):
    """Make hand empty."""
    
    
    for item in self.graphics:
      self.canvas.remove(item.l)
    self.graphics = []
    self.hand = []

  def show(self):
    """Make all cards visible."""
    ## 12. 모든 그래픽을 보이게 하시오
    for gr in self.graphics:
      gr.show()

  def value(self):
    """Return value of the hand."""
    ## 13. total value를 반환하시오
    value = 0
    for card in self.hand:
      value += card.value()
    return value

# --------------------------------------------------------------------

class Table(object):
  """A graphical Blackjack table for playing Blackjack."""
  
  def __init__(self):
    self.canvas = Canvas(600, 400, 'dark green', 'Black Jack 101')
    ## 14.
    ## self.player 이름의 Hand를 CARD_SIZE[0], CARD_SIZE[1]에 만드시오
    ## self.dealer 이름의 Hand를 CARD_SIZE[0], 3 * CARD_SIZE[1]에 만드시오
    self.player = Hand(CARD_SIZE[0], CARD_SIZE[1], self.canvas)
    self.dealer = Hand(CARD_SIZE[0], 3 * CARD_SIZE[1], self.canvas)

    
    
    
    
    self.score = [ Text(), Text() ]
    for i in range(2):
      self.score[i].setFontColor('white')
      self.score[i].setFontSize(20)
      self.score[i].moveTo(self.canvas.getWidth() - CARD_SIZE[0], CARD_SIZE[1])
      self.canvas.add(self.score[i])
    self.score[1].move(0, 2 * CARD_SIZE[1])

    
    
    
    self.message = Text()
    self.message.setFontColor('red')
    self.message.setFontSize(20)
    dim = self.message.getDimensions()
    self.message.moveTo(self.canvas.getWidth() / 2 - dim[0] / 2, 
                        self.canvas.getHeight() - 80)
    self.canvas.add(self.message)

    self.question = Text()
    self.question.setFontColor('white')
    self.question.setFontSize(20)
    dim = self.question.getDimensions()
    self.question.moveTo(self.canvas.getWidth() / 2 - dim[0] / 2, 
                        self.canvas.getHeight() - 40)
    self.canvas.add(self.question)

  def clear(self):
    """Clear everything on the table."""
    ## 15. player, dealer hand clear하고, message, question, score를 setMessage("") method 적용
        
    self.player.clear()
    self.dealer.clear()
    self.message.setMessage("")
    self.question.setMessage("")
    for i in range(2):
      self.score[i].setMessage("")

  def set_score(self, which, text):
    ## 16. score[which]에 text를 setmessage하시오
    self.score[which].setMessage(text)
    
  def show_message(self, text):
    ## 17. message에 text를 setmessage하시오
    self.message.setMessage(text)

  def ask(self, prompt):
    ## propmpt를 띄우고, user의 반응에 따라 action
    self.question.setMessage(prompt)
    while True:
      e = self.canvas.wait()
      d = e.getDescription()
      if d == "canvas close":
        sys.exit(1)
      if d == "keyboard":
        key = e.getKey() 
        if key == 'y':
          self.question.setMessage("")
          return True
        if key == 'n':
          self.question.setMessage("")
          return False
  
  def close(self):
    """Close the table to end playing."""
    self.canvas.close()
    
# --------------------------------------------------------------------

def blackjack(table):
  """Play one round of Blackjack.
  Returns 1 if player wins, -1 if dealer wins, and 0 for a tie."""
  ##################### 블랙잭 한번의 라운드, player가 이기면 1을 반환, 딜러가 이기면 -1, 비기면 0 반환


  deck = Deck()
   # 18.
  # player의 hand에 한장 추가, dealer에 한장 추가 (hidden)
  # player의 hand에 한장 추가, dealer에 한장 추가
  # player의 점수를 set_score하시오    

  table.player.add(deck.draw())
  table.dealer.add(deck.draw(), True) 
  time.sleep(1)
  table.player.add(deck.draw())
  table.dealer.add(deck.draw())
  table.set_score(0, str(table.player.value()))


  # 19.
  # player's turn to draw cards
  # 플레이어의 total value가 21보다 작으면 "Would you like another card?" 을 물어보고, n이면 딜러 턴으로 넘어가고 
  # y이면 한장 더 주기
  # 플레이어의 score를 set해줘야함 
  while table.player.value() < 21:
    if not table.ask("Would you like another card?"):
      break
    table.player.add(deck.draw())
    table.set_score(0, str(table.player.value()))
    
    
  # 플레이어의 카드값이 21보다 크면 "You went over 21! You lost!"를 show하고 경기 끝  
  # 플레이어가 카드를 더이상 받지 않으면, dealer의 hidden card를 보여주고 dealer의 score를 set 함
  # dealer의 value가 17보다 작으면 더 뽑고, score를 set 해줌

  if table.player.value() > 21:
    table.show_message("You went over 21! You lost!")
    return -1


  table.dealer.show()
  table.set_score(1, str(table.dealer.value()))
  while table.dealer.value() < 17:
    time.sleep(2)
    table.dealer.add(deck.draw())
    table.set_score(1, str(table.dealer.value()))
    
    
  # 20.
  # player의 total 점수와, dealer의 total 점수를 set 해주고 
  # "your total is 13"
  # "The dealer's total is 20"
  # 플레이어와 딜러의 점수에 따라, 
  # "You win!" set하고 1 반환 혹은
  # "The dealer went over 21! You win!" set하고 1 반환 혹은
  # "You lost" set하고 -1 반환 혹은
  # "You have a tie" 를 set하고, 0 반환
  player_total = table.player.value()
  dealer_total = table.dealer.value()

  if dealer_total > 21:
    Msg = "The dealer went over 21! You win!"
    result = 1
  elif player_total > dealer_total:
    Msg = "You win!"
    result = 1
  elif player_total < dealer_total:
    Msg = "You lost!"
    result = -1
  else:
    Msg = "You have a tie!"
    result = 0

  table.show_message(Msg)
  return result

# --------------------------------------------------------------------

def game_loop():
  table = Table()
  while True:
    blackjack(table)    
    if not table.ask("Another round?"):
      break
    table.clear()
  table.close()

game_loop()
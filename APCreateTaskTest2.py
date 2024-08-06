#Random Stuff I have to include
from cmu_graphics import *
import random

print('This is an evolution simulation. In this simulation, critters will spawn in based on parameters you set. They have two traits, sense and speed, which affect their behaviour. Food will spawn on the map and if they eat food and gain enough energy they will reproduce. Every time they move they lose energy and if they lose all their energy they will die. Over time, the most adapted individuals will survive demonstrating Darwins theory of natural selection. Press the left arrow key to slow down the simulation and the right one to speed up. The preys energy will be visible in the form of their color. As their energy decreases they will slowly turn red, and at maximum energy, they will be green. Sense will be visible as the circle around the critter. The sun wraps around the map, and food will only spawn inside the sun.')
print()
print()



#Defining the prey class
class Prey:
    def __init__(self, energy, size, speed, sense, x, y):
        self.energy = energy
        self.size = size
        self.speed = speed
        self.sense = sense
        self.x = x
        self.y = y
        self.body = Oval(self.x, self.y, 5, 7, fill='green', border = 'black', borderWidth = .2)
        self.body.rotateAngle = randrange(360)
        self.reproduced = False
        self.time = .00001
        self.vision = Circle(x, y, self.sense, opacity = 10)

    def move(self, myApp):
        if(self.vision.hitsShape(myApp.food)):
            closest = 100000 # init with some large value
            thingsToRemove = []
            for fruit in myApp.food:
                if(fruit.hitsShape(self.body) == True):
                    self.eatFood()
                    thingsToRemove.append(fruit)
                elif(distance(self.body.centerX, self.body.centerY, fruit.centerX, fruit.centerY) < closest):
                    closestFoodX = fruit.centerX
                    closestFoodY = fruit.centerY
                    closest = distance(self.body.centerX,self.body.centerY,fruit.centerX,fruit.centerY)
            
            for fruit in thingsToRemove:
                myApp.food.remove(fruit)

            self.body.rotateAngle = angleTo(self.body.centerX, self.body.centerY, closestFoodX, closestFoodY)

        else:
            self.body.rotateAngle += randrange(-30,30)

        self.body.centerX, self.body.centerY = getPointInDir(self.body.centerX, self.body.centerY, self.body.rotateAngle, self.speed)
        self.vision.centerX, self.vision.centerY = self.body.centerX, self.body.centerY
        self.x, self.y = self.body.centerX, self.body.centerY

        self.wrap(myApp)
        
        self.energy -= (self.speed*self.speed*self.size*self.size*self.size+self.sense)*self.time
        self.time += .000001

        self.updateColorBasedOnEnergy()

    def updateColorBasedOnEnergy(self):
        if(self.energy <= 100 and self.energy > 0):
            self.body.fill = rgb(255-int(self.energy*255/100),int(self.energy*255/100),0)

    def wrap(self, myApp):
        if(self.body.left>app.width-myApp.border.borderWidth):
            self.body.right = myApp.border.borderWidth

        if(self.body.right<myApp.border.borderWidth):
            self.body.left = app.width-myApp.border.borderWidth

        if(self.body.top>app.height-myApp.border.borderWidth):
            self.body.bottom = myApp.border.borderWidth

        if(self.body.bottom<myApp.border.borderWidth):
            self.body.top = app.height- myApp.border.borderWidth
        
    def eatFood(self):
        self.energy += 40
            
    def die(self):
        self.body.visible = False
        self.vision.visible = False
        
    def reproduce(self, myApp):
        if(self.reproduced == False):
            if(randrange(100) > 0):
                p = Prey(100,
                    self.size,
                    self.speed*pythonRound(random.uniform(0.8, 1.2), 2),
                    self.sense*pythonRound(random.uniform(0.8, 1.2), 2),
                    self.x,self.y)
            else:
                p = Prey(100,
                    self.size,
                    self.speed,
                    self.sense,
                    self.x,self.y)
            myApp.preys.append(p)
            self.energy -= 100
            self.reproduced = True

class MyApp:
    def __init__(self):
        app.setMaxShapeCount(100000)

        #Initialization
        app.width = int(input("What should be the width of the simulation map? WARNING: MAKING THIS VALUE TOO LARGE WILL CAUSE LAG. I recommend 600 for a smoooth simulation."))
        app.height = int(input("What should be the length of the simulation map? WARNING: MAKING THIS VALUE TOO LARGE WILL CAUSE LAG. I recommend 300 for a smoooth simulation."))
        self.border = Rect(0,0,app.width,app.height,fill=None,borderWidth=10,border='black')
        self.food = Group()
        app.counter = 0
        self.time = Label("Time: " + str(app.counter),45,15)
        self.sun = Group()
        app.background = 'lightGreen'
        self.preys = []
        self.avgSpeed = Label('Avg Speed: ', 45, 40)
        app.avgSpeedVal = 10
        self.avgSpeed.top = self.time.bottom
        app.avgSenseValue = 0
        self.avgSense = Label('Avg Sense: ',10,10)
        self.avgSense.top = self.avgSpeed.bottom
        self.pop =Label(0,45,60)
        self.pop.top = self.avgSense.bottom
        app.stepsPerSecond = 60
        self.numFood = Label(100,10,10)
        self.numFood.top = self.pop.bottom

        # Create Sun
        for i in range(int(app.width/10)):
            self.sun.add(Rect(5*i,0,5,app.height,fill=gradient('yellow','gold','orange',start='top'),opacity=50))

        # Making Food
        howMuchFood = input("How much food should there be to begin with? I suggest 100 for a good simulation...")
        for i in range(int(howMuchFood)):
            self.food.add(
                    Circle(randrange(app.width), randrange(app.height), 3, fill=gradient('green','yellow','red',start='bottom'))
                    )
        
        howManyPreys = input("How many critters should there be to begin with? I recommend 10 for a good simulation...")
        initSpeed = input("What should be the initial speed of these critters? Speed will determine how fast the critters move each tick, but a higher speed uses more energy. I recommend 10 for a good simulation...")
        initSense = input("What should be the initial sense of the critters? Sense is the radius the critters can see. A higher sense means they'll be able to find food faster, but will also use more energy. I recommend 10 for a good simulation...")
        
        self.foodPerStep = input("How much food should be added every tick? Food spawns inside the sun and critters need it to survive. I recommend 2 for a good simulation...")

        # Spawn preys
        for i in range(int(howManyPreys)):
            p = Prey(100,10,int(initSpeed),int(initSense),randrange(app.width),randrange(app.height))
            self.preys.append(p)

    def updateLabels(self, app):
        app.counter+=1
        self.time.value = "Time: " + str(app.counter)
        self.food.toFront()
        self.border.toFront()
        self.time.toFront()
        self.time.left = 10
        self.avgSpeed.value = "Avg Speed: " + str(app.avgSpeedVal)
        self.avgSpeed.left = 10
        app.avgSpeedVal = 0
        self.avgSense.value = "Avg Sense: " + str(app.avgSenseValue)
        self.avgSense.left = 10
        app.avgSenseValue = 0
        self.pop.value = 'Pop: ' + str(len(self.preys))
        self.pop.left = 10
        self.numFood.value = 'Food: ' + str(len(self.food))
        self.numFood.left = 10
        self.pop.toFront()
        self.avgSpeed.toFront()
        self.avgSense.toFront()

    def spwanNewFood(self):
        for i in range(int(self.foodPerStep)):
            x,y = randrange(self.sun.left, self.sun.right), randrange(self.sun.top, self.sun.bottom)
            
            while(not self.sun.hits(x,y)):
                x,y = randrange(self.sun.left, self.sun.right),randrange(self.sun.top, self.sun.bottom)
            
            self.food.add(Circle(x,y,3,fill=gradient('green','yellow','red',start='bottom')))

    
    def moveSunToTheRight(self,app):      
        for ray in self.sun.children:
            ray.centerX+=1
            if(ray.right>app.width):
                ray.left=0

    def onStep(self, app):
        self.updateLabels(app)

        if(app.counter%1 == 0):
            self.spwanNewFood()

        self.moveSunToTheRight(app)

        preysToRemove = []  
        for prey in myApp.preys:
            app.avgSpeedVal += prey.speed
            app.avgSenseValue += prey.sense
            prey.reproduced = False
            prey.move(myApp)

            if(prey.energy <= 0):
                prey.die()
                preysToRemove.append(prey)
            
            if(prey.energy>120):
                prey.reproduce(myApp)

        if(len(myApp.preys) != 0):
            app.avgSpeedVal /= len(myApp.preys)
            app.avgSpeedVal = pythonRound(app.avgSpeedVal,2)
            app.avgSenseValue /= len(myApp.preys)
            app.avgSenseValue = pythonRound(app.avgSenseValue,2)

        for prey in preysToRemove:
            myApp.preys.remove(prey)

myApp = MyApp()

#Controls What Happens Every Tick
def onStep():
    myApp.onStep(app)

# Changes the speed of the sim
def onKeyPress(key: str):
    if(key == 'left' and app.stepsPerSecond > 6):
        app.stepsPerSecond -= 5
    if(key == 'right'):
        app.stepsPerSecond += 5
    print('The program is running at ' + str(app.stepsPerSecond) + ' ticks per second')

cmu_graphics.run()
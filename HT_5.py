from colorama import Fore, Back, Style, init
import simpy
import random

init(autoreset = True)

def proceso(env,name,RAM,CPU,IO,arrivingTime,amount,instructions,einstructions):
    global startTime
    #Condicionamiento de tiempo que tarda en ejecutar las instrucciones
    
    #Simula la llegada de los proceso
    yield env.timeout(arrivingTime)
    print('\x1b[1;37;44m'+'El %s ha llegado en el tiempo %d y cuenta con %s instrucciones' % (name, env.now,instructions))
    
    
    #Pide una cantidad de memoria para continuar con el proceso
    yield RAM.get(amount)
    print('El %s ha tomado %d Megabytes de memoria RAM' % (name, amount))
    startTime = env.now
    
    #Ejecuta la funcion running
    env.process(running(env,name,CPU,instructions,einstructions,RAM))
     
       
def running(env,name,CPU,instructions,einstructions,RAM):
    
    global totalTime
    
    #El proceso está listo para ser ejecutado, solo falta que lo atienda el CPU
    with CPU.request() as req:  #Se pide atención por el CPU
        yield req
        #va en otra funcion para poder hacer un ciclo de ejecuciones        
        #Verificaciónd de la cantidad de instrucciones que tiene el proceso
        if (instructions < einstructions): #Cuando el proceso tiene menos de 3 instrucciones y el CPU se libera con anticipacion
            print('El CPU ha iniciado a ejecutar %s instrucciones del %s en el tiempo %s' % (instructions,name, env.now))
            yield env.timeout(2) #Tiempo que tarda en ejecutar menos de 3 instrucciones
            yield RAM.put(amount) #Como ya termino de ejecutar sus instrucciones, entonces regresa la memoria
            print('\033[1;37;42m'+'El %s ha finalizado la ejecucicion de sus instrucciones en el tiempo %s' % (name, env.now))
            endTime = env.now
            processTime = endTime - startTime
            print('\033[1;37;41m''El tiempo que se ha tardado en ejecutar el %s es de: %s' %(name,processTime))
            totalTime += processTime
            instructions = 0
            
        elif (instructions == einstructions): #Cuando el proceso tiene 3 instrucciones
            print('El CPU ha iniciado a ejecutar 3 instrucciones del %s en el tiempo %s' % (name, env.now))
            yield env.timeout(3) #Tiempo que tarda en ejecutar 3 instrucciones
            yield RAM.put(amount) #Como ya termino de ejecutar las 3 instrucciones, regresa la memoria y se libera el CPU
            print('\033[1;37;42m'+ 'El %s ha finalizado la ejecucicion de sus instrucciones en el tiempo %s' % (name, env.now))
            endTime = env.now
            processTime = endTime - startTime
            print('\033[1;37;41m''El tiempo que se ha tardado en ejecutar el %s es de: %s' %(name,processTime))
            totalTime += processTime
            instructions = 0
            
        else: #Cuando el proceso tiene más de 3 instrucciones
            print('El CPU ha iniciado a ejecutar %s instrucciones del %s en el tiempo %s' % (einstructions,name,env.now))
            yield env.timeout(3) #Tiempo que tarda en ejecutar 3 instrucciones
            instructions -= 3
            print('\033[1;31m' + 'El %s aun cuenta con %s instrucciones restantes' % (name, instructions))
            
    if(instructions > 0):
        decision = random.randint(1,2) #Cuando sale del CPU analiza si va a ir a waiting o regresa a ready
        if decision == 1: #Cuando el número generado es 1 va a realizar operaciones I/O
            print('El %s se dirige a realizar operaciones de entrada y salida' % (name))
            with IO.request() as req:  #Pide atencion para poder realizar las operaciones de I/O
                yield req
                yield env.timeout(1)
                print('El %s ha finalizado las operaciones de entrada y salida en el tiempo %s' % (name,env.now))
            print('El %s se dirige a la cola, para esperar la atencion del CPU' % (name))
            env.process(running(env,name,CPU,instructions,einstructions,RAM))#Realiza nuevamente el proceso de espera y la ejecuacion de las instrucciones
        else:
            print('El %s se dirige a la cola, para esperar la atencion del CPU' % (name))
            env.process(running(env,name,CPU,instructions,einstructions,RAM))




#Datos variables a lo largo de las simulaciones
totalTime = 0    
env = simpy.Environment()
SEED = 10
RAM = simpy.Container(env,init = 100, capacity = 100)
CPU = simpy.Resource(env, capacity = 1)
IO = simpy.Resource(env, capacity = 1)
NO_PROCESS = 5

print('Simulacion de Ejecucion de Programas')
random.seed(SEED)
                
for i in range(NO_PROCESS):
    #timeDriving = random.randint(1,5)
    arrivingTime = random.expovariate(1.0/10)
    amount = random.randint(1,10)
    instructions = random.randint(1,10)
    env.process(proceso(env, 'Proceso %d' % i, RAM, CPU, IO, arrivingTime,amount,instructions,3))
    
    
#Se ejecuta la simulacion
env.run()
print()
print('\033[1;30m'+'PROMEDIO:' , (totalTime/NO_PROCESS))
            
            
            
            
        
        
        
        
        
        
        
    
    
    

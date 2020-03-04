import simpy
import random


def proceso(env,name,RAM,CPU,IO,arrivingTime,amount,instructions,einstructions):
    #Condicionamiento de tiempo que tarda en ejecutar las instrucciones
    if instructions < 3:
        attentionTime = 2
    else:
        attentionTime = 4
    
    #Simula la llegada de los proceso
    yield env.timeout(arrivingTime)
    print('El %s ha llegado en el tiempo %d y cuenta con %s instrucciones' % (name, env.now,instructions))
    
    #Pide una cantidad de memoria para continuar con el proceso
    yield RAM.get(amount)
    print('El %s ha tomado %d Megabytes de memoria RAM' % (name, amount))
    
    env.process(running(env,name,CPU,instructions,einstructions,RAM))
    
    
    
                

         
    #Cuando las instruccioes son mayores que 3 lo que hace es que realiza las instrucciones que puede y lo que haya quedado como instrucciones restantes o el resto de procesos que encesita
    #ejecutar los hacer fuera del with para que asi agarre otras instrucciones
    
env = simpy.Environment()
SEED = 10
RAM = simpy.Container(env,init = 100, capacity = 100)
CPU = simpy.Resource(env, capacity = 1)
IO = simpy.Resource(env, capacity = 1)

print('Simulacion de Ejecucion de Programas')
random.seed(SEED)
                
for i in range(5):
    #timeDriving = random.randint(1,5)
    arrivingTime = random.expovariate(1.0/10)
    amount = random.randint(1,10)
    instructions = random.randint(1,10)
    env.process(proceso(env, 'Proceso %d' % i, RAM, CPU, IO, arrivingTime,amount,instructions,3))
    
    
#Se ejecuta la simulacion
env.run()    
            
            
            
            
        
        
        
        
        
        
        
    
    
    

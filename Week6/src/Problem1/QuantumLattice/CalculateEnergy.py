#Finding total energy of lattice
def CalulateEnergy(lattice,interactionMatrix,selfEnergyVector):
    totalEnergy = 0

    #Energy by self-energy
    for quantum in lattice:
        #print(f"Type extracted : {type(selfEnergyVector[quantum])} of value : {selfEnergyVector[quantum]}")
        totalEnergy += selfEnergyVector[quantum]

    #print(f"total energy after self-energy:{totalEnergy}")
    #Energy by interaction
    for quantum in lattice:
        for interact_quantum in lattice:
            totalEnergy += interactionMatrix[quantum][interact_quantum]

    #print(f"Energy after interation:{totalEnergy}")
    return totalEnergy
